#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Cross Site Tracing -- TRACE/TRACK enabled and echoing request headers."""

from __future__ import annotations

from urllib.parse import urlsplit, urlunsplit

import requests

from core.methods import modkit as kit
from core.methods.inject import marker
from core.methods.print import pvln

info = ("This module searches for Cross Site Tracing (XST): it sends TRACE and TRACK requests "
        "carrying a random header and reports the method as enabled only when the response "
        "echoes that header back. Modern browsers forbid TRACE from scripts, so XST itself is "
        "mostly historical, but an echoing TRACE still discloses headers that proxies add "
        "(internal IPs, auth tokens) and is flagged by compliance scans.")
searchinfo = "Cross Site Tracing"
properties = {
    "PORT": ["Port to use (default: the target URL's port)", ""],
}


def target_url(web) -> str:
    url = kit.url(web)
    port = kit.option(properties, "PORT", "Port to use", "")
    if not port:
        return url + "/"
    if not port.isdigit() or not 0 < int(port) < 65536:
        kit.warn(f"Invalid port '{port}', using the URL's port.")
        return url + "/"
    p = urlsplit(url)
    scheme = "https" if port == "443" else ("http" if port == "80" else p.scheme)
    netloc = p.netloc.rsplit("@", 1)
    host = netloc[-1]
    if host.startswith("["):
        host = host.split("]")[0] + "]"
    else:
        host = host.split(":")[0]
    netloc[-1] = f"{host}:{port}"
    return urlunsplit((scheme, "@".join(netloc), p.path.rstrip("/") + "/", "", ""))


def xsstrace(web):
    pvln("xss tracer")
    record = kit.Recorder(web, kit.MISCONFIG, "xsstrace")
    session = kit.http()
    url = target_url(web)
    kit.info(f"Testing {url}")

    findings = []
    for method in ("TRACE", "TRACK"):
        name, value = f"X-Tidos-{marker(4)}", marker(10)
        try:
            r = session.request(method, url, headers={name: value}, allow_redirects=False)
        except requests.RequestException as e:
            kit.bad(f"{method}: request failed ({type(e).__name__})")
            continue
        echoed = value in r.text and name.lower() in r.text.lower()
        if r.status_code < 300 and echoed:
            ctype = r.headers.get("Content-Type", "-")
            kit.found(f"{method} enabled", f"HTTP {r.status_code}, request echoed ({ctype})")
            findings.append(f"{method} enabled: HTTP {r.status_code} echoes request headers "
                            f"(random header {name} reflected, Content-Type {ctype})")
            if "cookie" in r.text.lower() or "authorization" in r.text.lower():
                kit.warn("The echo includes Cookie/Authorization headers.")
        else:
            kit.bullet(f"{method}: HTTP {r.status_code}" + (", no echo" if r.status_code < 300 else ""))

    if not findings:
        kit.good("TRACE/TRACK are disabled or do not echo the request.")
        record("Not vulnerable to Cross-Site Tracing: TRACE/TRACK disabled or not echoing.")
        return []
    for f in findings:
        record(f)
    return findings


def attack(web):
    xsstrace(web)
