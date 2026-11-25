#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reverse IP lookup -- passive recon (HackerTarget API)."""

from core.methods import modkit as kit
from core.methods.print import posintpas

info = "Perform a reverse IP lookup using a free API."
searchinfo = "Reverse IP Lookup"
properties = {}

def revip(web):
    posintpas("reverse ip lookup")
    host = kit.host(web)
    record = kit.Recorder(web, kit.PASSIVE, "revip")
    kit.info(f"Looking up sites sharing the IP of {host} ...")
    result = kit.hackertarget("reverseiplookup", host)
    if result is None:
        return []
    sites = result.splitlines()
    if not sites:
        kit.bad("No result found!")
        record("No result found.")
        return []
    for site in sites:
        kit.found("Site", site)
    kit.good(f"{len(sites)} site(s) hosted on the same IP.")
    record(result)
    return sites


def attack(web):
    revip(web)
