#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Page links -- passive recon."""

from __future__ import annotations

from urllib.parse import urldefrag, urljoin, urlsplit

import requests
from bs4 import BeautifulSoup

from core.methods import modkit as kit
from core.methods.print import posintpas

info = "Find Links pointing to the target."
searchinfo = "Page Links"
properties = {}


def page_links(base: str, html: str) -> tuple[list[str], list[str]]:
    """(same-host, external) links of a page, deduplicated in page order."""
    host = urlsplit(base).hostname
    internal, external = [], []
    for a in BeautifulSoup(html, "lxml").find_all("a", href=True):
        link = urldefrag(urljoin(base, a["href"].strip()))[0]
        parts = urlsplit(link)
        if parts.scheme not in ("http", "https"):
            continue
        (internal if parts.hostname == host else external).append(link)
    return list(dict.fromkeys(internal)), list(dict.fromkeys(external))


def links(web):
    posintpas("page links")
    base = kit.url(web)
    kit.info(f"Fetching links from {base} ...")
    try:
        resp = kit.http().get(base)
    except requests.RequestException as e:
        kit.bad(f"Could not fetch {base}: {e}")
        return []

    internal, external = page_links(resp.url or base, resp.text)
    if not internal and not external:
        kit.bad("No links found on the page.")
        kit.Recorder(web, kit.PASSIVE, "links")("No links found.")
        return []

    for link in internal:
        kit.found("Found link", link)
    if external:
        kit.info(f"{len(external)} external link(s):")
        for link in external:
            kit.bullet(link)
    kit.good(f"{len(internal)} same-host and {len(external)} external link(s).")
    kit.Recorder(web, kit.PASSIVE, "links")(internal + external)
    return internal


def attack(web):
    links(web)
