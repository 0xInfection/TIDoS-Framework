#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""SQL injection scanner -- error-based, boolean-blind and time-blind."""

from core.methods import inject
from core.methods import modkit as kit
from core.methods import webinj
from core.methods import sqli as engine
from core.methods.print import pvln

info = ("Tests every parameter (PARAM, or the ones found by crawling) for SQL injection: "
        "error-based (MySQL/MariaDB, PostgreSQL, MSSQL, Oracle, SQLite, DB2, Access... error "
        "messages caused by a quote that the balanced payload does not cause), boolean-blind "
        "(true/false condition pairs compared with the baseline) and time-blind (DBMS sleep "
        "functions, confirmed with a zero-delay control and a second delay). Reports a DBMS guess.")
searchinfo = "SQL Injection Scanner"
properties = {
    **inject.OPTIONS,
    **webinj.COOKIE_OPTION,
    "TECHNIQUE": ["Techniques: error, boolean, time or all, comma separated (default error,boolean)", ""],
    "DELAY": ["Sleep used by time-based payloads, seconds (default 3; confirmed with twice that)", ""],
}

DEFAULT_DELAY = 3.0


def sqli(target):
    pvln("sql !njection")
    chosen = kit.option(properties, "TECHNIQUE", "Techniques (error,boolean,time,all)", "error,boolean")
    techniques = engine.parse_techniques(chosen)
    if not techniques:
        kit.bad(f"Unknown TECHNIQUE '{chosen}'. Use error, boolean, time or all.")
        return
    delay = DEFAULT_DELAY
    if "time" in techniques:
        delay = max(1.0, kit.number(properties, "DELAY", "Sleep delay in seconds", DEFAULT_DELAY))

    points = inject.discover(target, properties)
    if not points:
        return
    kit.info(f"Techniques: {', '.join(techniques)}" + (f" (delay {delay:g}s)" if "time" in techniques else ""))
    session = webinj.session(properties, timeout=15)
    findings = inject.scan(points, engine.make_check(session, techniques, delay))
    inject.report(findings, kit.Recorder(target, kit.CRITICAL, "sqli"),
                  clean="No SQL injection found.")


def attack(target):
    sqli(target)
