#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Google+ profile gathering -- passive recon."""

from core.methods import modkit as kit
from core.methods.print import posintpas

info = "Enumerate profiles using Google (Google+ People API)."
searchinfo = "Google Gathering"
properties = {
    "LIMIT": ["Maximum number of profiles (1-50)", ""],
}

API = "https://www.googleapis.com/plus/v1/people"
FIELDS = [("Kind", "kind"), ("E-Tag", "etag"), ("ObjectType", "objectType"),
          ("ID", "id"), ("DisplayName", "displayName"), ("Link", "url")]


def googlenum(web):
    posintpas("google gathering")
    key = kit.apikey("GOOGLE_API_TOKEN")
    if not key:
        kit.bad("This module cannot be used without a Google API token.")
        return []
    limit = max(1, min(kit.integer(properties, "LIMIT", "Maximum number of profiles", 50), 50))
    domain = kit.host(web)

    kit.info(f"Searching profiles for {domain} (max {limit})...")
    try:
        resp = kit.http().get(API, params={"query": domain, "key": key, "maxResults": limit})
    except Exception as e:
        kit.bad(f"Request to the Google API failed: {e}")
        return []
    try:
        data = resp.json()
    except ValueError:
        kit.bad(f"Unexpected answer from the Google API (HTTP {resp.status_code}).")
        return []
    if "error" in data:
        kit.bad(f"Google API error: {data['error'].get('message', data['error'])}")
        return []

    profiles = data.get("items") or []
    if not profiles:
        kit.bad("No profiles found.")
        kit.warn("Google+ was shut down in 2019: this API now always returns an empty feed.")
        return []

    record = kit.Recorder(web, kit.PASSIVE, "googlenum")
    for n, person in enumerate(profiles, 1):
        kit.good(f"Profile {n}")
        kit.kv_table((label, person.get(field)) for label, field in FIELDS)
    record({label: [p.get(field) for p in profiles if p.get(field)] for label, field in FIELDS})
    kit.good("Google enumeration completed!")
    return profiles


def attack(web):
    googlenum(web)
