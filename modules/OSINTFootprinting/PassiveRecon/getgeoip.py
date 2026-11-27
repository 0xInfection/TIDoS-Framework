#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""GeoIP lookup (HackerTarget) -- passive recon."""

import socket

from core.methods import modkit as kit
from core.methods.print import posintpas

info = "Find out where the target server is located."
searchinfo = "GeoIP Lookup"
properties = {}



def getgeoip(web):
    posintpas("geoip lookup")
    name = kit.host(web)
    try:
        ip = name if kit.is_ip(name) else socket.gethostbyname(name)
    except (socket.gaierror, UnicodeError) as e:
        kit.bad(f"Could not resolve {name}: {e}")
        return {}

    kit.info(f"Looking up the GeoIP location of {name} ({ip})...")
    text = kit.hackertarget("geoip", ip)
    if text is None:
        return {}
    pairs = [l.split(":", 1) for l in text.splitlines() if ":" in l]
    if not pairs:
        kit.bad("No GeoIP data returned.")
        return {}

    result = {k.strip(): v.strip() for k, v in pairs}
    kit.good("GeoIP location found:")
    for k, v in result.items():
        kit.found(k, v)
    kit.Recorder(web, kit.PASSIVE, "getgeoip")(text)
    return result


def attack(web):
    getgeoip(web)
