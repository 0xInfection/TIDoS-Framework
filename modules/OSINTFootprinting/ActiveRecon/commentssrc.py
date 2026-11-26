#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Comment scraper -- HTML comments left in the target's pages."""

from __future__ import annotations

import re

from core.methods import harvest
from core.methods import modkit as kit
from core.methods.print import posintact

info = ("This module hunts down HTML comments in the source code of the target page "
        "and of the same-host pages it links to.")
searchinfo = "Comment Scraper"
properties = {
    "CRAWL": ["Also scan same-host pages linked from the target (y/n)", ""],
    **kit.AUTH_OPTIONS,
}

COMMENT = re.compile(r"<!--(.*?)-->", re.S)


def extract(body: str) -> list[str]:
    """Unique, whitespace-normalised, non-empty comments of a page."""
    comments = (" ".join(c.split()) for c in COMMENT.findall(body))
    return list(dict.fromkeys(c for c in comments if c))


def commentssrc(web):
    posintact("comment scraper")
    deep = kit.flag(properties, "CRAWL", "Also scan pages linked from the target?", True)
    pages = harvest.crawl(web, deep, headers=kit.request_headers(properties))
    record = kit.Recorder(web, kit.ACTIVE, "commentssrc")

    everything = {}
    for page, body in pages.items():
        comments = extract(body)
        if not comments:
            continue
        kit.found("Comments on page", page)
        for c in comments:
            kit.bullet(c)
        everything.update(dict.fromkeys(comments))

    if everything:
        kit.good(f"{len(everything)} unique comment(s) across {len(pages)} page(s)")
        record(list(everything))
    elif pages:
        kit.bad("No comments found in source code!")
        record("No comments found in source code.")
    kit.good("Comments scraping done!")
    return list(everything)


def attack(web):
    commentssrc(web)
