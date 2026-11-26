#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Email hunter -- information disclosure."""

import re

from core.methods import harvest
from core.methods import modkit as kit
from core.methods.print import pleak
from files.signaturedb.infodisc_signatures import EMAIL_HARVESTER_SIGNATURE, EMAIL_IGNORE_SIGNATURE

info = "Finds email addresses disclosed in the target's pages."
searchinfo = "Email hunter"
properties = {
    "CRAWL": ["Also scan same-host pages linked from the target (y/n)", ""],
    **kit.AUTH_OPTIONS,
}

PATTERN = re.compile(EMAIL_HARVESTER_SIGNATURE)
IGNORE = re.compile(EMAIL_IGNORE_SIGNATURE)


def extract(body):
    for m in PATTERN.finditer(body):
        address = m.group(0).lower()
        if not IGNORE.search(address):
            yield address


def emailext(web):
    pleak("email info harvester")
    return harvest.run(web, properties, noun="email addresses", lvl2="emailext", extract=extract)


def attack(web):
    emailext(web)
