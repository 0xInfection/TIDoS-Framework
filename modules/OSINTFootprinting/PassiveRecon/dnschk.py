#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""DNS record lookup (DNS-over-HTTPS) -- passive recon."""

from __future__ import annotations

from core.methods import modkit as kit
from core.methods.print import posintpas

info = "Lookup the public DNS records of the target's domain (via DNS-over-HTTPS)."
searchinfo = "DNS Lookup Module"
properties = {
    "RESOLVER": ["DNS-over-HTTPS JSON endpoint", ""],
}

DEFAULT_RESOLVER = "https://dns.google/resolve"
TYPES = {"A": 1, "AAAA": 28, "CNAME": 5, "NS": 2, "MX": 15, "TXT": 16, "SOA": 6, "CAA": 257}


def query(session, resolver: str, name: str, rtype: str) -> list[str]:
    resp = session.get(resolver, params={"name": name, "type": rtype},
                       headers={"Accept": "application/dns-json"})
    resp.raise_for_status()
    data = resp.json()
    return [a["data"] for a in data.get("Answer", []) if a.get("type") == TYPES[rtype]]


def dnschk(web):
    posintpas("dns lookup")
    domain = kit.domain(web)
    resolver = kit.option(properties, "RESOLVER", "DoH resolver", DEFAULT_RESOLVER)
    session = kit.http()

    kit.info(f"Looking up DNS records of {domain} via {resolver}...")
    records: dict[str, list[str]] = {}
    for rtype in TYPES:
        try:
            answers = query(session, resolver, domain, rtype)
        except Exception as e:
            kit.bad(f"{rtype} lookup failed: {e}")
            continue
        if not answers:
            continue
        records[rtype] = answers
        kit.good(f"{rtype} Records")
        for a in answers:
            kit.bullet(a)

    # resolve the mail / name servers too, like DNSDumpster's host table
    hosts = {r.split()[-1].rstrip(".") for r in records.get("MX", []) + records.get("NS", [])}
    hosts.discard("")
    host_ips = {}
    for h in sorted(hosts):
        try:
            host_ips[h] = query(session, resolver, h, "A")
        except Exception:
            continue
    if host_ips:
        kit.good("Host Records (A)")
        for h, ips in host_ips.items():
            kit.bullet(f"{h} ({', '.join(ips) or 'no A record'})")

    if not records:
        kit.bad("No standard publicly recorded DNS records found.")
        return {}
    kit.Recorder(web, kit.PASSIVE, "dnschk")(str({**records, "HOST": host_ips}))
    return records


def attack(web):
    dnschk(web)
