#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Pastebin posts -- passive recon (Google dork against pastebin.com)."""

from core.methods import modkit as kit
from core.methods.google import Blocked, blocked_hint, search
from core.methods.print import posintpas

info = "Find Pastebin posts."
searchinfo = "Find Pastebin posts."
properties = {
    "LIMIT": ["Maximum number of results", ""],
}


def pastebin(web):
    posintpas("pastebin posts")
    site = kit.domain(web)
    limit = kit.integer(properties, "LIMIT", "Maximum number of results", 30)

    kit.info(f"Finding Pastebin posts mentioning {site}...")
    try:
        posts = search(f'site:pastebin.com intext:"{site}"', limit)
    except Blocked:
        blocked_hint()
        return []
    except Exception as e:
        kit.bad(f"Search failed: {e}")
        return []

    posts = [p for p in posts if "pastebin.com" in p]
    if not posts:
        kit.bad("No Pastebin posts found.")
        return []
    for post in posts:
        kit.found("Post found", post)
    kit.good(f"{len(posts)} Pastebin post(s) found.")
    kit.Recorder(web, kit.PASSIVE, "pastebin")(posts)
    return posts


def attack(web):
    pastebin(web)
