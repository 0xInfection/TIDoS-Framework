#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Reverse DNS lookup -- passive recon (HackerTarget API)."""

from __future__ import annotations

import re
import socket

from core.methods import modkit as kit
from core.methods.print import posintpas

info = "Perform a reverse DNS lookup using free API."
searchinfo = "Reverse DNS Lookup"
properties = {}


def revdns(web):
    posintpas("reverse dns lookup")
    record = kit.Recorder(web, kit.PASSIVE, "revdns")
    ip = kit.resolve(web)
    if not ip:
        kit.bad(f"Could not resolve {kit.host(web)}.")
        return []
    kit.info(f"Looking up reverse DNS (PTR) records of {ip} ...")
    result = kit.hackertarget("reversedns", ip)
    if result is None:
        kit.info("Falling back to a local PTR lookup ...")
        try:
            result = f"{ip} {socket.gethostbyaddr(ip)[0]}"
        except OSError:
            result = ""
    pairs = [re.split(r"[\s,]+", line.strip(), maxsplit=1) for line in result.splitlines()]
    pairs = [(p[0], p[1].strip()) for p in pairs if len(p) == 2]
    if not pairs:
        kit.bad("No result found!")
        record("No result found.")
        return []
    for addr, name in pairs:
        kit.found("Received", f"{addr} => {name}")
    record(result)
    return pairs


def attack(web):
    revdns(web)
