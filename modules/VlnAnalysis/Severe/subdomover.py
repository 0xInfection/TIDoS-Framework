#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Subdomain takeover scanner."""

from __future__ import annotations

import os
import re
from concurrent.futures import ThreadPoolExecutor

import core.variables as variables
from core.methods import modkit as kit
from core.methods import takeover
from core.methods.print import pvln

info = ("Finds subdomain takeovers. Subdomains come from SUBDOM (single mode), the list "
        "saved by the Subdomain Gatherer module, passive sources (crt.sh, HackerTarget) and "
        "optionally a DNS bruteforce. Each CNAME chain is resolved and matched against ~50 "
        "provider fingerprints (can-i-take-over-xyz): a takeover is reported only when the "
        "CNAME points at the provider AND its unclaimed-resource page is served, or the CNAME "
        "dangles (NXDOMAIN) for providers where that is the signal, or it dangles into an "
        "unregistered domain. DNS queries do not go through Tor.")
searchinfo = "Subdomain Takeover Module"
properties = {
    "SUBDOM": ["Subdomain to check in single mode (empty: enumerate the domain)", ""],
    "PASSIVE": ["Enumerate with passive sources: crt.sh, HackerTarget (y/n, default y)", ""],
    "BRUTE": ["Also bruteforce subdomains over DNS (y/n, default n)", ""],
    "WORDLIST": ["Wordlist for BRUTE (default: files/fuzz-db/subdomain_paths.lst)", ""],
}

DEFAULT_WORDLIST = "files/fuzz-db/subdomain_paths.lst"


def saved_list(web) -> set[str]:
    """Subdomains saved earlier by the OSINT Subdomain Gatherer, if any."""
    stem = re.sub(r"[^A-Za-z0-9._-]", "_", kit.host(web)) or "target"   # as kit.logdir()
    path = os.path.join("tmp", "logs", f"{stem}-logs", f"{stem}-subdomains.lst")
    if not os.path.isfile(path):
        return set()
    names = set(kit.wordlist(path))
    kit.info(f"Loaded {len(names)} subdomains from {path}")
    return names


def enumerate_subdomains(web, domain: str) -> list[str]:
    from modules.OSINTFootprinting.ActiveRecon import subdom as gatherer
    names = {kit.host(web)} | saved_list(web)
    if kit.flag(properties, "PASSIVE", "Query passive sources (crt.sh, HackerTarget)", True):
        names |= gatherer.passive(domain)
    if kit.flag(properties, "BRUTE", "Bruteforce subdomains over DNS", False):
        labels = kit.wordlist(kit.option(properties, "WORDLIST", "Subdomain wordlist", DEFAULT_WORDLIST))
        names |= set(gatherer.bruteforce(domain, labels))
    names = {n.strip().lower().rstrip(".") for n in names}
    return sorted(n for n in names if n == domain or n.endswith("." + domain))


def subdomover(web):
    pvln("subdomain takeover")
    record = kit.Recorder(web, kit.CRITICAL, "subdomover")
    if variables.tor:
        kit.warn("Tor is on, but DNS lookups are made directly (dnspython bypasses Tor).")

    single = kit.option(properties, "SUBDOM", "Subdomain to check (enter to enumerate the domain)", "")
    if single:
        subs = [single.strip().lower().split("://")[-1].split("/")[0]]
    else:
        domain = kit.domain(web)
        if kit.is_ip(domain):
            kit.bad("Target is an IP address; set SUBDOM or use a domain name.")
            record("Target is an IP address; no subdomains to check.")
            return []
        subs = enumerate_subdomains(web, domain)
    if not subs:
        kit.bad("No subdomains to check.")
        record("No subdomains to check.")
        return []

    kit.info(f"Checking {len(subs)} subdomain(s) for takeover...")
    workers = max(1, min(variables.processes, len(subs), 32))
    findings, notes = [], []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for res in pool.map(takeover.check, subs):
            for f in res.findings:
                kit.found(f"Takeover ({f.service}, {f.confidence})", f.subdomain)
                kit.bullet(f.evidence, 6)
            findings += res.findings
            notes += res.notes

    print()
    for n in notes:
        kit.warn(n)
    if not findings:
        kit.bad(f"No subdomain takeover found ({len(subs)} checked).")
        record([f"No subdomain takeover found ({len(subs)} checked)."] + notes)
        return []
    kit.good(f"{len(findings)} takeover candidate(s):")
    for f in findings:
        kit.bullet(f)
    record([str(f) for f in findings] + notes)
    return findings


def attack(web):
    subdomover(web)
