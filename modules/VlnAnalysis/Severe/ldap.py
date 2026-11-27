#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""LDAP injection scanner."""

from __future__ import annotations

from core.methods import inject
from core.methods import modkit as kit
from core.methods import webinj
from core.methods.print import pvln
from files.signaturedb.ldaperror_signatures import LDAP_ERRORS

info = ("Finds LDAP injection. Error-based: filter-breaking payloads must make an LDAP "
        "library error appear (JNDI, PHP ldap_*, .NET DirectoryServices, UnboundID, "
        "python-ldap...) that neither the original value nor a random value produce, so "
        "pages that always show such text are not reported. Boolean-based: on a stable page "
        "that depends on the parameter, '<v>)(objectClass=*' must reproduce the original "
        "page while '<v>)(objectClass=<random>' must not.")
searchinfo = "LDAP Injection Scan"
properties = {
    **inject.OPTIONS,
    **webinj.COOKIE_OPTION,
    "DICT": ["Filter-breaking payload list (default: files/payload-db/ldap_payloads.lst)", ""],
}

DEFAULT_DICT = "files/payload-db/ldap_payloads.lst"
SIGNATURES = webinj.compile_signatures(LDAP_ERRORS)


def check(point, s, payloads):
    rnd = inject.marker()
    pairs = [("{v})(objectClass=*", "{v})(objectClass=" + rnd),
             ("{v}*)(objectClass=*", "{v}*)(objectClass=" + rnd)]
    return webinj.syntax_check(point, s, SIGNATURES, payloads, pairs, "LDAP injection")


def ldap(web):
    pvln("ldap Injection")
    record = kit.Recorder(web, kit.CRITICAL, "ldap")
    points = inject.discover(web, properties)
    if not points:
        record("No injection points found.")
        return []
    payloads = inject.payloads(properties, DEFAULT_DICT)
    s = webinj.session(properties)
    findings = inject.scan(points, lambda p: check(p, s, payloads))
    inject.report(findings, record, "No LDAP injection found.")
    return findings


def attack(web):
    ldap(web)
