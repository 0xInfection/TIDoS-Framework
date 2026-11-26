#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""WhoIS lookup -- passive recon (RDAP, the JSON successor of WhoIS)."""

from __future__ import annotations

import requests

from core.methods import modkit as kit
from core.methods.print import posintpas

info = "Perform a WhoIS lookup on the target (domain or IP, via the public RDAP bootstrap at rdap.org)."
searchinfo = "WhoIS Lookup"
properties = {}

RDAP = "https://rdap.org"


def _vcard(entity: dict) -> str:
    """Display name / org / email of an RDAP entity."""
    fields = {}
    for item in (entity.get("vcardArray") or [None, []])[1]:
        if item[0] in ("fn", "org", "email") and item[3]:
            value = item[3]
            fields.setdefault(item[0], " ".join(value) if isinstance(value, list) else str(value))
    return " / ".join(fields.values()) or entity.get("handle", "")


def _entities(entities: list, out: list) -> None:
    for ent in entities or []:
        name = _vcard(ent)
        if name:
            out.append((", ".join(ent.get("roles", [])).title() or "Entity", name))
        _entities(ent.get("entities"), out)


def summarize(data: dict) -> list[tuple[str, str]]:
    rows = [
        ("Name", data.get("ldhName") or data.get("name")),
        ("Handle", data.get("handle")),
        ("Range", f"{data['startAddress']} - {data['endAddress']}" if data.get("startAddress") else ""),
        ("Type", data.get("type")),
        ("Country", data.get("country")),
        ("Status", ", ".join(data.get("status", []))),
    ]
    rows += [(e.get("eventAction", "").capitalize(), e.get("eventDate"))
             for e in data.get("events", []) if "rdap" not in e.get("eventAction", "").lower()]
    rows += [("Name server", ns.get("ldhName", "").lower()) for ns in data.get("nameservers", [])]
    _entities(data.get("entities"), rows)
    return list(dict.fromkeys((k, str(v)) for k, v in rows if v))


def whoischeckup(web):
    posintpas("whois lookup")
    host = kit.host(web)
    query = f"ip/{host}" if kit.is_ip(host) else f"domain/{kit.domain(web)}"
    kit.info(f"Looking up WhoIS (RDAP) information for {query.split('/', 1)[1]} ...")
    try:
        resp = kit.http(timeout=30, headers={"Accept": "application/rdap+json"}).get(f"{RDAP}/{query}")
        if resp.status_code == 404:
            kit.bad("No RDAP record found (unregistered domain or TLD without RDAP).")
            return []
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError) as e:
        kit.bad(f"RDAP lookup failed: {e}")
        return []

    rows = summarize(data)
    if not rows:
        kit.bad("Empty RDAP record.")
        return []
    kit.kv_table(rows)
    kit.Recorder(web, kit.PASSIVE, "whoischeckup")([f"{k}: {v}" for k, v in rows])
    return rows


def attack(web):
    whoischeckup(web)
