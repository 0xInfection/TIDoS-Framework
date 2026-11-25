#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WAF fingerprinter -- names the firewall / filtering proxy in front of the target."""

from __future__ import annotations

import random
import string

import requests

from core.methods import modkit as kit
from core.methods.print import pscan
from modules.ScanningEnumeration.wafimpo import STRONG, blocked, detect, failure, snapshot

info = ("This module tries to fingerprint the firewall the targeted Web application uses. "
        "It sends a normal request, a request with a harmless parameter and the same "
        "request carrying an obvious attack payload (SQLi, XSS, path traversal), then "
        "matches ~65 WAF/CDN signatures (vendor headers, cookies, server banners and "
        "block pages) and reports the evidence for each hit. If the attack request is "
        "blocked but no product matches, it reports an unidentified WAF/filter.")
searchinfo = "Firewall Fingerprinter"
properties = {}

PAYLOAD = "1' OR '1'='1' -- <script>alert(document.cookie)</script> ../../../../etc/passwd"


def fetch(session, url, params=None):
    try:
        return snapshot(session.get(url, params=params))
    except requests.RequestException as e:
        return failure(e)


def waf(web):
    pscan("waf enumeration")
    url = kit.url(web)
    record = kit.Recorder(web, kit.SCAN, "waf")
    session = kit.http()

    kit.info(f"Sending a normal request to {url}...")
    try:
        resp = session.get(url)
    except requests.RequestException as e:
        kit.bad(f"Could not reach {url}: {type(e).__name__}")
        return []
    normal = [snapshot(r) for r in (*resp.history, resp)]

    param = "".join(random.choice(string.ascii_lowercase) for _ in range(6))
    kit.info("Sending a benign and a malicious request to compare the responses...")
    benign = fetch(session, url, {param: "1234"})
    hostile = fetch(session, url, {param: PAYLOAD})
    why = blocked(benign, hostile)

    detections = detect([*normal, benign, hostile], hostile, bool(why))
    if not why and any(d.blockpage for d in detections):
        why = f"a block page was served (HTTP {hostile.status})"
        detections = detect([*normal, benign, hostile], hostile, True)

    kit.kv_table([
        ("Normal request", f"HTTP {resp.status_code}"),
        ("Benign parameter", benign.error or f"HTTP {benign.status}"),
        ("Attack payload", (hostile.error or f"HTTP {hostile.status}") + (" (blocked)" if why else "")),
        ("Server", resp.headers.get("Server")),
    ])
    lines = []
    for d in detections:
        conf = "strong" if d.confidence == STRONG else "weak"
        kit.found("Firewall detected", f"{d.product} ({conf} evidence)")
        for e in d.evidence:
            kit.bullet(e)
        lines.append(f"{d.product} ({conf}): " + "; ".join(d.evidence))

    if detections:
        if why:
            kit.info(f"The attack request was blocked: {why}.")
        else:
            kit.warn("The attack request was not blocked; the WAF may be in monitoring mode, "
                     "or the matched product is a CDN/proxy without filtering enabled.")
    elif why:
        kit.found("Firewall detected", "unknown WAF/filter likely")
        kit.bullet(f"attack request: {why}")
        lines.append(f"Unknown WAF/filter likely: attack request got {why}")
    else:
        kit.bad("No WAF detected: no signature matched and the attack request was not blocked.")
        lines.append("No WAF detected.")

    record(lines)
    kit.good("WAF fingerprinting module completed!")
    return [d.product for d in detections] or (["unknown"] if why else [])


def attack(web):
    waf(web)
