#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""
Small dnspython wrappers for the DNS misconfiguration modules
(mailspoof, zone, ssscript, cloudflaremisc).

Lookups return empty lists instead of raising on NXDOMAIN / no answer /
timeouts, so callers only need to handle "nothing found". DNS traffic
never goes through Tor: call warn_tor() before using these.
"""

from __future__ import annotations

import dns.exception
import dns.name
import dns.resolver

import core.variables as variables
from core.methods import modkit as kit

LIFETIME = 8.0


def warn_tor() -> None:
    if variables.tor:
        kit.warn("DNS queries are sent directly (not through Tor).")


def resolver(nameserver: str = "") -> dns.resolver.Resolver:
    r = dns.resolver.Resolver()
    r.lifetime = LIFETIME
    r.timeout = min(LIFETIME, 4.0)
    if nameserver:
        r.nameservers = [nameserver]
    return r


def query(name: str, rdtype: str, res: dns.resolver.Resolver | None = None) -> list:
    """Answer rdata list; [] for NXDOMAIN, no data, timeouts or bad names."""
    try:
        return list((res or resolver()).resolve(name, rdtype, search=False))
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers,
            dns.resolver.YXDOMAIN, dns.exception.Timeout, dns.name.LabelTooLong,
            dns.name.EmptyLabel, dns.name.NameTooLong, ValueError):
        return []


def txt(name: str) -> list[str]:
    """TXT strings of a name (multi-string records joined, as SPF/DMARC require)."""
    out = []
    for rr in query(name, "TXT"):
        out.append(b"".join(rr.strings).decode("utf-8", "replace"))
    return out


def addresses(name: str, ipv6: bool = True) -> list[str]:
    ips = [rr.address for rr in query(name, "A")]
    if ipv6:
        ips += [rr.address for rr in query(name, "AAAA")]
    return ips


def ns(domain: str) -> list[str]:
    return sorted({str(rr.target).rstrip(".").lower() for rr in query(domain, "NS")})


def mx(domain: str) -> list[str]:
    return [str(rr.exchange).rstrip(".").lower()
            for rr in sorted(query(domain, "MX"), key=lambda r: r.preference)
            if str(rr.exchange) not in (".", "")]
