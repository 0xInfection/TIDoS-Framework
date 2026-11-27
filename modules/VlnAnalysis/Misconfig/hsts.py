#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""HTTP Strict Transport Security check."""

from urllib.parse import urlsplit, urlunsplit

import requests

from core.methods import modkit as kit
from core.methods import secheaders as sh
from core.methods.print import pvln

info = ("This module checks if the target uses HSTS: whether it is served over HTTPS, "
        "whether plain HTTP redirects to HTTPS, and whether the Strict-Transport-Security "
        "header is valid and strong (max-age, includeSubDomains, preload eligibility). "
        "It also notes certificates browsers would reject (HSTS is useless then).")
searchinfo = "HSTS Check"
properties = {}


def with_scheme(url, scheme):
    parts = urlsplit(url)
    netloc = parts.netloc
    if parts.port in (80, 443):
        netloc = netloc.rsplit(":", 1)[0]
    return urlunsplit((scheme, netloc, parts.path or "/", parts.query, ""))


def hsts(web):
    pvln("hsts")
    record = kit.Recorder(web, kit.MISCONFIG, "hsts")
    session = kit.http()
    url = kit.url(web)
    lines = []

    if urlsplit(url).scheme == "http" and urlsplit(url).port not in (None, 80):
        kit.bad("Target is plain HTTP on a non-standard port: HSTS is not applicable.")
        record("Plain HTTP on a non-standard port: HSTS not applicable.")
        return
    if urlsplit(url).scheme == "http":
        try:
            r = session.get(url, allow_redirects=True)
            if urlsplit(r.url).scheme == "https":
                kit.good(f"HTTP redirects to HTTPS ({r.url})")
            else:
                kit.warn("Plain HTTP is served without redirecting to HTTPS.")
                lines.append("[LOW] HTTP is served without a redirect to HTTPS")
        except requests.RequestException as e:
            kit.info(f"HTTP not reachable ({type(e).__name__}).")
        url = with_scheme(url, "https")

    try:
        resp = session.get(url, allow_redirects=True)
    except requests.RequestException as e:
        kit.bad(f"HTTPS not available at {url}: {type(e).__name__}")
        record("No HTTPS: HSTS not applicable." + (" " + "; ".join(lines) if lines else ""))
        return
    if urlsplit(resp.url).scheme != "https":
        kit.warn(f"HTTPS redirects back to plain HTTP ({resp.url}).")
        record("[MEDIUM] HTTPS redirects back to plain HTTP: HSTS cannot apply.")
        return

    values = sh.raw_values(resp, "Strict-Transport-Security")
    kit.kv_table([("URL", resp.url), ("Strict-Transport-Security", " | ".join(values) or "(none)")])
    issues = sh.analyze_hsts(values, https=True)
    for line in lines:
        record(line)
    if issues:
        sh.show(issues, record)
    else:
        kit.good("HSTS header is properly configured.")
        record(f"HSTS properly configured: {values[0]}")
    try:
        requests.get(resp.url, timeout=10, proxies=session.proxies,
                     headers={"User-Agent": kit.USER_AGENT}, allow_redirects=False)
    except requests.exceptions.SSLError:
        sh.show([sh.Issue(sh.MEDIUM, "TLS certificate", "not trusted: browsers ignore HSTS "
                                                        "from sites with certificate errors")], record)
    except requests.RequestException:
        pass


def attack(web):
    hsts(web)
