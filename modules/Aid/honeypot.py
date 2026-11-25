#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Honeypot detector -- Shodan HoneyScore for the target's IP."""

from __future__ import annotations

from core.methods import modkit as kit
from core.methods.print import title

info = ("Estimates the probability that the target is a honeypot using Shodan's "
        "HoneyScore service. Needs TIDOS_SHODAN_API_KEY (see docs/setup.md).")
searchinfo = "HoneyScore Calculator"
properties = {}

ENDPOINT = "https://api.shodan.io/labs/honeyscore/{ip}"


def banner():
    print("""
                __/   _
        .__  __.  \\__/   __
         .-`'-.   /  \\__/
     .-.(  oo  ).-. _/  \\__/   {}
 __ :   \\".~~."/   ; \\__/
/  \\_`.  Y`--'Y  .' _/  \\__   {}
 __/  `./======\\.'   \\__/  \\_
/  \\__/ \\======/  \\__/  \\__/
\\__/   (_`----'_)    \\__/  \\ (shodan)
    """.format(title("Honeypot"), title("Detector")))


def honeypot(web):
    banner()
    key = kit.apikey("SHODAN_API_KEY")
    if not key:
        return
    ip = kit.resolve(web)
    if not ip:
        kit.bad(f"Could not resolve {kit.host(web)}.")
        return
    kit.info(f"Querying Shodan HoneyScore for {ip}...")
    try:
        resp = kit.http(timeout=20).get(ENDPOINT.format(ip=ip), params={"key": key})
    except Exception as e:
        kit.bad(f"Shodan API unreachable: {type(e).__name__}")
        return
    if resp.status_code != 200:
        kit.bad(f"Shodan API error: HTTP {resp.status_code} -- {resp.text.strip()[:100]}")
        return
    try:
        score = float(resp.text.strip())
    except ValueError:
        kit.bad(f"Unexpected Shodan response: {resp.text.strip()[:100]}")
        return
    percent = f"{score * 100:.0f}%"
    if score < 0.5:
        kit.good(f"Target does not look like a honeypot (HoneyScore {percent}).")
    else:
        kit.warn(f"Potential honeypot detected (HoneyScore {percent}).")


def attack(web):
    honeypot(web)
