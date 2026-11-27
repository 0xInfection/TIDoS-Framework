#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Alternate site discovery -- compare what the target serves to different User-Agents."""

import hashlib
from collections import Counter

import requests

from core.methods import modkit as kit
from core.methods.print import posintact

info = ("Requests the target with several User-Agents (desktop, mobile, legacy IE, "
        "Googlebot) and reports when a client is served a different site: other "
        "status code, a redirect elsewhere or substantially different content.")
searchinfo = "Alternate Site Discovery"
properties = {}

BASELINE = "Chrome on Windows"
USER_AGENTS = {
    BASELINE: kit.USER_AGENT,
    "Safari on iOS": ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
                      "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"),
    "Chrome on Android": ("Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36"),
    "IE6 on Windows XP": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
    "Googlebot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
}
# dynamic pages (tokens, timestamps) never hash the same twice; below this
# similarity we call it a different site
SIMILARITY = 0.95


def _fetch(session, url, agent):
    r = session.get(url, headers={"User-Agent": agent}, allow_redirects=True)
    return {"status": r.status_code, "url": r.url.rstrip("/"), "body": r.text,
            "md5": hashlib.md5(r.content).hexdigest()}


def _similarity(a: str, b: str) -> float:
    """Cheap, order-insensitive character overlap ratio (0..1)."""
    if not a and not b:
        return 1.0
    ca, cb = Counter(a), Counter(b)
    return 2 * sum((ca & cb).values()) / (len(a) + len(b))


def _differences(base, resp):
    diffs = []
    if resp["status"] != base["status"]:
        diffs.append(f"status {base['status']} -> {resp['status']}")
    if resp["url"] != base["url"]:
        diffs.append(f"redirected to {resp['url']}")
    if resp["md5"] != base["md5"]:
        ratio = _similarity(base["body"], resp["body"])
        if ratio < SIMILARITY:
            diffs.append(f"content {ratio:.0%} similar ({len(base['body'])} vs {len(resp['body'])} chars)")
    return diffs


def altsites(web):
    posintact("alternative sites")
    url = kit.url(web)
    session = kit.http()
    record = kit.Recorder(web, kit.ACTIVE, "altsites")

    responses = {}
    for name, agent in USER_AGENTS.items():
        try:
            responses[name] = resp = _fetch(session, url, agent)
        except requests.RequestException as e:
            kit.bad(f"{name}: request failed ({type(e).__name__})")
            if name == BASELINE:
                kit.bad("Baseline request failed, nothing to compare against.")
                return {}
            continue
        kit.info(f"{name:<18} -> {resp['status']}  {len(resp['body'])} chars  md5 {resp['md5']}")

    base = responses[BASELINE]

    alternates = {}
    for name, resp in responses.items():
        if name == BASELINE:
            continue
        diffs = _differences(base, resp)
        if diffs:
            alternates[name] = diffs
            kit.found(f"{name} differs from baseline", "; ".join(diffs))

    if alternates:
        record([f"{n} differs from baseline: {'; '.join(d)}" for n, d in alternates.items()])
    else:
        kit.bad("No alternative site found via User-Agent spoofing.")
        record(f"No alternative site found via User-Agent spoofing: {base['md5']}")
    kit.good("Alternate site discovery completed!")
    return alternates


def attack(web):
    altsites(web)
