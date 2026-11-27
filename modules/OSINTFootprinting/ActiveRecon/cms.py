#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""CMS detector -- WhatCMS API lookup plus local builtwith fingerprinting."""

from __future__ import annotations

import builtwith
import requests

from core.methods import modkit as kit
from core.methods.print import posintact

info = ("This module tries to determine if the target is running a CMS. It asks the "
        "WhatCMS.org API (needs WHATCMS_ACCESS_TOKEN) and fingerprints the page "
        "headers and HTML locally with builtwith.")
searchinfo = "CMS Detector"
properties = {}

WHATCMS_API = "https://whatcms.org/API/CMS"


def whatcms(web) -> str | None:
    """CMS name (with version) according to WhatCMS, None if unknown."""
    target = kit.host(web)
    if kit.is_ip(target) or target == "localhost":
        kit.warn("WhatCMS needs a public hostname, skipping lookup.")
        return None
    kit.info("Passive fingerprinting via WhatCMS.org...")
    key = kit.apikey("WHATCMS_ACCESS_TOKEN")
    if not key:
        kit.warn("Skipping WhatCMS lookup.")
        return None
    try:
        res = kit.http().get(WHATCMS_API, params={"key": key, "url": target}).json()
    except (requests.RequestException, ValueError) as e:
        kit.bad(f"WhatCMS query failed: {type(e).__name__}")
        return None
    result = res.get("result") or {}
    if result.get("code") != 200:
        kit.bad(f"WhatCMS: {result.get('msg') or 'no answer'}")
        return None
    name = " ".join(filter(None, (result.get("name"), result.get("version"))))
    return name or None


def fingerprint(web) -> list[str] | None:
    """CMS names builtwith finds in the target's headers and HTML (None on failure)."""
    kit.info("Active fingerprinting of the target page...")
    url = kit.url(web)
    try:
        r = kit.http().get(url)
    except requests.RequestException as e:
        kit.bad(f"Could not fetch {url}: {type(e).__name__}")
        return None
    try:
        techs = builtwith.builtwith(r.url, headers=r.headers, html=r.text)
    except Exception as e:  # third-party regex soup, don't let it kill the run
        kit.bad(f"builtwith failed: {e}")
        return []
    others = {k: v for k, v in techs.items() if k != "cms"}
    if others:
        kit.info("Other technologies:")
        kit.kv_table((k, ", ".join(v)) for k, v in sorted(others.items()))
    return techs.get("cms", [])


def cms(web):
    posintact("cms detector")
    record = kit.Recorder(web, kit.ACTIVE, "cms")

    detected = []
    name = whatcms(web)
    if name:
        kit.found("CMS detected (WhatCMS)", name)
        detected.append(name)
    local = fingerprint(web)
    for name in local or []:
        kit.found("CMS detected", name)
        if name not in detected:
            detected.append(name)

    if detected:
        record(detected)
    elif local is None:
        kit.bad("Could not determine the CMS.")
    else:
        kit.bad(f"{kit.url(web)} doesn't seem to use a CMS")
        record("No CMS detected.")
    kit.good("CMS detection module completed!")
    return detected


def attack(web):
    cms(web)
