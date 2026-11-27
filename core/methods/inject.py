#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""
Injection points and request plumbing shared by the vulnerability scanners.

    points = inject.discover(target, properties)    # PARAM option, else crawl
    for point in points:
        r = point.send(session, payload)            # value replaced by payload
        r = point.send(session, payload, append=True)  # original value + payload
    findings = inject.scan(points, check)           # check(point) per point, concurrently
    inject.report(findings, kit.Recorder(target, kit.CRITICAL, "xss"))

A Point is one parameter of one request (a query-string parameter of a URL
or a field of a form). Every other parameter keeps its original value.

The PARAM option accepts:
    /page.php?id=1                    relative to the target
    https://host/page.php?id=1&q=x    absolute
    POST /login.php user=a&pass=b     form body (method first)
Without PARAM the target is crawled (DEPTH, default 1) and every query
parameter and form field found becomes a point, capped by MAXPOINTS.
"""

from __future__ import annotations

import difflib
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Callable, Iterable
from urllib.parse import parse_qsl, quote, urlencode, urljoin, urlsplit, urlunsplit

import core.variables as variables
from core.methods import modkit as kit

DEFAULT_DEPTH = 1
DEFAULT_MAXPOINTS = 40
CRAWL_PAGES = 60

# merge into a module's `properties` so every scanner exposes the same knobs:
#     properties = {**inject.OPTIONS, "DICT": [...]}
OPTIONS = {
    "PARAM": ["Endpoint to test, e.g. /page.php?id=1 or 'POST /login user=a&pass=b' (empty: crawl)", ""],
    "DEPTH": [f"Crawl depth used when PARAM is empty (default {DEFAULT_DEPTH})", ""],
    "MAXPOINTS": [f"Maximum injection points tested (default {DEFAULT_MAXPOINTS})", ""],
}


# --------------------------------------------------------------------------
# injection points
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Point:
    method: str                          # GET or POST
    url: str                             # request URL without the query string
    params: tuple[tuple[str, str], ...]  # all parameters with original values
    name: str                            # the parameter being injected

    @property
    def original(self) -> str:
        return dict(self.params).get(self.name, "")

    def values(self, value: str, append: bool = False) -> list[tuple[str, str]]:
        new = (self.original + value) if append else value
        return [(k, new if k == self.name else v) for k, v in self.params]

    def url_for(self, value: str, append: bool = False, raw: bool = False) -> str:
        """GET URL carrying `value`; with raw=True the injected value is not
        percent-encoded (for payloads that are already encoded, e.g. %0d%0a)."""
        if not raw:
            return f"{self.url}?{urlencode(self.values(value, append))}"
        parts = []
        for k, v in self.values(value, append):
            v = v if k == self.name else quote(v, safe="")
            parts.append(f"{quote(k, safe='')}={v}")
        return f"{self.url}?{'&'.join(parts)}"

    def send(self, session, value: str, append: bool = False, raw: bool = False, **kw):
        """Send the request with `value` injected; None on network errors."""
        try:
            if self.method == "POST":
                return session.post(self.url, data=self.values(value, append), **kw)
            return session.get(self.url_for(value, append, raw), **kw)
        except Exception:
            return None

    def __str__(self) -> str:
        return f"{self.method} {self.url} [{self.name}]"


def _points(method: str, url: str, params: list[tuple[str, str]]) -> list[Point]:
    params = tuple((k, v) for k, v in params if k)
    return [Point(method, url, params, name) for name in dict.fromkeys(k for k, _ in params)]


def from_url(url: str, method: str = "GET", body: str = "") -> list[Point]:
    """One point per parameter of a URL (query) or of a POST body."""
    parts = urlsplit(url)
    base = urlunsplit((parts.scheme, parts.netloc, parts.path or "/", "", ""))
    if method == "POST":  # a query string stays on the URL; body fields are injected
        base = urlunsplit((parts.scheme, parts.netloc, parts.path or "/", parts.query, ""))
        return _points("POST", base, parse_qsl(body, keep_blank_values=True))
    return _points("GET", base, parse_qsl(parts.query, keep_blank_values=True))


def from_form(form) -> list[Point]:
    """Points from a crawler.Form; fields get a harmless default value."""
    method = "POST" if form.method == "POST" else "GET"
    action = urlsplit(form.action)
    base = urlunsplit((action.scheme, action.netloc, action.path or "/", "", ""))
    params = parse_qsl(action.query, keep_blank_values=True) if method == "GET" else []
    params += [(name, "1") for name in form.inputs]
    if method == "POST" and action.query:
        base = form.action
    return _points(method, base, params)


def parse_spec(target, spec: str) -> list[Point]:
    """Points from a PARAM value (see module docstring)."""
    spec = spec.strip()
    method, body = "GET", ""
    head, _, rest = spec.partition(" ")
    if head.upper() in ("GET", "POST") and rest:
        method = head.upper()
        spec, _, body = rest.strip().partition(" ")
    url = spec if spec.startswith(("http://", "https://")) else urljoin(kit.url(target), spec)
    return from_url(url, method, body.strip())


def _dedupe(points: Iterable[Point]) -> list[Point]:
    seen, out = set(), []
    for p in points:
        key = (p.method, p.url, p.name)
        if key not in seen:
            seen.add(key)
            out.append(p)
    return out


def discover(target, properties: dict, key: str = "PARAM") -> list[Point]:
    """Injection points from the PARAM option, the target URL, or a crawl."""
    spec = kit.option(properties, key, "Endpoint to test, e.g. /page.php?id=1 (enter to crawl)", "")
    limit = max(1, kit.integer(properties, "MAXPOINTS", "Maximum injection points", DEFAULT_MAXPOINTS))
    if spec:
        points = parse_spec(target, spec)
        if not points:
            kit.bad(f"No parameters in '{spec}'. Give one like /page.php?id=1.")
        return points[:limit]

    points = from_url(kit.url(target))  # vicadd https://host/page?id=1
    depth = max(0, kit.integer(properties, "DEPTH", "Crawl depth", DEFAULT_DEPTH))
    from core.methods import crawler  # late import: crawler pulls in bs4/lxml
    kit.info(f"No PARAM set; crawling {kit.url(target)} (depth {depth}) for parameters...")
    res = crawler.crawl(target, depth, max_pages=CRAWL_PAGES, headers=kit.request_headers(properties))
    if res.error:
        kit.bad(f"{res.error} Set PARAM to test a specific endpoint without crawling.")
    for url in res.params:
        points += from_url(url)
    for form in res.forms:
        points += from_form(form)
    points = _dedupe(points)
    if not points:
        kit.bad("No parameters found. Set PARAM, e.g. 'set PARAM /page.php?id=1'.")
    elif len(points) > limit:
        kit.warn(f"{len(points)} injection points found; testing the first {limit} (raise MAXPOINTS).")
    else:
        kit.info(f"{len(points)} injection point(s) found.")
    return points[:limit]


# --------------------------------------------------------------------------
# helpers for checks
# --------------------------------------------------------------------------

def marker(n: int = 8) -> str:
    """Random lowercase canary that will not occur in a page by chance."""
    return "tid" + "".join(random.choices(string.ascii_lowercase + string.digits, k=n))


def text(resp) -> str:
    """Body of a response as text ('' for None)."""
    if resp is None:
        return ""
    try:
        return resp.text
    except Exception:
        return ""


def ratio(a: str, b: str, cap: int = 20000) -> float:
    """Similarity 0..1 of two bodies (for boolean/blind comparisons)."""
    if a == b:
        return 1.0
    return difflib.SequenceMatcher(None, a[:cap], b[:cap], autojunk=False).ratio()


def payloads(properties: dict, default: str, key: str = "DICT", label: str = "payload") -> list[str]:
    """Payload list from the DICT option or the bundled default file."""
    path = kit.option(properties, key, f"Path to the {label} list", default) or default
    items = kit.wordlist(path)
    if not items:
        kit.bad(f"No {label}s loaded from {path}.")
    return items


# --------------------------------------------------------------------------
# running checks
# --------------------------------------------------------------------------

@dataclass
class Finding:
    point: Point
    payload: str
    evidence: str = ""
    kind: str = ""
    extra: dict = field(default_factory=dict)

    def __str__(self) -> str:
        kind = f"{self.kind}: " if self.kind else ""
        ev = f" -- {self.evidence}" if self.evidence else ""
        return f"{kind}{self.point} payload={self.payload!r}{ev}"


def scan(points: list[Point], check: Callable[[Point], Iterable[Finding]],
         workers: int | None = None) -> list[Finding]:
    """Run check(point) for each point concurrently; findings in point order."""
    if not points:
        return []
    workers = workers or max(1, min(variables.processes, len(points), 16))
    results: dict[int, list[Finding]] = {}
    pool = ThreadPoolExecutor(max_workers=workers)
    try:
        futures = {pool.submit(lambda p=p: list(check(p) or [])): i for i, p in enumerate(points)}
        for fut in as_completed(futures):
            i = futures[fut]
            try:
                results[i] = fut.result()
            except Exception as e:
                kit.bad(f"{points[i]}: {type(e).__name__}: {e}")
                results[i] = []
            for f in results[i]:
                kit.found(f.kind or "Vulnerable", f"{f.point} <- {f.payload}")
    except KeyboardInterrupt:
        kit.bad("Interrupted; reporting what was found so far.")
        for fut in futures:
            fut.cancel()
    finally:
        pool.shutdown(wait=False)
    return [f for i in sorted(results) for f in results[i]]


def report(findings: list[Finding], record, clean: str = "No vulnerable parameters found.") -> None:
    """Summarise findings and store them (or the clean verdict)."""
    if not findings:
        kit.bad(clean)
        record(clean)
        return
    print()
    kit.good(f"{len(findings)} finding(s):")
    for f in findings:
        kit.bullet(f)
    record(str(f) for f in findings)
