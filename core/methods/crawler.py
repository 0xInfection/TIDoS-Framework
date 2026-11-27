#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""
Same-host, depth-limited web crawling, powered by Katana (core/methods/katana.py).

Depth 0 is the start page, depth N the pages N clicks away; links found on
the last level are reported but not followed. Only the target's host is
crawled -- off-host links are listed, never fetched. Endpoints referenced
from JavaScript are discovered too. Binary assets are classified, soft-404
pages are recognised, and a page cap bounds the run.

    result = crawl(target, depth=2, max_pages=200, headers={"Cookie": "..."})
    result.params      # in-scope URLs with a query string
    result.forms       # Form(page, method, action, inputs)
    result.error       # why the crawl could not run (Katana missing...), or ""

run() is the whole module flow used by the crawler modules.
"""

from __future__ import annotations

import base64
import hashlib
import os
import re
import uuid
from dataclasses import dataclass, field
from typing import Callable
from urllib.parse import parse_qsl, unquote, urldefrag, urljoin, urlsplit, urlunsplit

from core.Core.colors import C, G, GR, O, R, color
from core.methods import katana
from core.methods import modkit as kit

SKIP_EXT = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp", ".css",
            ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".mp3", ".zip", ".pdf")

ASSET_EXT = SKIP_EXT + (
    ".bmp", ".tif", ".tiff", ".avif", ".otf", ".avi", ".mov", ".mkv", ".webm",
    ".wav", ".ogg", ".flac", ".m4a", ".7z", ".rar", ".tar", ".gz", ".tgz", ".bz2",
    ".xz", ".exe", ".msi", ".dmg", ".apk", ".iso", ".bin", ".deb", ".rpm", ".jar",
    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".ods", ".swf",
    ".js", ".mjs", ".map",
)
HTML_TYPES = ("", "text/html", "application/xhtml+xml")
TEXT_TYPES = ("json", "xml", "javascript", "text/")
DEFAULT_PORTS = {"http": 80, "https": 443}
MAX_BODY = 5 * 1024 * 1024
DEFAULT_MAXPAGES = 200

# not followed while crawling with credentials: one click would end the session
LOGOUT = re.compile(r"log[-_]?out|log[-_]?off|sign[-_]?out|sign[-_]?off|destroy[-_]?session", re.I)


# --------------------------------------------------------------------------
# URLs
# --------------------------------------------------------------------------

def normalise(link: str, base: str = "") -> str | None:
    """Canonical absolute http(s) URL, or None for anything uncrawlable.

    Resolves relative links against `base`, drops the fragment and any
    credentials, lowercases scheme/host, strips default ports, turns an
    empty path into "/" and sorts query parameters so that ?a=1&b=2 and
    ?b=2&a=1 are the same page.
    """
    link = (link or "").strip()
    if not link:
        return None
    try:
        parts = urlsplit(urldefrag(urljoin(base, link))[0])
        port = parts.port
    except ValueError:
        return None
    scheme = parts.scheme.lower()
    if scheme not in DEFAULT_PORTS or not parts.hostname:
        return None
    host = parts.hostname.lower()
    if ":" in host:
        host = f"[{host}]"
    netloc = host if port in (None, DEFAULT_PORTS[scheme]) else f"{host}:{port}"
    query = "&".join(sorted(p for p in parts.query.split("&") if p))
    return urlunsplit((scheme, netloc, parts.path or "/", query, ""))


def scope(url: str) -> tuple[str, int | None]:
    """Host identity of a URL: hostname plus non-default port.

    http:// and https:// on default ports are the same scope, so an
    http -> https upgrade does not leave the target.
    """
    parts = urlsplit(url)
    port = parts.port
    return parts.hostname or "", None if port in DEFAULT_PORTS.values() else port


def is_asset(url: str) -> bool:
    return urlsplit(url).path.lower().endswith(ASSET_EXT)


# --------------------------------------------------------------------------
# results
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Form:
    page: str
    method: str
    action: str
    inputs: tuple[str, ...]


@dataclass
class Page:
    url: str
    depth: int
    status: int | None = None
    note: str = ""         # soft-404, redirect target, content type, error
    body: str = ""
    binary: bool = False   # answered with non-text content


@dataclass
class Result:
    start: str
    depth: int
    pages: dict[str, Page] = field(default_factory=dict)    # fetched
    internal: set[str] = field(default_factory=set)        # in scope, seen
    external: set[str] = field(default_factory=set)
    scripts: set[str] = field(default_factory=set)
    assets: set[str] = field(default_factory=set)
    forms: list[Form] = field(default_factory=list)
    soft404: set[str] = field(default_factory=set)
    error: str = ""                                        # set when the crawl could not run
    skipped: set[str] = field(default_factory=set)         # logout links (authenticated crawl)
    truncated: bool = False

    @property
    def urls(self) -> list[str]:
        """Every in-scope page URL, crawled or merely discovered."""
        return sorted(self.internal - self.assets)

    @property
    def params(self) -> list[str]:
        """In-scope URLs carrying query parameters (fuzzing candidates)."""
        return [u for u in self.urls
                if urlsplit(u).query and u not in self.soft404 and u not in self.skipped]

    @property
    def parameters(self) -> list[str]:
        """Distinct parameter names from query strings and form fields."""
        names = {k for u in self.params for k, _ in parse_qsl(urlsplit(u).query, True)}
        names.update(n for f in self.forms for n in f.inputs)
        return sorted(names)


# --------------------------------------------------------------------------
# fetching and parsing
# --------------------------------------------------------------------------

def _fetch(session, page: Page) -> tuple[Page, str]:
    """Fill in status/body of `page`; returns (page, redirect location)."""
    try:
        with session.get(page.url, allow_redirects=False, stream=True) as r:
            page.status = r.status_code
            location = r.headers.get("Location", "") if r.is_redirect else ""
            ctype = r.headers.get("Content-Type", "").split(";")[0].strip().lower()
            if not 200 <= r.status_code < 300:
                return page, location
            if ctype not in HTML_TYPES:
                page.note = ctype
                page.binary = not any(t in ctype for t in TEXT_TYPES)
                return page, ""
            raw = b""
            for chunk in r.iter_content(64 * 1024):
                raw += chunk
                if len(raw) >= MAX_BODY:
                    break
            page.body = raw.decode(r.encoding or "utf-8", errors="replace")
            return page, ""
    except Exception as e:
        page.note = type(e).__name__
        return page, ""


def _fingerprint(page: str, body: str) -> str:
    """Body hash with the requested path removed (soft-404 pages echo it)."""
    path = urlsplit(page).path
    tokens = {path, unquote(path), path.rsplit("/", 1)[-1]} - {""}
    for token in sorted(tokens, key=len, reverse=True):
        body = body.replace(token, "")
    return hashlib.md5(" ".join(body.split()).encode()).hexdigest()


def _soft404(session, start: str) -> str:
    """Fingerprint of the target's "not found" page if it answers 200."""
    probe = Page(urljoin(start, f"/{uuid.uuid4().hex}.html"), 0)
    _fetch(session, probe)
    if probe.status == 200 and probe.body:
        kit.warn("Target answers 200 for missing pages; soft-404s will be skipped.")
        return _fingerprint(probe.url, probe.body)
    return ""


