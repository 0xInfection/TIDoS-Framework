#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Dig DNS lookup -- passive recon."""

from core.methods import modkit as kit
from core.methods.print import posintpas

info = ("Queries the target's DNS records with the system `dig` tool. TYPE selects "
        "the record type (A, AAAA, MX, NS, TXT, SOA, ANY, ...).")
searchinfo = "Dig DNS lookup"
properties = {
    "TYPE": ["DNS record type to query (A, AAAA, MX, NS, TXT, ANY, ...)", ""],
}


def dig(target):
    posintpas("dig lookup")
    name = kit.host(target)
    rtype = kit.option(properties, "TYPE", "Record type", "A").upper()
    if not name or name.startswith("-") or not rtype.isalnum():
        kit.bad(f"Refusing to dig '{name}' / type '{rtype}'.")
        return ""

    kit.info(f"Running dig {name} {rtype}...")
    out = kit.command(["dig", name, rtype], timeout=60)
    if out is None:
        return ""
    data = out.replace("<<", "").replace(">>", "")
    print(data)
    kit.Recorder(target, kit.PASSIVE, "dig")(data)
    return data


def attack(web):
    dig(web)
