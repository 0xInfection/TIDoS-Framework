#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Host header injection -- does the application build URLs from Host?"""

from __future__ import annotations

import re

import requests

from core.methods import modkit as kit
from core.methods.inject import marker
from core.methods.print import pvln

info = ("This module tries to determine if the target is vulnerable to Host Header Injection. "
        "It sends a random host name in Host, X-Forwarded-Host, X-Host, X-Forwarded-Server, "
        "X-HTTP-Host-Override and Forwarded, and reports a finding only when that host comes "
        "back in the Location header or inside links/URLs of the page (password-reset "
        "poisoning, cache poisoning, open redirect). Plain-text echoes on successful pages are "
        "reported as 'possible'; echoes on error pages are ignored.")
searchinfo = "Host Header Injection"
properties = {
    **kit.AUTH_OPTIONS,
}

OVERRIDES = ("X-Forwarded-Host", "X-Host", "X-Forwarded-Server", "X-HTTP-Host-Override",
             "Forwarded")
URL_CONTEXT = r"""(?:https?:)?//{host}|(?:href|src|action|content|url)\s*=\s*["']?[^"'\s>]*{host}"""


def classify(resp, canary: str) -> tuple[str, str] | None:
    """(confidence, evidence) when `canary` is reflected in a meaningful place."""
    loc = resp.headers.get("Location", "")
    if canary in loc.lower():
        return "confirmed", f"Location: {loc}"
    for name, value in resp.headers.items():
        if name.lower() not in ("location", "content-length") and canary in value.lower():
            return "confirmed", f"{name}: {value[:150]}"
    body = resp.text.lower() if resp.content else ""
    if canary not in body:
        return None
    m = re.search(URL_CONTEXT.format(host=re.escape(canary)), body)
    if m:
        start = max(0, m.start() - 40)
        return "confirmed", "URL in body: ..." + resp.text[start:m.end() + 40].strip() + "..."
    if resp.status_code < 400:
        i = body.index(canary)
        return "possible", "text in body: ..." + resp.text[max(0, i - 40):i + 60].strip() + "..."
    return None


def hhi(web):
    pvln("host header Injection")
    record = kit.Recorder(web, kit.MISCONFIG, "hhi")
    session = kit.http(headers=kit.request_headers(properties))
    url = kit.url(web) + "/"
    real = kit.host(web)

    try:
        base = session.get(url, allow_redirects=False)
    except requests.RequestException as e:
        kit.bad(f"Could not reach {url}: {type(e).__name__}")
        return []
    kit.info(f"Baseline: HTTP {base.status_code}")

    findings = []
    for header in ("Host",) + OVERRIDES:
        canary = f"{marker(8)}.com"
        if header == "Host":
            hdrs = {"Host": canary}
        elif header == "Forwarded":
            hdrs = {"Forwarded": f"host={canary}"}
        else:
            hdrs = {header: canary}
        try:
            r = session.get(url, headers=hdrs, allow_redirects=False)
        except requests.RequestException as e:
            kit.info(f"{header}: request failed ({type(e).__name__})")
            continue
        hit = classify(r, canary)
        if hit is None:
            kit.bullet(f"{header}: not reflected (HTTP {r.status_code})")
            continue
        conf, evidence = hit
        line = f"{header}: injected host reflected [{conf}] ({evidence})"
        if conf == "confirmed":
            kit.found("Host header injection", line)
        else:
            kit.warn(line)
        findings.append(f"HTTP {r.status_code} {line}")

    if not findings:
        kit.good(f"The application does not build URLs from an injected host ({real}).")
        record("No host header injection found.")
        return []
    for f in findings:
        record(f)
    kit.info("Check password reset / e-mail links and cached pages: they may embed the "
             "attacker's host.")
    return findings


def attack(web):
    hhi(web)
