#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Domain contact info (RDAP) -- passive recon."""

from __future__ import annotations

import re

from core.methods import modkit as kit
from core.methods.print import posintpas

info = "Find domain contact info (registrar, registrant, admin/tech/abuse contacts) via RDAP."
searchinfo = "Domain Contact Info"
properties = {}

RDAP = "https://rdap.org/domain/"
VCARD = {"fn": "Name", "org": "Organization", "email": "Email", "tel": "Phone", "adr": "Address"}


def vcard(entity: dict) -> list[tuple[str, str]]:
    """Human-readable (label, value) pairs from an entity's jCard."""
    out = []
    for prop, params, _, value in (entity.get("vcardArray") or [None, []])[1]:
        if prop not in VCARD:
            continue
        if prop == "adr":
            value = (params or {}).get("label") or ", ".join(
                v if isinstance(v, str) else " ".join(v) for v in value if v)
        elif isinstance(value, list):
            value = " ".join(str(v) for v in value if v)
        value = re.sub(r"^(tel|mailto):", "", str(value)).strip()
        if value:
            out.append((VCARD[prop], value))
    return out


def contacts(doc: dict) -> list[tuple[str, list[tuple[str, str]]]]:
    """(roles, vcard) for every entity of an RDAP document, nested ones included."""
    found = []
    stack = list(doc.get("entities") or [])
    while stack:
        ent = stack.pop(0)
        card = vcard(ent)
        if card:
            found.append((", ".join(ent.get("roles") or ["contact"]), card))
        stack.extend(ent.get("entities") or [])
    return found


def fetch(session, url: str) -> dict | None:
    try:
        resp = session.get(url)
    except Exception as e:
        kit.bad(f"RDAP request failed: {e}")
        return None
    if resp.status_code == 404:
        return None
    try:
        return resp.json()
    except ValueError:
        kit.bad(f"Unexpected RDAP answer (HTTP {resp.status_code}).")
        return None


def getconinfo(web):
    posintpas("domain contact info")
    domain = kit.domain(web)
    session = kit.http(timeout=20, headers={"Accept": "application/rdap+json"})

    kit.info(f"Looking up contact info for {domain} via RDAP...")
    doc = fetch(session, RDAP + domain)
    record = kit.Recorder(web, kit.PASSIVE, "getconinfo")
    if not doc or "errorCode" in doc:
        kit.bad(f"Did not find any info about domain {domain}.")
        record(f"Did not find any info about domain {domain}")
        return []

    found = contacts(doc)
    # thin registries (.com/.net) keep the real contacts at the registrar
    for link in doc.get("links") or []:
        if link.get("rel") == "related" and "rdap" in link.get("type", "rdap"):
            extra = fetch(session, link["href"])
            if extra:
                found += [c for c in contacts(extra) if c not in found]

    events = {e.get("eventAction"): e.get("eventDate") for e in doc.get("events") or []}
    kit.good(f"Found domain info for {domain}!")
    kit.kv_table([("Domain", doc.get("ldhName", domain).lower()),
                  ("Status", ", ".join(doc.get("status") or [])),
                  ("Registered", events.get("registration")),
                  ("Expires", events.get("expiration")),
                  ("Nameservers", ", ".join(ns.get("ldhName", "").lower()
                                            for ns in doc.get("nameservers") or []))])
    lines = []
    for roles, card in found:
        kit.good(roles.title())
        kit.kv_table(card, indent=5)
        lines += [f"{roles}: {k}: {v}" for k, v in card]
    if not found:
        kit.warn("No contact entities published (likely redacted for privacy).")
    record(lines or f"No public contacts for {domain}")
    kit.good("Public Contact Info Module Completed!")
    return found


def attack(web):
    getconinfo(web)
