#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Internal IP hunter -- information disclosure."""

import re

from core.methods import harvest
from core.methods import modkit as kit
from core.methods.print import pleak
from files.signaturedb.infodisc_signatures import INTERNAL_IP_SIGNATURE

info = "Finds private/internal IP addresses (RFC 1918, loopback, link-local) disclosed in the target's pages."
searchinfo = "Internal IP hunter"
properties = {
    "CRAWL": ["Also scan same-host pages linked from the target (y/n)", ""],
    **kit.AUTH_OPTIONS,
}

PATTERN = re.compile(INTERNAL_IP_SIGNATURE)


def extract(body):
    return (m.group(0) for m in PATTERN.finditer(body))


def internalip(web):
    pleak("internal ip disclosure")
    return harvest.run(web, properties, noun="internal IPs", lvl2="internalip", extract=extract)


def attack(web):
    internalip(web)