# --------------------------------------------------------------------------
# crawling (Katana)
# --------------------------------------------------------------------------

def _content_type(headers: dict) -> str:
    for k, v in (headers or {}).items():
        if k.lower() == "content-type":
            return str(v).split(";")[0].strip().lower()
    return ""


def crawl(target, depth: int, max_pages: int = DEFAULT_MAXPAGES,
          on_page: Callable[[Page], None] | None = None,
          headers: dict[str, str] | None = None, keep_bodies: bool = False,
          js: bool = True) -> Result:
    """Crawl the target's host down to `depth` clicks with Katana.

    Katana fetches the pages (and, with `js`, endpoints referenced from
    JavaScript); this function classifies what it reports: pages with
    status/forms, in-scope URLs merely discovered, scripts, assets,
    off-host links and soft-404s. `headers` (e.g. kit.request_headers())
    go with every request; when they or URL credentials authenticate the
    crawl, logout-looking links are excluded so the session survives.
    At most `max_pages` pages are fetched; `on_page` sees each one.
    Page bodies are dropped unless `keep_bodies`. If Katana cannot run,
    res.error says why and the result is empty.
    """
    raw = kit.url(target)
    start = normalise(raw)
    res = Result(start or raw, depth)
    if not start:
        return res
    home = scope(start)

    hdrs = dict(headers or {})
    creds = urlsplit(raw)
    if creds.username:
        token = base64.b64encode(f"{unquote(creds.username)}:{unquote(creds.password or '')}".encode()).decode()
        hdrs.setdefault("Authorization", f"Basic {token}")
    authenticated = bool(creds.username or headers)
    soft = _soft404(kit.http(headers=hdrs), start)

    depths = {start: 0}
    forms_seen: dict[tuple, Form] = {}
    res.internal.add(start)
    try:
        stream = katana.crawl(start, depth=depth, max_pages=max_pages, headers=hdrs, js=js,
                              out_scope=[LOGOUT.pattern] if authenticated else [])
        for item in stream:
            req = item.get("request") or {}
            url = normalise(req.get("endpoint", ""))
            if not url:
                continue
            source = normalise(req.get("source", "")) or start
            level = depths.setdefault(url, depths.get(source, 0) + 1 if url != start else 0)
            if scope(url) != home:
                res.external.add(url)
                continue
            res.internal.add(url)
            path = urlsplit(url)
            if authenticated and LOGOUT.search(f"{path.path}?{path.query}"):
                res.skipped.add(url)
                continue
            if req.get("tag") == "script" or path.path.lower().endswith((".js", ".mjs")):
                res.scripts.add(url)
            elif is_asset(url):
                res.assets.add(url)
            resp = item.get("response") or {}
            if not resp.get("status_code") or item.get("error") or url in res.pages:
                continue            # discovered, not fetched (depth limit, scope, error)
            if depth == 0 and url != start:
                continue            # Katana's minimum depth is 1

            page = Page(url, level, status=resp["status_code"])
            ctype = _content_type(resp.get("headers") or {})
            body = resp.get("body") or ""
            if ctype not in HTML_TYPES:
                page.note = ctype
                page.binary = not any(t in ctype for t in TEXT_TYPES)
            if 300 <= page.status < 400:
                page.note = "redirect"
            if body and soft and page.status == 200 and _fingerprint(url, body) == soft:
                page.note = "soft-404"
                res.soft404.add(url)
                body = ""
            page.body = body if keep_bodies and not page.binary else ""
            for f in resp.get("forms") or []:
                action = normalise(f.get("action") or url, url)
                if not action:
                    continue
                if authenticated and LOGOUT.search(action):
                    res.skipped.add(action)
                    continue
                inputs = tuple(dict.fromkeys(p for p in (f.get("parameters") or []) if p))
                form = Form(url, (f.get("method") or "GET").upper(), action, inputs)
                forms_seen.setdefault((form.method, form.action, form.inputs), form)
            res.pages[url] = page
            if on_page:
                on_page(page)
            if len(res.pages) >= max_pages:
                res.truncated = True
                stream.close()
                break
    except katana.KatanaError as e:
        res.error = str(e)
    res.forms = list(forms_seen.values())
    return res


