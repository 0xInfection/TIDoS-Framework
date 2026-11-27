#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Insecure CORS -- which foreign origins may read the target's responses?"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlsplit

import requests

from core.methods import modkit as kit
from core.methods.inject import marker
from core.methods.print import pvln

info = ("This module searches for CORS misconfigurations. It sends requests with crafted "
        "Origin headers (arbitrary origin, null, prefix/suffix lookalikes such as "
        "evil-target.com and target.com.evil.com, an unescaped-dot lookalike, a subdomain and "
        "an http:// downgrade of the target) and reports every origin the server explicitly "
        "trusts in Access-Control-Allow-Origin. Trust combined with "
        "Access-Control-Allow-Credentials: true lets that origin read authenticated data "
        "(the severe case).")
searchinfo = "Insecure Cross Origin Resource Sharing"
properties = {
    **kit.AUTH_OPTIONS,
}


@dataclass
class Probe:
    name: str
    origin: str
    severity_creds: str     # severity when credentials are allowed
    severity_plain: str     # severity without credentials
    why: str


def probes(url: str, host: str, domain: str) -> list[Probe]:
    rnd = marker(6)
    scheme = urlsplit(url).scheme
    out = [
        Probe("arbitrary origin", f"https://{rnd}.com", "HIGH", "LOW",
              "any website is trusted"),
        Probe("null origin", "null", "HIGH", "LOW",
              "the 'null' origin (sandboxed iframes, data: URLs) is trusted"),
        Probe("suffix match", f"https://{rnd}{domain}", "HIGH", "LOW",
              f"any domain ending in '{domain}' is trusted (attacker registers {rnd}{domain})"),
        Probe("prefix match", f"https://{host}.{rnd}.com", "HIGH", "LOW",
              f"any domain starting with '{host}' is trusted"),
        Probe("subdomain", f"https://{rnd}.{domain}", "LOW", "INFO",
              "every subdomain is trusted (an XSS or takeover on any subdomain reads this endpoint)"),
    ]
    if "." in host:
        first, rest = host.split(".", 1)
        out.append(Probe("unescaped dot", f"https://{first}{rnd[:1]}{rest}", "HIGH", "LOW",
                         "the allowlist regex has an unescaped '.' (matches any character)"))
    if scheme == "https":
        out.append(Probe("http downgrade", f"http://{host}", "MEDIUM", "INFO",
                         "the plain-HTTP origin is trusted: a network attacker injecting into "
                         "http:// pages can read HTTPS responses"))
    return out


def ask(session, url: str, origin: str):
    """(ACAO, ACAC, Vary) for a request carrying `origin`; None on errors."""
    try:
        r = session.get(url, headers={"Origin": origin} if origin else None,
                        allow_redirects=False)
    except requests.RequestException as e:
        kit.bad(f"Request failed: {type(e).__name__}")
        return None
    return (r.headers.get("Access-Control-Allow-Origin", "").strip(),
            r.headers.get("Access-Control-Allow-Credentials", "").strip().lower() == "true",
            "origin" in r.headers.get("Vary", "").lower())


def icors(web):
    pvln("icors")
    record = kit.Recorder(web, kit.MISCONFIG, "icors")
    session = kit.http(headers=kit.request_headers(properties))

    # test the final URL: CORS is evaluated on the response that is read
    try:
        url = session.get(kit.url(web), allow_redirects=True).url
    except requests.RequestException as e:
        kit.bad(f"Could not reach {kit.url(web)}: {type(e).__name__}")
        return []
    host = urlsplit(url).hostname or kit.host(web)
    domain = kit.domain(web) if not kit.is_ip(host) else host
    kit.info(f"Testing {url}")

    base = ask(session, url, "")
    if base and base[0]:
        kit.info(f"Without Origin: Access-Control-Allow-Origin: {base[0]}"
                 + (" (with credentials)" if base[1] else ""))

    findings = []
    wildcard = reflects_any = False
    for p in probes(url, host, domain):
        if reflects_any and p.name != "null origin":
            continue  # implied by the arbitrary-origin finding
        res = ask(session, url, p.origin)
        if res is None:
            continue
        acao, acac, vary = res
        if acao == "*":
            wildcard = True
            continue
        if acao.lower() != p.origin.lower():
            continue
        sev = p.severity_creds if acac else p.severity_plain
        cred = "with credentials" if acac else "without credentials"
        line = f"[{sev}] {p.name}: Origin '{p.origin}' reflected in ACAO {cred} -- {p.why}"
        if not vary and acao == p.origin and p.name == "arbitrary origin":
            line += "; no 'Vary: Origin' (cache poisoning risk)"
        findings.append((sev, line))
        reflects_any = reflects_any or p.name == "arbitrary origin"

    if wildcard:
        kit.info("Access-Control-Allow-Origin: * (public read access; browsers never send "
                 "credentials with a wildcard).")
        record("ACAO: * (public, no credentials)")
    if not findings:
        kit.good("No insecure CORS configuration found.")
        record("No insecure CORS configuration found.")
        return []
    order = ("HIGH", "MEDIUM", "LOW", "INFO")
    for sev, line in sorted(findings, key=lambda f: order.index(f[0])):
        if sev in ("HIGH", "MEDIUM"):
            kit.found("CORS misconfiguration", line)
        else:
            kit.warn(line)
        record(line)
    if any(s == "HIGH" for s, _ in findings):
        kit.warn("An attacker page can read this endpoint's responses with the victim's cookies.")
    return findings


def attack(web):
    icors(web)
