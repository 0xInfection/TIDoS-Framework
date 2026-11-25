#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WAF fingerprinter -- names the firewall / filtering proxy in front of the target.

Detection is delegated to wafw00f (https://github.com/EnableSecurity/wafw00f),
which ships ~170 WAF/CDN signatures and is maintained upstream. wafw00f drives
its own requests, so when `tor on` is active we hand it our Tor SOCKS proxy.
"""

from __future__ import annotations

import logging

import requests

import core.variables as variables
from core.methods import modkit as kit
from core.methods import tor
from core.methods.print import pscan

info = ("This module fingerprints the firewall the targeted Web application sits "
        "behind. It uses wafw00f, which sends a normal request and a batch of "
        "attack requests (SQLi, XSS, LFI, ...) and matches ~170 WAF/CDN signatures "
        "(vendor headers, cookies, server banners and block pages). If no product "
        "matches but the target still behaves defensively, it reports a generic, "
        "unidentified WAF/filter and the evidence for it.")
searchinfo = "Firewall Fingerprinter"
properties = {}


def _proxies():
    """wafw00f-style proxy dict honouring `tor on`, or None for a direct connection."""
    if variables.tor:
        return {"http": tor.TOR_PROXY, "https": tor.TOR_PROXY}
    return None


def waf(web):
    pscan("waf enumeration")
    url = kit.url(web)
    record = kit.Recorder(web, kit.SCAN, "waf")

    try:
        from wafw00f.main import WAFW00F
    except ImportError:
        kit.bad("wafw00f is not installed. Install it with: pip install wafw00f")
        return []

    # Reach the target with our own (Tor-aware) session first, both to fail early
    # with a clear message and to surface the Server banner.
    kit.info(f"Sending a normal request to {url}...")
    try:
        resp = kit.http().get(url)
    except requests.RequestException as e:
        kit.bad(f"Could not reach {url}: {type(e).__name__}")
        return []
    server = resp.headers.get("Server")

    # wafw00f chatters on its own logger; keep the console clean.
    logging.getLogger("wafw00f").setLevel(logging.CRITICAL)

    kit.info("Probing with attack payloads and matching WAF signatures (wafw00f)...")
    scanner = WAFW00F(target=url, proxies=_proxies(), followredirect=True, timeout=10)
    try:
        result = scanner.identwaf(findall=True)
    except Exception as e:  # noqa: BLE001 -- wafw00f raises a variety of request errors
        kit.bad(f"WAF fingerprinting failed: {type(e).__name__}")
        return []
    # identwaf returns (list, url) on current wafw00f, a bare list on older ones.
    detected = list(result[0]) if isinstance(result, tuple) else list(result)

    generic = ""
    if not detected:
        try:
            if scanner.genericdetect():
                generic = scanner.knowledge["generic"]["reason"]
        except Exception:  # noqa: BLE001
            pass

    kit.kv_table([
        ("Target", url),
        ("Server", server),
        ("Signatures checked", str(len(scanner.wafdetections))),
    ])

    lines = []
    if detected:
        for name in detected:
            kit.found("Firewall detected", name)
            lines.append(name)
        if len(detected) > 1:
            kit.info("More than one product matched; the target may chain a CDN and a WAF.")
    elif generic:
        kit.found("Firewall detected", "generic / unidentified WAF")
        for part in str(generic).splitlines():
            part = part.strip()
            if part:
                kit.bullet(part)
        lines.append("Generic WAF/filter likely: " + " ".join(str(generic).split()))
    else:
        kit.bad("No WAF detected: no signature matched and the target did not behave defensively.")
        lines.append("No WAF detected.")

    record(lines)
    kit.good("WAF fingerprinting module completed!")
    return detected or (["generic"] if generic else [])


def attack(web):
    waf(web)
