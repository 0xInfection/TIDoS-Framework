#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Robots/Sitemap printer -- fetches and parses robots.txt and sitemaps."""

import re
from urllib.parse import urljoin

from core.methods import modkit as kit
from core.methods.print import posintact

info = ("Fetches the target's robots.txt, lists its Allow/Disallow rules and "
        "advertised sitemaps, then fetches /sitemap.xml (plus any sitemap listed in "
        "robots.txt, following sitemap indexes one level) and lists the URLs found.")
searchinfo = "Robot/Sitemap Printer"
properties = {
    "SHOW": ["Max sitemap URLs to print (all are stored)", ""],
}

LOC = re.compile(r"<loc>\s*(.*?)\s*</loc>", re.I | re.S)
RULE = re.compile(r"^\s*(allow|disallow|sitemap)\s*:\s*(\S*)", re.I | re.M)


def fetch(session, url, kind):
    """Body of `url` if it looks like a real `kind` file (not an HTML soft-404)."""
    try:
        r = session.get(url)
    except Exception as e:
        kit.bad(f"Could not fetch {url}: {type(e).__name__}")
        return None
    body = r.text
    if r.status_code != 200 or not body.strip():
        kit.bad(f"{kind} not found ({r.status_code})")
        return None
    if kind == "robots.txt" and re.search(r"<html|<!doctype", body[:500], re.I):
        kit.bad("robots.txt not found (got an HTML page)")
        return None
    if kind != "robots.txt" and "<loc" not in body.lower():
        kit.bad(f"{kind} does not look like a sitemap")
        return None
    return body


def robots(session, base, record):
    kit.info("Testing for robots.txt...")
    body = fetch(session, f"{base}/robots.txt", "robots.txt")
    if body is None:
        record("robots.txt not found.")
        return []
    kit.good("robots.txt found!")
    print(body.strip() + "\n")
    record(">> robots.txt:\n" + body)

    rules = RULE.findall(body)
    for kind in ("disallow", "allow"):
        paths = sorted({p for k, p in rules if k.lower() == kind and p})
        if paths:
            kit.found(f"{kind.capitalize()} entries", len(paths))
    return [urljoin(base + "/", p) for k, p in rules if k.lower() == "sitemap" and p]


def sitemaps(session, base, extra, record, show):
    queue = [(u, 0) for u in dict.fromkeys([f"{base}/sitemap.xml", *extra])]
    seen, urls = set(), []
    while queue:
        smap, depth = queue.pop(0)
        if smap in seen:
            continue
        seen.add(smap)
        kit.info(f"Testing {smap}...")
        body = fetch(session, smap, "sitemap")
        if body is None:
            continue
        locs = LOC.findall(body)
        if "<sitemapindex" in body.lower():
            kit.good(f"Sitemap index with {len(locs)} sitemaps")
            if depth == 0:  # follow indexes one level only
                queue.extend((u, 1) for u in locs)
            continue
        kit.good(f"Sitemap found with {len(locs)} URLs")
        urls.extend(locs)

    urls = list(dict.fromkeys(urls))
    if not urls:
        record("sitemap.xml not found.")
        return urls
    for u in urls[:show]:
        kit.bullet(u)
    if len(urls) > show:
        kit.info(f"... {len(urls) - show} more (stored in the database)")
    record(">> sitemap.xml:\n" + "\n".join(urls))
    return urls


def robot(web):
    posintact("robots checker")
    record = kit.Recorder(web, kit.ACTIVE, "robot")
    show = kit.integer(properties, "SHOW", "Max sitemap URLs to print", 50)
    session = kit.http()
    base = kit.url(web)

    extra = robots(session, base, record)
    return sitemaps(session, base, extra, record, show)


def attack(web):
    robot(web)
