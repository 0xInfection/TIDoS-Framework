#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cookie security flags (Secure / HttpOnly / SameSite / prefixes)."""

from urllib.parse import urlsplit

from core.methods import modkit as kit
from core.methods import secheaders as sh
from core.methods.print import pvln

info = ("This module analyzes the security of the cookies the target sets (on the page and "
        "on every redirect leading to it): Secure, HttpOnly and SameSite flags, SameSite=None "
        "without Secure, __Host-/__Secure- prefix rules and parent-domain scoping. "
        "Session-like cookie names are rated higher than other cookies.")
searchinfo = "Cookie Analysis"
properties = {
    **kit.AUTH_OPTIONS,
}


def cookiecheck(web):
    pvln("Cookie check")
    record = kit.Recorder(web, kit.MISCONFIG, "cookiecheck")
    session = kit.http(headers=kit.request_headers(properties))
    resp = sh.fetch(web, session)
    if resp is None:
        return []

    cookies = []
    for r in (*resp.history, resp):
        for raw in sh.raw_values(r, "Set-Cookie"):
            c = sh.parse_set_cookie(raw)
            if c and not c.deleted:
                cookies.append((r, c))
    if not cookies:
        kit.bad("The target sets no cookies.")
        record("No cookies set.")
        return []

    kit.good(f"{len(cookies)} cookie(s) set")
    issues = []
    for r, c in cookies:
        https = urlsplit(r.url).scheme == "https"
        found = sh.analyze_cookie(c, https, urlsplit(r.url).hostname or "")
        flags = [f for f, on in (("Secure", c.secure), ("HttpOnly", c.httponly)) if on]
        if c.samesite:
            flags.append(f"SameSite={c.samesite}")
        print()
        kit.found(f"Cookie {c.name}", ", ".join(flags) or "no security flags")
        if not found:
            kit.good("All flags set properly.")
            record(f"Cookie {c.name}: OK ({', '.join(flags)})")
        sh.show(found, record)
        issues += found
    return issues


def attack(web):
    cookiecheck(web)
