#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IP history lookup (ViewDNS) -- passive recon."""

from __future__ import annotations

from bs4 import BeautifulSoup

from core.methods import modkit as kit
from core.methods.print import posintpas

info = "Display the history of the target's IP (via ViewDNS.info)."
searchinfo = "IP History lookup"
properties = {}

WEB = "https://viewdns.info/iphistory/"
API = "https://api.viewdns.info/iphistory/"


def from_page(session, domain: str) -> list[dict] | None:
    """Scrape the public page; None when it is unavailable (Cloudflare, etc.)."""
    resp = session.get(WEB, params={"domain": domain})
    if resp.status_code != 200:
        return None
    table = BeautifulSoup(resp.text, "lxml").find("table", attrs={"border": "1"})
    if table is None:
        return None
    rows = []
    for tr in table.find_all("tr")[1:]:
        td = [c.get_text(strip=True) for c in tr.find_all("td")]
        if len(td) >= 4:
            rows.append({"ip": td[0], "owner": td[2], "last": td[3]})
    return rows


def from_api(session, domain: str, key: str) -> list[dict] | None:
    data = session.get(API, params={"domain": domain, "apikey": key, "output": "json"}).json()
    records = (data.get("response") or {}).get("records")
    if records is None:
        kit.bad(f"ViewDNS API error: {data.get('response') or data}")
        return None
    return [{"ip": r.get("ip", ""), "owner": r.get("owner", ""), "last": r.get("lastseen", "")}
            for r in records]


def iphistory(web):
    posintpas("ip history")
    domain = kit.host(web)
    session = kit.http(timeout=20)

    kit.info(f"Looking up the IP history of {domain}...")
    try:
        rows = from_page(session, domain)
        if rows is None:
            kit.warn("viewdns.info refused the request (Cloudflare challenge); trying the ViewDNS API...")
            key = kit.apikey("VIEWDNS_API_KEY", quiet=True)
            rows = from_api(session, domain, key) if key else None
    except Exception as e:
        kit.bad(f"Request to ViewDNS failed: {e}")
        return []
    if rows is None:
        kit.bad("IP history is unavailable without a ViewDNS API key.")
        return []
    if not rows:
        kit.bad("No instances of IP history found.")
        return []

    kit.good(f"{len(rows)} instance(s) found:")
    for r in rows:
        kit.found("Instance", f"{r['ip']} => {r['owner']} - ({r['last']})")
    kit.Recorder(web, kit.PASSIVE, "iphistory")(rows)
    return rows


def attack(web):
    iphistory(web)
