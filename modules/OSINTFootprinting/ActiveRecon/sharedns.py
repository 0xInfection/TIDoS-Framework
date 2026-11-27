#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Shared DNS hostnames -- finds other domains served by the target's nameserver."""

from core.methods import modkit as kit
from core.methods.print import posintact

info = ("Looks up the nameservers of the target's domain, then asks the HackerTarget "
        "findshareddns API (free tier, rate limited) which other domains are hosted "
        "on the chosen nameserver. NAMESERVER defaults to the first one found.")
searchinfo = "DNS Shared Hostnames"
properties = {
    "NAMESERVER": ["Nameserver to query for shared hosts (default: first NS of the target)", ""],
}



def nameservers(domain):
    try:
        import dns.resolver
    except ImportError:
        kit.bad("dnspython is required for nameserver lookups (pip install dnspython).")
        return []
    try:
        answer = dns.resolver.resolve(domain, "NS", lifetime=10)
    except Exception as e:
        kit.bad(f"NS lookup for {domain} failed: {type(e).__name__}")
        return []
    return sorted(str(r.target).rstrip(".") for r in answer)


def shared_hosts(ns):
    text = kit.hackertarget("findshareddns", ns)
    return None if text is None else text.splitlines()


def sharedns(web):
    posintact("shared dns hostnames")
    record = kit.Recorder(web, kit.ACTIVE, "sharedns")
    domain = kit.domain(web)

    kit.info(f"Looking up the nameservers of {domain}...")
    servers = nameservers(domain)
    for ns in servers:
        kit.found("Nameserver", ns)

    ns = kit.option(properties, "NAMESERVER", "DNS server to query",
                    servers[0] if servers else "")
    if not ns:
        kit.bad("No nameserver to query.")
        return []

    kit.info(f"Discovering hosts on the same DNS server ({ns})...")
    hosts = shared_hosts(ns)
    if hosts is None:
        return []
    if not hosts:
        kit.bad("No shared DNS nameserver hosts...")
        record("No shared DNS nameserver hosts.")
        return []
    for h in hosts:
        kit.found("Site found", h)
    kit.good(f"{len(hosts)} domains share {ns}")
    record("\n".join(hosts))
    return hosts


def attack(web):
    sharedns(web)
