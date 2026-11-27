#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""XPath injection scanner."""

from __future__ import annotations

from core.methods import inject
from core.methods import modkit as kit
from core.methods import webinj
from core.methods.print import pvln
from files.signaturedb.xpatherror_signatures import XPATH_ERRORS

info = ("Finds XPath injection. Error-based: quote/bracket-breaking payloads must make an "
        "XPath engine error appear (.NET, Java/Xalan/Saxon, libxml2/PHP, lxml...) that "
        "neither the original value nor a random value produce. Boolean-based: on a stable "
        "page that depends on the parameter, a condition using XPath-only functions "
        "(count(/*)=1, string-length) must reproduce the original page while its false twin "
        "must not -- SQL injection does not trigger it.")
searchinfo = "XPATH Injection Scanner"
properties = {
    **inject.OPTIONS,
    **webinj.COOKIE_OPTION,
    "DICT": ["Expression-breaking payload list (default: files/payload-db/xpath_payloads.lst)", ""],
}

DEFAULT_DICT = "files/payload-db/xpath_payloads.lst"
SIGNATURES = webinj.compile_signatures(XPATH_ERRORS)

# XPath-only functions: in SQL these are syntax errors, so TRUE ~ FALSE there
PAIRS = (
    ("{v}' and count(/*)=1 and 'a'='a", "{v}' and count(/*)=0 and 'a'='a"),
    ('{v}" and count(/*)=1 and "a"="a', '{v}" and count(/*)=0 and "a"="a'),
    ("{v} and count(/*)=1", "{v} and count(/*)=0"),
    ("{v}' and string-length(name(/*))>0 and 'a'='a", "{v}' and string-length(name(/*))=0 and 'a'='a"),
)


def check(point, s, payloads):
    return webinj.syntax_check(point, s, SIGNATURES, payloads, PAIRS, "XPath injection")


def xpathi(web):
    pvln("xpath Injection")
    record = kit.Recorder(web, kit.CRITICAL, "xpathi")
    points = inject.discover(web, properties)
    if not points:
        record("No injection points found.")
        return []
    payloads = inject.payloads(properties, DEFAULT_DICT)
    s = webinj.session(properties)
    findings = inject.scan(points, lambda p: check(p, s, payloads))
    inject.report(findings, record, "No XPath injection found.")
    return findings


def attack(web):
    xpathi(web)
