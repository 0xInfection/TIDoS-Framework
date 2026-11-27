#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""
Google results scraper shared by the Google-based recon modules.

Tor-aware through kit.http(). Google increasingly serves a JavaScript-only
page to scripts; that case raises Blocked so callers can explain it.
"""

from __future__ import annotations

from urllib.parse import parse_qs, urlsplit

from bs4 import BeautifulSoup

from core.methods import modkit as kit

GOOGLE = "https://www.google.com/search"
PAGE = 10


class Blocked(Exception):
    """Google answered with a captcha / JavaScript wall instead of results."""


def _blocked(resp) -> bool:
    return (resp.status_code == 429 or "/sorry/" in resp.url
            or "/httpservice/retry/enablejs" in resp.text
            or "unusual traffic" in resp.text)


def _links(html: str) -> list[str]:
    """Organic result URLs from a Google results page (basic or full HTML)."""
    out = []
    for a in BeautifulSoup(html, "lxml").find_all("a", href=True):
        href = a["href"]
        if href.startswith("/url?"):
            href = parse_qs(urlsplit(href).query).get("q", [""])[0]
        elif not a.find("h3"):
            continue
        host = urlsplit(href).hostname or ""
        if href.startswith("http") and not host.endswith(("google.com", "googleusercontent.com")):
            out.append(href)
    return list(dict.fromkeys(out))


def pages(query: str, limit: int = 30, session=None):
    """Yield the raw HTML of each Google results page (up to `limit` results).

    Raises Blocked when Google refuses to serve results, and requests'
    exceptions on network errors. Tor-aware through kit.http().
    """
    session = session or kit.http()
    for start in range(0, max(limit, 1), PAGE):
        resp = session.get(GOOGLE, params={"q": query, "start": start, "num": PAGE, "hl": "en"})
        if _blocked(resp):
            raise Blocked("Google answered with a captcha / JavaScript challenge")
        yield resp.text
        if not _links(resp.text):
            return


def search(query: str, limit: int = 30, session=None) -> list[str]:
    """Up to `limit` result URLs for `query`."""
    found: list[str] = []
    for html in pages(query, limit, session):
        found += [l for l in _links(html) if l not in found]
        if len(found) >= limit:
            break
    return found[:limit]


def blocked_hint() -> None:
    kit.bad("Google blocked the request (captcha / JavaScript-only results page).")
    kit.warn("Google now only serves results to JavaScript-capable browsers; run the query in a browser.")
