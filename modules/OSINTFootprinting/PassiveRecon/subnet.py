#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Subnet enumeration -- passive recon (HackerTarget subnet calculator)."""

from core.methods import modkit as kit
from core.methods.print import posintpas

info = "Enumerate subnets of the target's network."
searchinfo = "Subnet Enumeration"
properties = {
    "MASK": ["CIDR prefix length of the network to calculate (e.g. 24; none = host only)", ""],
}


def subnet(web):
    posintpas("subnet enumeration")
    record = kit.Recorder(web, kit.PASSIVE, "subnet")
    host = kit.host(web)
    mask = kit.option(properties, "MASK", "CIDR prefix length (e.g. 24)", "")
    query = host
    if mask:  # the API only takes CIDRs of IP addresses
        ip = kit.resolve(web)
        if not ip:
            kit.bad(f"Could not resolve {host}.")
            return {}
        query = f"{ip}/{mask.lstrip('/')}"

    kit.info(f"Getting subnet class info for {query} ...")
    result = kit.hackertarget("subnetcalc", query)
    if result is None:
        return {}
    rows = dict(line.split("=", 1) for line in result.splitlines() if "=" in line)
    rows = {k.strip(): v.strip() for k, v in rows.items()}
    if not rows:
        kit.bad("No results found!")
        record("No results found.")
        return {}
    kit.kv_table(rows.items())
    record(result)
    return rows


def attack(web):
    subnet(web)
