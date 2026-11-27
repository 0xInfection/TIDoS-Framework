#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Error hunter -- information disclosure."""

import re

from core.methods import harvest
from core.methods import modkit as kit
from core.methods.print import pleak
from files.signaturedb.commonerror_signatures import SIGNATURES

info = ("Finds server-side error messages, debug pages and stack traces leaking "
        "in the target's pages, and names the technology behind them (PHP, "
        "Laravel, ASP.NET, Java/Spring/Tomcat, Django, Flask, Rails, Node.js, "
        "Go, and MySQL/PostgreSQL/MSSQL/Oracle/SQLite database errors).")
searchinfo = "Error hunter"
properties = {
    "CRAWL": ["Also scan same-host pages linked from the target (y/n)", ""],
    **kit.AUTH_OPTIONS,
}

COMPILED = [(tech, re.compile(rx, re.I | re.S)) for tech, rx in SIGNATURES]


BLOCK_END = re.compile(r"\n|<br\s*/?>|</(?:p|div|pre|h\d|title|li|td|tr|table|body)>", re.I)


def _snippet(body: str, start: int, width: int = 110) -> str:
    """The error message starting at `start`: up to the end of its line or
    block element, tags stripped, single-spaced."""
    chunk = body[start:start + 400]
    end = BLOCK_END.search(chunk, 1)
    text = re.sub(r"<[^>]+>", "", chunk[:end.start()] if end else chunk)
    text = " ".join(text.split())
    return text if len(text) <= width else text[:width - 3] + "..."


def extract(body):
    seen = set()
    for tech, rx in COMPILED:
        if tech in seen:
            continue  # one finding per technology per page is enough
        m = rx.search(body)
        if m:
            seen.add(tech)
            yield f"{tech}: {_snippet(body, m.start())}"


def errors(web):
    pleak("error hunter")
    return harvest.run(web, properties, noun="error signatures", lvl2="errors", extract=extract)


def attack(web):
    errors(web)