# --------------------------------------------------------------------------
# module flow
# --------------------------------------------------------------------------

def _progress(page: Page) -> None:
    status = page.status or "ERR"
    tint = G if page.status and page.status < 300 and page.note != "soft-404" else (
        O if page.status and page.status < 400 else R)
    note = f" {GR}{page.note}" if page.note else ""
    print(f"{GR} [{page.depth}] {C}{page.url} {tint}({status}){note}{color.END}")


def _listing(title: str, items) -> None:
    items = list(items)
    if items:
        kit.found(title, len(items))
        for item in items:
            kit.bullet(item)


def write_links(target, urls: list[str]) -> str:
    """tmp/logs/<host>-logs/<host>-links.lst (read by the SQLi modules)."""
    folder = kit.logdir(target)
    name = os.path.basename(folder).rsplit("-logs", 1)[0]
    path = os.path.join(folder, f"{name}-links.lst")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(urls) + ("\n" if urls else ""))
    return path


def run(target, properties: dict, depth: int, lvl2: str) -> Result:
    """Crawl, print a summary, store it and write the URL list."""
    max_pages = kit.integer(properties, "MAXPAGES", "Maximum number of pages to fetch",
                            DEFAULT_MAXPAGES)
    external = kit.flag(properties, "INCLUDE_EXTERNAL",
                        "List off-host links too (never followed)?", True)
    if max_pages < 1:
        kit.warn(f"MAXPAGES must be positive, using {DEFAULT_MAXPAGES}.")
        max_pages = DEFAULT_MAXPAGES

    kit.info(f"Crawling {kit.url(target)} (depth {depth}, at most {max_pages} pages)")
    headers = kit.request_headers(properties)
    if headers:
        kit.info(f"Sending {', '.join(sorted(headers))} with every request.")
    res = crawl(target, depth, max_pages, _progress, headers=headers)
    if res.error:
        kit.bad(res.error)
        return res
    first = res.pages.get(res.start)
    if not first or first.status is None:
        kit.bad(f"Target unreachable: {first.note}." if first else
                f"Cannot crawl {res.start}: the start page could not be fetched.")
        return res
    if res.truncated:
        kit.warn(f"Page cap of {max_pages} reached; raise MAXPAGES to crawl further.")

    print()
    _listing("URLs with parameters", res.params)
    _listing("Forms", (f"{f.method} {f.action}  [{', '.join(f.inputs) or 'no fields'}]  (on {f.page})"
                       for f in res.forms))
    _listing("Scripts", sorted(res.scripts))
    if external:
        _listing("External links (not followed)", sorted(res.external))
    _listing("Logout links/forms (not followed, they would end the session)", sorted(res.skipped))

    reached = sum(1 for p in res.pages.values() if p.status and p.status < 400
                  and p.note != "soft-404")
    print()
    kit.kv_table([
        ("Pages fetched", f"{len(res.pages)} ({reached} reachable)"),
        ("In-scope URLs", len(res.urls)),
        ("URLs with parameters", len(res.params)),
        ("Parameter names", ", ".join(res.parameters)),
        ("Forms", len(res.forms)),
        ("Scripts", len(res.scripts)),
        ("Assets skipped", len(res.assets)),
        ("Soft-404 pages", len(res.soft404)),
        ("External links", len(res.external)),
    ])

    urls = [u for u in res.urls if u not in res.soft404]
    saved = urls + sorted(res.external) if external else urls
    kit.Recorder(target, kit.CRAWL, lvl2)(saved)
    path = write_links(target, urls)
    kit.good(f"Crawl done: {len(urls)} in-scope URL(s) saved to {path}")
    return res
