#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""
SPF / DMARC parsing and evaluation (RFC 7208 / RFC 7489), used by the
mailspoof and cloudflaremisc modules.

Lookups go through a `get_txt(name) -> list[str]` callable so the logic can
be tested with canned records (core.methods.dnsmisc.txt in production).
"""

from __future__ import annotations

import ipaddress
from dataclasses import dataclass, field
from typing import Callable

LOOKUP_LIMIT = 10
LOOKUP_TERMS = ("include", "a", "mx", "ptr", "exists")
QUALIFIERS = "+-~?"
ALL_MEANING = {"-": "fail (strict)", "~": "softfail", "?": "neutral", "+": "pass (anyone may send)"}


# --------------------------------------------------------------------------
# SPF
# --------------------------------------------------------------------------

@dataclass
class Spf:
    record: str
    all: str | None = None            # qualifier of the all mechanism, None if absent
    redirect: str | None = None
    includes: list = field(default_factory=list)
    lookups: int = 0                  # DNS-querying terms in this record only
    broad: list = field(default_factory=list)
    ptr: bool = False


def spf_records(txts: list[str]) -> list[str]:
    return [t for t in txts if t.lower() == "v=spf1" or t.lower().startswith("v=spf1 ")]


def parse_spf(record: str) -> Spf:
    spf = Spf(record)
    for term in record.split()[1:]:
        low = term.lower()
        if low.startswith("redirect="):
            spf.redirect = term.split("=", 1)[1].rstrip(".")
            spf.lookups += 1
            continue
        if "=" in low.split(":")[0]:
            continue  # other modifiers (exp=...)
        qual = low[0] if low[0] in QUALIFIERS else "+"
        mech = low.lstrip(QUALIFIERS)
        name = mech.split(":")[0].split("/")[0]
        if name == "all":
            spf.all = qual
        elif name in LOOKUP_TERMS:
            spf.lookups += 1
            if name == "include" and ":" in mech:
                spf.includes.append(term.split(":", 1)[1].rstrip("."))
            if name == "ptr":
                spf.ptr = True
        elif name in ("ip4", "ip6") and qual == "+" and ":" in mech:
            try:
                net = ipaddress.ip_network(mech.split(":", 1)[1], strict=False)
            except ValueError:
                continue
            if (net.version == 4 and net.prefixlen < 16) or (net.version == 6 and net.prefixlen < 32):
                spf.broad.append(str(net))
    return spf


def count_lookups(domain: str, get_txt: Callable[[str], list[str]], seen=None, depth=0) -> int:
    """Total DNS lookups needed to evaluate a domain's SPF (RFC 7208 4.6.4)."""
    seen = set() if seen is None else seen
    if domain in seen or depth > 12:
        return 0
    seen.add(domain)
    records = spf_records(get_txt(domain))
    if len(records) != 1:
        return 0
    spf = parse_spf(records[0])
    total = spf.lookups
    for inc in spf.includes + ([spf.redirect] if spf.redirect else []):
        total += count_lookups(inc, get_txt, seen, depth + 1)
    return total


def analyze_spf(domain: str, get_txt: Callable[[str], list[str]]) -> tuple[str, list[str]]:
    """(strength, notes). strength: missing | invalid | weak | softfail | strict."""
    notes = []
    records = spf_records(get_txt(domain))
    if not records:
        return "missing", ["no SPF record"]
    if len(records) > 1:
        return "invalid", [f"{len(records)} SPF records (permerror: receivers treat it as no SPF)"]
    spf = parse_spf(records[0])
    notes.append(f"record: {spf.record}")
    qual = spf.all
    hops = 0
    while qual is None and spf.redirect and hops < 5:
        target = spf.redirect
        recs = spf_records(get_txt(target))
        if len(recs) != 1:
            return "invalid", notes + [f"redirect={target} has no usable SPF record (permerror)"]
        notes.append(f"redirect={target}: {recs[0]}")
        spf = parse_spf(recs[0])
        qual = spf.all
        hops += 1
    lookups = count_lookups(domain, get_txt)
    if lookups > LOOKUP_LIMIT:
        notes.append(f"{lookups} DNS lookups (> {LOOKUP_LIMIT}: permerror, SPF is ignored)")
    if spf.broad:
        notes.append("very broad ranges authorised: " + ", ".join(spf.broad))
    if spf.ptr:
        notes.append("uses the deprecated 'ptr' mechanism")
    if lookups > LOOKUP_LIMIT:
        return "invalid", notes
    if qual is None:
        notes.append("no 'all' mechanism: unlisted senders get neutral")
        return "weak", notes
    notes.append(f"all qualifier: {qual}all = {ALL_MEANING[qual]}")
    if qual in "+?":
        return "weak", notes
    if spf.broad:
        return "weak", notes
    return ("strict" if qual == "-" else "softfail"), notes


