#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Open redirect scanner."""

from __future__ import annotations

import re
from urllib.parse import urlencode, urlsplit, urlunsplit

from core.methods import inject
from core.methods import modkit as kit
from core.methods import webinj
from core.methods.print import pvln

info = ("Finds open redirects. Every parameter (PARAM, crawled ones, or -- when none are "
        "found -- common redirect parameters such as next/url/returnTo on the target URL) "
        "receives a URL on a random attacker host, plus filter bypasses (//host, /\\host, "
        "https:host, target-prefix and userinfo tricks, encoded slashes). Redirects are not "
        "followed; a finding needs the Location header (or a meta refresh / JavaScript "
        "location assignment) to resolve, the way a browser parses it, to the attacker host.")
searchinfo = "Open Redirect Checker"
properties = {**inject.OPTIONS, **webinj.COOKIE_OPTION}

COMMON_PARAMS = (
    "next", "url", "redirect", "redirect_uri", "redirect_url", "redirectUrl", "redir",
    "return", "returnTo", "return_to", "returnUrl", "return_url", "dest", "destination",
    "continue", "goto", "go", "target", "to", "out", "forward", "callback", "r", "u",
    "rurl", "checkout_url", "success_url", "back", "ref", "uri", "path", "link",
)

META = re.compile(r"<meta[^>]+http-equiv\s*=\s*[\"']?refresh[^>]*>", re.I)
META_URL = re.compile(r"url\s*=\s*[\"']?([^\"'>;\s]+)", re.I)
JS = re.compile(
    r"(?:window|document|top|self|parent)?\.?location(?:\.href)?\s*=\s*[\"'`]([^\"'`]+)"
    r"|location\.(?:replace|assign)\(\s*[\"'`]([^\"'`]+)", re.I)


def variants(evil: str, target_host: str) -> list[str]:
    return [
        f"https://{evil}/",
        f"//{evil}/",
        f"/\\{evil}/",
        f"\\\\{evil}/",
        f"https:{evil}/",
        f"/%2f{evil}/",
        f"https://{target_host}.{evil}/",
        f"https://{target_host}@{evil}/",
        f"//{evil}%2f%2e%2e",
        f"%2f%2f{evil}/",
        f"https://{evil}%23.{target_host}/",
    ]


def is_evil(host: str, evil: str) -> bool:
    return host == evil or host.endswith("." + evil)


def landing(resp, evil: str) -> tuple[str, str]:
    """(confidence, evidence) when the response sends the browser to `evil`."""
    if resp is None:
        return "", ""
    loc = resp.headers.get("Location")
    if loc and 300 <= resp.status_code < 400 and is_evil(webinj.redirect_host(loc, resp.url), evil):
        return "confirmed", f"HTTP {resp.status_code} Location: {loc}"
    refresh = resp.headers.get("Refresh", "")
    m = META_URL.search(refresh)
    if m and is_evil(webinj.redirect_host(m.group(1), resp.url), evil):
        return "confirmed", f"Refresh header: {refresh}"
    body = inject.text(resp)[:200000]
    if evil not in body:
        return "", ""
    for tag in META.findall(body):
        m = META_URL.search(tag.split("content", 1)[-1])
        if m and is_evil(webinj.redirect_host(m.group(1), resp.url), evil):
            return "confirmed", f"meta refresh: {tag[:150]}"
    for m in JS.finditer(body):
        dest = m.group(1) or m.group(2)
        if is_evil(webinj.redirect_host(dest, resp.url), evil):
            return "likely", f"JavaScript redirect: {m.group(0)[:150]}"
    return "", ""


def _evil() -> str:
    return f"{inject.marker(6)}.example.com"


def check(point, s, target_host: str):
    evil = _evil()
    for payload in variants(evil, target_host):
        conf, why = landing(point.send(s, payload, allow_redirects=False), evil)
        if conf:
            return [inject.Finding(point, payload, kind=f"Open redirect ({conf})", evidence=why)]
    return []


def common_params(web, s, target_host: str) -> list:
    """Try COMMON_PARAMS on the target URL: all at once per payload, then
    pin down which one is responsible."""
    parts = urlsplit(kit.url(web))
    base = urlunsplit((parts.scheme, parts.netloc, parts.path or "/", "", ""))
    kit.info(f"Trying {len(COMMON_PARAMS)} common redirect parameters on {base}...")
    evil = _evil()
    for payload in variants(evil, target_host):
        try:
            resp = s.get(f"{base}?{urlencode([(p, payload) for p in COMMON_PARAMS])}",
                         allow_redirects=False)
        except Exception:
            continue
        if not landing(resp, evil)[0]:
            continue
        found = []
        for name in COMMON_PARAMS:
            point = inject.Point("GET", base, ((name, ""),), name)
            conf, why = landing(point.send(s, payload, allow_redirects=False), evil)
            if conf:
                f = inject.Finding(point, payload, kind=f"Open redirect ({conf})", evidence=why)
                kit.found(f.kind, f"{point} <- {payload}")
                found.append(f)
        return found
    return []


def openredirect(web):
    pvln("open redirect checker")
    record = kit.Recorder(web, kit.CRITICAL, "openredirect")
    s = webinj.session(properties)
    target_host = kit.host(web)
    points = inject.discover(web, properties)
    findings = inject.scan(points, lambda p: check(p, s, target_host))
    if not points:
        findings = common_params(web, s, target_host)
    inject.report(findings, record, "No open redirect found.")
    return findings


def attack(web):
    openredirect(web)
