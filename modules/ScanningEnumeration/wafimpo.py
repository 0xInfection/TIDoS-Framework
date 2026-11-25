#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WAF detection engine -- signature matching and block detection (helper of `waf`)."""

from __future__ import annotations

import re
from typing import NamedTuple

from files.signaturedb.waf.signatures import STRONG, WAF_SIGNATURES, WEAK

MAX_BODY = 256 * 1024
# statuses a WAF answers a blocked request with; 400/404/500 are left out
# on purpose: those are what applications themselves return to bad input
BLOCK_STATUS = frozenset({403, 405, 406, 418, 419, 429, 444, 501, 999})
COOKIE_NAME = re.compile(r"\s*([^=;,\s]+)\s*=")
SET_COOKIE_SPLIT = re.compile(r",\s*(?=[^;,=\s]+=)")


def _compile(kind, field, pattern):
    if kind == "header":
        return re.compile(field, re.I), re.compile(pattern, re.I) if pattern else None
    if kind == "cookie":
        return None, re.compile(pattern)
    return None, re.compile(pattern, re.I | re.S)


COMPILED = tuple(
    (product, tuple((kind, *_compile(kind, field, pattern), strength)
                    for kind, field, pattern, strength in evidence))
    for product, evidence in WAF_SIGNATURES
)


class Snapshot(NamedTuple):
    """What one HTTP exchange looked like, reduced to what signatures need."""
    status: int | None
    headers: tuple        # ((name, value), ...)
    cookies: tuple        # names of the cookies the response sets
    body: str
    error: str = ""       # set when the request failed (reset, timeout...)


class Detection(NamedTuple):
    product: str
    confidence: str       # STRONG / WEAK
    evidence: tuple       # human-readable descriptions
    blockpage: bool       # a block page showed up only for the attack request


def set_cookies(resp) -> list[str]:
    """Raw Set-Cookie header lines of a requests.Response."""
    raw = getattr(resp, "raw", None)
    getlist = getattr(getattr(raw, "headers", None), "getlist", None)
    if getlist:
        return list(getlist("Set-Cookie"))
    joined = resp.headers.get("Set-Cookie", "")
    return SET_COOKIE_SPLIT.split(joined) if joined else []


def snapshot(resp) -> Snapshot:
    names = []
    for line in set_cookies(resp):
        m = COOKIE_NAME.match(line)
        if m and m.group(1) not in names:
            names.append(m.group(1))
    try:
        body = resp.text[:MAX_BODY]
    except Exception:  # undecodable / truncated body: headers still count
        body = ""
    return Snapshot(resp.status_code, tuple(resp.headers.items()), tuple(names), body)


def failure(error: Exception) -> Snapshot:
    return Snapshot(None, (), (), "", type(error).__name__)


def _short(text: str, width: int = 70) -> str:
    text = " ".join(text.split())
    return text if len(text) <= width else text[:width - 3] + "..."


def _match(kind, name_rx, rx, snap: Snapshot):
    """Description of the first piece of evidence in `snap`, or None."""
    if kind == "header":
        for name, value in snap.headers:
            if name_rx.fullmatch(name) and (rx is None or rx.search(value)):
                return f"header {name}: {_short(value)}" if value else f"header {name}"
    elif kind == "cookie":
        for name in snap.cookies:
            if rx.fullmatch(name):
                return f"cookie {name}"
    else:
        m = rx.search(snap.body)
        if m:
            return f"page text '{_short(m.group(0))}'"
    return None


def blocked(benign: Snapshot, attack: Snapshot) -> str:
    """Why the attack request looks blocked compared to the benign one ('' if not)."""
    if benign.error:
        return ""
    if attack.error:
        return f"the connection failed ({attack.error}) while the benign request worked"
    if attack.status != benign.status and attack.status in BLOCK_STATUS:
        return f"HTTP {attack.status} instead of HTTP {benign.status}"
    return ""


def detect(snapshots, attack: Snapshot | None = None, was_blocked: bool = False) -> list[Detection]:
    """Products whose evidence shows up.

    Strong evidence counts on every snapshot; weak evidence only on the
    attack response, and only when it was blocked.
    """
    snapshots = [s for s in snapshots if not s.error]
    others = [s for s in snapshots if s is not attack]
    found = []
    for product, evidence in COMPILED:
        hits, strong, blockpage = [], False, False
        for kind, name_rx, rx, strength in evidence:
            pool = snapshots if strength == STRONG else ([attack] if attack and was_blocked else [])
            for snap in pool:
                desc = _match(kind, name_rx, rx, snap)
                if desc:
                    if desc not in hits:
                        hits.append(desc)
                    strong |= strength == STRONG
                    break
            if (kind == "body" and strength == STRONG and attack is not None and not attack.error
                    and _match(kind, name_rx, rx, attack)
                    and not any(_match(kind, name_rx, rx, s) for s in others)):
                blockpage = True
        if hits:
            found.append(Detection(product, STRONG if strong else WEAK, tuple(hits), blockpage))
    found.sort(key=lambda d: d.confidence != STRONG)
    return found