# --------------------------------------------------------------------------
# DMARC
# --------------------------------------------------------------------------

def parse_dmarc(record: str) -> dict[str, str] | None:
    tags = {}
    for part in record.split(";"):
        k, sep, v = part.strip().partition("=")
        if sep:
            tags.setdefault(k.strip().lower(), v.strip())
    if tags.get("v", "").upper() != "DMARC1" or not record.strip().lower().startswith("v"):
        return None
    return tags


def dmarc_records(txts: list[str]) -> list[str]:
    return [t for t in txts if t.strip().lower().replace(" ", "").startswith("v=dmarc1")]


def analyze_dmarc(domain: str, org: str, get_txt: Callable[[str], list[str]]) -> tuple[str, list[str]]:
    """(policy, notes). policy: missing | invalid | none | partial | quarantine | reject."""
    notes = []
    records = dmarc_records(get_txt(f"_dmarc.{domain}"))
    subdomain = False
    if not records and org and org != domain:
        records = dmarc_records(get_txt(f"_dmarc.{org}"))
        subdomain = bool(records)
        if records:
            notes.append(f"no record for {domain}, using the organisational record of {org}")
    if not records:
        return "missing", ["no DMARC record"]
    if len(records) > 1:
        return "invalid", [f"{len(records)} DMARC records (receivers ignore DMARC)"]
    tags = parse_dmarc(records[0])
    notes.append(f"record: {records[0]}")
    if tags is None:
        return "invalid", notes + ["malformed record (must start with v=DMARC1)"]
    p = tags.get("p", "").lower()
    if p not in ("none", "quarantine", "reject"):
        # RFC 7489 6.6.3: invalid/missing p= with rua -> treat as none
        notes.append(f"invalid or missing p= ('{p}'), treated as p=none")
        p = "none"
    policy = tags.get("sp", p).lower() if subdomain else p
    if policy not in ("none", "quarantine", "reject"):
        policy = p
    if subdomain:
        notes.append(f"subdomain policy: {policy}")
    elif tags.get("sp", "").lower() == "none" and p != "none":
        notes.append("sp=none: subdomains of the domain can be spoofed")
    pct = tags.get("pct", "100")
    if policy != "none" and pct.isdigit() and int(pct) < 100:
        notes.append(f"pct={pct}: only {pct}% of failing mail gets the policy")
        return "partial", notes
    return policy, notes


# --------------------------------------------------------------------------
# verdict
# --------------------------------------------------------------------------

def verdict(spf: str, dmarc: str) -> tuple[str, str]:
    """(severity, sentence) for an SPF strength / DMARC policy pair."""
    if dmarc in ("reject", "quarantine"):
        if spf in ("missing", "invalid"):
            return "LOW", (f"DMARC p={dmarc} blocks spoofed From: headers (SPF {spf}, so "
                           "legitimate mail relies on DKIM alone)")
        return "OK", f"not spoofable: DMARC p={dmarc} enforced"
    if dmarc == "partial":
        return "MEDIUM", "partially spoofable: DMARC enforced on less than 100% of mail"
    if spf in ("missing", "invalid", "weak"):
        return "HIGH", (f"spoofable: SPF {spf} and DMARC {dmarc}; forged mail from this domain "
                        "passes or is not rejected")
    return "MEDIUM", (f"From: header spoofable: SPF is {spf} but DMARC is {dmarc}, and SPF only "
                      "protects the envelope sender")
