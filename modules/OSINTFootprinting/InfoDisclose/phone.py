#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Phone Number Harvester -- information disclosure."""

import re

from core.methods import harvest
from core.methods import modkit as kit
from core.methods.print import pleak
from files.signaturedb.infodisc_signatures import PHONE_NUMBER_SIGNATURE

info = "Finds international phone numbers disclosed in the target's pages."
searchinfo = "Phone Number Harvester"
properties = {
    "CRAWL": ["Also scan same-host pages linked from the target (y/n)", ""],
    **kit.AUTH_OPTIONS,
}

PATTERN = re.compile(PHONE_NUMBER_SIGNATURE)


def extract(body):
    for m in PATTERN.finditer(body):
        number = m.group(0).strip()
        digits = sum(ch.isdigit() for ch in number)
        grouped = not number[1:].isdigit()
        # E.164 bounds; an ungrouped run needs a full-length number to
        # stand apart from numeric constants
        if (8 if grouped else 11) <= digits <= 15:
            yield number


def phone(web):
    pleak("phone number harvester")
    return harvest.run(web, properties, noun="phone numbers", lvl2="phone", extract=extract)


def attack(web):
    phone(web)
