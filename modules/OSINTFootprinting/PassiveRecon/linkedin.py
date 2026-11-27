#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""LinkedIn gathering -- passive recon (Google dorks against linkedin.com)."""

from core.methods import modkit as kit
from core.methods.google import Blocked, blocked_hint, search
from core.methods.print import posintpas

info = "Use LinkedIn as information gathering resource."
searchinfo = "LinkedIn Gathering"
properties = {
    "LIMIT": ["Maximum results per search", ""],
}

# (what, dork) -- {s} is the target domain
DORKS = [
    ("employee profiles", 'site:linkedin.com/in "{s}"'),
    ("company profiles", 'site:linkedin.com/company "{s}"'),
]


def linkedin(web):
    posintpas("linkedin gathering")
    site = kit.domain(web)
    limit = kit.integer(properties, "LIMIT", "Maximum results per search", 30)

    profiles = []
    for what, dork in DORKS:
        kit.info(f"Finding LinkedIn {what} for {site}...")
        try:
            links = search(dork.format(s=site), limit)
        except Blocked:
            blocked_hint()
            break
        except Exception as e:
            kit.bad(f"Search failed: {e}")
            continue
        links = [l for l in links if "linkedin.com" in l and l not in profiles]
        if not links:
            kit.bad("Nothing found.")
        for link in links:
            kit.found("Profile found", link)
        profiles += links

    if profiles:
        kit.good(f"{len(profiles)} LinkedIn profile(s) found.")
        kit.Recorder(web, kit.PASSIVE, "linkedin")(profiles)
    return profiles


def attack(web):
    linkedin(web)
