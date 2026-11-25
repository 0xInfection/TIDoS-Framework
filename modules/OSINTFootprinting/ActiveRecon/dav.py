#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WebDAV enumeration -- probes the SEARCH and PROPFIND methods."""

from __future__ import annotations

import re

import requests

from core.methods import modkit as kit
from core.methods.print import posintact

info = ("DAV HTTP enumeration module. Sends WebDAV SEARCH and PROPFIND requests to "
        "the target and reports when they return a DAV directory listing.")
searchinfo = "DAV HTTP Enumeration"
properties = {}

HEADERS = {"Content-Type": 'application/xml; charset="utf-8"'}

SEARCH_BODY = """<?xml version="1.0"?>
<g:searchrequest xmlns:g="DAV:">
<g:sql>
Select "DAV:displayname" from scope()
</g:sql>
</g:searchrequest>
"""

PROPFIND_BODY = """<?xml version="1.0"?>
<a:propfind xmlns:a="DAV:">
<a:prop>
<a:displayname/>
</a:prop>
</a:propfind>
"""

# (method, label, body, extra headers, signature of a DAV listing)
PROBES = [
    ("SEARCH", "htsearch", SEARCH_BODY, {},
     re.compile(r"<\w*:?response\b|<\w*:?status\b|xmlns:\w+=[\"']DAV:[\"']", re.I)),
    ("PROPFIND", "profind", PROPFIND_BODY, {"Depth": "1"},
     re.compile(r"<\w*:?href\b|<\w*:?multistatus\b", re.I)),
]


def probe(session, url, method, body, headers, signature) -> bool | None:
    """True/False: DAV listing or not; None: the request itself failed."""
    try:
        r = session.request(method, url, data=body.encode(),
                            headers={**HEADERS, **headers}, allow_redirects=False)
    except requests.RequestException as e:
        kit.bad(f"{method} request failed: {type(e).__name__}")
        return None
    kit.info(f"{method} -> HTTP {r.status_code}")
    # 207 Multi-Status is the proper WebDAV answer; some servers send 200
    return r.status_code in (200, 207) and bool(signature.search(r.text))


def dav(web):
    posintact("dav http enumeration")
    url = kit.url(web)
    session = kit.http()
    record = kit.Recorder(web, kit.ACTIVE, "dav")

    enabled = []
    for method, label, body, headers, signature in PROBES:
        kit.info(f"Probing HTTP {method}...")
        result = probe(session, url, method, body, headers, signature)
        if result is None:
            continue
        if result:
            kit.found(f"HTTP {method} enabled, DAV directory listing at", url)
            record(f"{label}: {url}")
            enabled.append(method)
        else:
            kit.bad(f"No HTTP {method} profiling found.")
            record(f"No HTTP {method} profiling found.")

    kit.good("HTTP profiling of DAV completed!")
    return enabled


def attack(web):
    dav(web)
