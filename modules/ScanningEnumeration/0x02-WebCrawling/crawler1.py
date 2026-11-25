#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Depth 1 crawler -- the target page and its direct links."""

from core.methods import crawler
from core.methods import modkit as kit
from core.methods.print import pscan

info = "Depth 1 Crawler."
searchinfo = "Depth 1 Crawler"
properties = {
    "MAXPAGES": ["Maximum number of pages to fetch (default 200)", ""],
    "INCLUDE_EXTERNAL": ["List off-host links too; they are never followed (y/n)", ""],
    **kit.AUTH_OPTIONS,
}

DEPTH = 1


def crawler1(web):
    pscan("crawler (depth 1)")
    return crawler.run(web, properties, DEPTH, "crawler1")


def attack(web):
    crawler1(web)
