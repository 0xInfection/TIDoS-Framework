#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Google search -- passive recon."""

from core.methods import modkit as kit
from core.methods.google import Blocked, blocked_hint, search
from core.methods.print import posintpas

info = "Simple Google search (defaults to site:<target>)."
searchinfo = "Google Search"
properties = {
    "QUERY": ["Search query (default: site:<target domain>)", ""],
    "LIMIT": ["Maximum number of results (not recommended above 30)", ""],
}


def googleSearch(web=None):
    posintpas("google search")
    default = f"site:{kit.domain(web)}" if web else ""
    query = kit.option(properties, "QUERY", "Query", default)
    if not query:
        kit.bad("No query given.")
        return []
    limit = kit.integer(properties, "LIMIT", "Search limit (not recommended above 30)", 30)

    kit.info(f"Searching Google for: {query}")
    try:
        results = search(query, limit)
    except Blocked:
        blocked_hint()
        return []
    except Exception as e:
        kit.bad(f"Google search failed: {e}")
        return []

    if not results:
        kit.bad("No results.")
        return []
    kit.good(f"{len(results)} result(s) for '{query}':")
    for link in results:
        kit.found("Site found", link)
    if web:
        kit.Recorder(web, kit.PASSIVE, "googleSearch")([query] + results)
    return results


def attack(web):
    googleSearch(web)
