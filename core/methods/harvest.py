#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""
Page harvesting for the information-disclosure modules.

Fetches the target page plus the same-host pages it links to (depth 1,
crawled with Katana; COOKIE/HEADERS are sent), runs an extractor over each
body and reports unique findings per page.
"""

from __future__ import annotations

from typing import Callable, Iterable

from core.methods import modkit as kit

Extractor = Callable[[str], Iterable[str]]

MAX_PAGES = 100


def _fetch_one(url: str, headers: dict | None) -> dict[str, str]:
    kit.info(f"Fetching {url}")
    try:
        body = kit.http(headers=headers).get(url).text
    except Exception as e:
        kit.bad(f"Cannot fetch {url}: {type(e).__name__}")
        return {}
    if not body:
        kit.bad("Target did not return any content.")
        return {}
    return {url: body}


def crawl(target, crawl_links: bool = True, scripts: bool = False,
          headers: dict | None = None) -> dict[str, str]:
    """{url: body} for the target page and (optionally) the same-host pages
    it links to, plus their scripts when `scripts` (Katana, depth 1)."""
    base = kit.url(target)
    if not crawl_links:
        return _fetch_one(base, headers)
    from core.methods import crawler  # late import: avoids loading Katana plumbing when unused
    kit.info(f"Crawling {base} and the pages it links to...")
    res = crawler.crawl(target, 1, max_pages=MAX_PAGES, headers=headers,
                        keep_bodies=True, js=scripts)
    if res.error:
        kit.warn(f"{res.error} Scanning the target page only.")
        return _fetch_one(base, headers)
    pages = {p.url: p.body for p in res.pages.values()
             if p.body and (scripts or p.url not in res.scripts)}
    if not pages:
        kit.bad("Target did not return any content.")
    elif len(pages) > 1:
        kit.info(f"{len(pages)} page(s) fetched")
    return pages


def run(target, properties: dict, *, noun: str, lvl2: str,
        extract: Extractor, scripts: bool = False) -> set[str]:
    """Full module flow: crawl, extract, print per page, record."""
    deep = kit.flag(properties, "CRAWL", "Also scan pages linked from the target?", True)
    pages = crawl(target, deep, scripts, headers=kit.request_headers(properties))
    record = kit.Recorder(target, kit.INFODISC, lvl2)

    everything: set[str] = set()
    for page, body in pages.items():
        hits = list(dict.fromkeys(extract(body)))
        if not hits:
            continue
        kit.found(f"{noun[0].upper()}{noun[1:]} on", page)
        for h in hits:
            kit.bullet(h)
        everything.update(hits)

    if everything:
        kit.good(f"{len(everything)} unique {noun} across {len(pages)} page(s)")
        record(sorted(everything))
    elif pages:
        kit.bad(f"No {noun} disclosed in {len(pages)} page(s).")
        record(f"No {noun} found.")
    return everything
