#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""HTTP security header audit."""

from core.methods import modkit as kit
from core.methods import secheaders as sh
from core.methods.print import pvln

info = ("Audits the security headers of the target's response: Content-Security-Policy "
        "(unsafe-inline/unsafe-eval, wildcard and gadget-host sources, object-src, base-uri), "
        "HSTS (max-age, includeSubDomains, preload), X-Frame-Options vs CSP frame-ancestors, "
        "X-Content-Type-Options, Referrer-Policy, Permissions-Policy, COOP/CORP, the deprecated "
        "X-XSS-Protection/HPKP/Expect-CT, and version or debug information leaking through "
        "Server, X-Powered-By, X-AspNet-Version, X-Debug-Token and similar headers.")
searchinfo = "HTTP Header Analysis"
properties = {}


def headers(web):
    pvln("http header analysis")
    record = kit.Recorder(web, kit.MISCONFIG, "headers")
    resp = sh.fetch(web)
    if resp is None:
        return []
    chain = " -> ".join([r.url for r in resp.history] + [resp.url])
    kit.info(f"Analysing headers of {chain} (HTTP {resp.status_code})")

    issues = sh.audit(resp)
    if not issues:
        kit.good("No security header issues found.")
        record("No security header issues found.")
        return []
    counts = {s: sum(i.severity == s for i in issues) for s in sh.SEVERITIES}
    sh.show(issues, record)
    summary = ", ".join(f"{n} {s.lower()}" for s, n in counts.items() if n)
    kit.info(f"{len(issues)} header issues: {summary}")
    return issues


def attack(web):
    headers(web)
