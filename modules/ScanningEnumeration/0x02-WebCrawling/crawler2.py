#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Depth 2 crawler -- the target page and pages up to two clicks away."""

from core.methods import crawler
from core.methods import modkit as kit
from core.methods.print import pscan

info = "Depth 2 Crawler."
searchinfo = "Depth 2 Crawler"
properties = {
    "MAXPAGES": ["Maximum number of pages to fetch (default 200)", ""],
    "INCLUDE_EXTERNAL": ["List off-host links too; they are never followed (y/n)", ""],
    **kit.AUTH_OPTIONS,
}

DEPTH = 2


def crawler2(web):
    pscan("crawler (depth 2)")
    return crawler.run(web, properties, DEPTH, "crawler2")


def attack(web):
    crawler2(web)
