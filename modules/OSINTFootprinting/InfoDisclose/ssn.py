#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""SSN Hunter -- information disclosure."""

import re

from core.methods import harvest
from core.methods import modkit as kit
from core.methods.print import pleak
from files.signaturedb.infodisc_signatures import SOCIAL_SECURITY_SIGNATURE

info = "Finds US social security numbers disclosed in the target's pages."
searchinfo = "SSN Hunter"
properties = {
    "CRAWL": ["Also scan same-host pages linked from the target (y/n)", ""],
    **kit.AUTH_OPTIONS,
}

PATTERN = re.compile(SOCIAL_SECURITY_SIGNATURE)


def extract(body):
    return (m.group(0) for m in PATTERN.finditer(body))


def ssn(web):
    pleak("ssn disclosure")
    return harvest.run(web, properties, noun="social security numbers", lvl2="ssn", extract=extract)


def attack(web):
    ssn(web)
