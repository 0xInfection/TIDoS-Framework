#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Wayback Machine lookup -- passive recon."""

from __future__ import annotations

import requests

from core.methods import modkit as kit
from core.methods.print import posintpas

info = "Find past versions of a website using the Wayback Machine."
searchinfo = "Wayback Machine Lookup"
properties = {
    "START": ["Year from when results to be fetched", ""],
    "END": ["Year till when results to be fetched", ""],
    "LIMIT": ["No. of results", ""],
}

CDX = "https://web.archive.org/cdx/search/cdx"


def _overloaded(e) -> bool:
    status = getattr(getattr(e, "response", None), "status_code", 0) or 0
    return isinstance(e, requests.Timeout) or status >= 500


def snapshots(host: str, start: str, end: str, limit: int) -> list[tuple[str, str]] | None:
    """[(timestamp, original-url), ...] sorted by date, None on failure."""
    params = {"url": host, "matchType": "domain", "limit": limit, "output": "json",
              "fl": "timestamp,original"}
    if start:
        params["from"] = start
    if end:
        params["to"] = end
    try:
        resp = kit.http(timeout=60).get(CDX, params=params)
        resp.raise_for_status()
        rows = resp.json() if resp.text.strip() else []
    except (requests.RequestException, ValueError) as e:
        kit.bad(f"Wayback Machine request failed: {e}")
        if _overloaded(e):
            kit.warn("The CDX API is slow on large domains; try without START/END or a lower LIMIT.")
        return None
    unique = dict.fromkeys(tuple(r) for r in rows[1:])  # first row is the header
    return sorted(unique, key=lambda r: r[0])


def webarchive(web):
    posintpas("wayback machine lookup")
    host = kit.host(web)
    start = kit.option(properties, "START", "Year from when results to be fetched (eg. 2010)")
    end = kit.option(properties, "END", "Year till when results to be fetched (eg. 2017)")
    limit = kit.integer(properties, "LIMIT", "No. of results", 50)

    kit.info(f"Querying web.archive.org for {host} ...")
    rows = snapshots(host, start, end, limit)
    if rows is None:
        return []
    if not rows:
        kit.bad("No results found!")
        return []

    kit.good(f"Found {len(rows)} snapshot(s) at web.archive.org:")
    lines = []
    for stamp, original in rows:
        line = f"{stamp[:4]}/{stamp[4:6]}/{stamp[6:8]}  {original}  (https://web.archive.org/web/{stamp}/{original})"
        kit.bullet(line)
        lines.append(line)
    kit.Recorder(web, kit.PASSIVE, "webarchive")(lines)
    return lines


def attack(web):
    webarchive(web)
