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
Evidence helpers for the file inclusion, path traversal and code/command
injection scanners (lfi, rfi, pathtrav, phpi, rce, shellshock,
strutsshock).

    sig = file_signature("../../etc/passwd%00")      # -> "passwd"
    hit = file_evidence(body, baseline, sig)        # signature snippet or ""
    src = php_source(body, baseline)                # decoded php://filter output
    err = inclusion_error(body, baseline, token)    # error naming our token
    a, b = numbers()                                 # operands for computed markers
    ev = time_confirm(probe, delay)                  # repeated sleep vs control

Nothing here decides on its own that a target is vulnerable: every check
needs the evidence to be absent from a baseline response as well.
"""

from __future__ import annotations

import base64
import binascii
import random
import re
import time
from typing import Callable
from urllib.parse import unquote

import requests

from files.signaturedb.lfierror_signatures import FILE_SIGNATURES, INCLUSION_ERRORS

_FILES = {key: (suffix, label, re.compile(rx)) for key, (suffix, label, rx) in FILE_SIGNATURES.items()}
_ERRORS = [re.compile(rx) for rx in INCLUSION_ERRORS]
_ENCODED = re.compile(r"%[0-9a-fA-F]{2}")
_B64 = re.compile(r"[A-Za-z0-9+/]{24,}={0,2}")


# --------------------------------------------------------------------------
# sending
# --------------------------------------------------------------------------

def encoded(payload: str) -> bool:
    """True when a payload carries its own percent-encoding (%00, %252e...)."""
    return bool(_ENCODED.search(payload))


def send(point, session, payload: str, append: bool = False, **kw):
    """point.send() that keeps pre-encoded payloads intact.

    GET: sent raw (not encoded again). POST: decoded once so that the form
    encoding of requests reproduces the intended bytes on the wire.
    """
    if encoded(payload):
        if point.method == "POST":
            return point.send(session, unquote(payload), append=append, **kw)
        return point.send(session, payload, append=append, raw=True, **kw)
    return point.send(session, payload, append=append, **kw)


def raw_get(session, url: str, timeout: float = 10, **kw):
    """GET `url` exactly as written: no dot-segment removal (requests/urllib3
    collapse /a/../b otherwise). None on network errors."""
    try:
        prep = session.prepare_request(requests.Request("GET", url, **kw))
        prep.url = url
        return session.send(prep, timeout=timeout, allow_redirects=False)
    except Exception:
        return None


def body(resp) -> str:
    if resp is None:
        return ""
    try:
        return resp.text
    except Exception:
        return ""


def headers_text(resp) -> str:
    if resp is None:
        return ""
    return "\n".join(f"{k}: {v}" for k, v in resp.headers.items())


# --------------------------------------------------------------------------
# file content evidence
# --------------------------------------------------------------------------

def _normal(payload: str) -> str:
    p = payload
    for _ in range(3):
        p = unquote(p)
    p = p.replace("\\", "/").split("\x00")[0].lower()
    return p.rstrip("/ ")


def file_signature(payload: str) -> str:
    """Key of the FILE_SIGNATURES entry the payload targets ('' if none)."""
    path = _normal(payload)
    for key, (suffix, _, _) in _FILES.items():
        if path.endswith(suffix):
            return key
    return ""


def file_label(key: str) -> str:
    return _FILES[key][1]


def control_payload(payload: str, key: str) -> str:
    """Same payload pointing at a file that does not exist (same directory)."""
    name = _FILES[key][0].rsplit("/", 1)[-1]
    idx = payload.lower().rfind(name)
    if idx < 0:
        return ""
    return payload[:idx] + "tid" + str(random.randint(10 ** 6, 10 ** 7)) + payload[idx + len(name):]


def file_evidence(text: str, baseline: str, key: str) -> str:
    """Snippet proving file `key` was read: matched in `text`, not in baseline."""
    rx = _FILES[key][2]
    if rx.search(baseline):
        return ""
    m = rx.search(text)
    if not m:
        return ""
    return shorten(m.group(0).replace("\x00", " ").strip())


def php_source(text: str, baseline: str) -> str:
    """First line of PHP source hidden in a base64 blob (php://filter output)."""
    for m in _B64.finditer(text):
        blob = m.group(0)
        if blob in baseline:
            continue
        try:
            raw = base64.b64decode(blob + "=" * (-len(blob) % 4), validate=False)
        except (binascii.Error, ValueError):
            continue
        src = raw.decode("utf-8", errors="replace")
        idx = max(src.find("<?php"), src.find("<?="))
        if idx >= 0:
            return shorten(src[idx:].splitlines()[0])
    return ""


def inclusion_error(text: str, baseline: str, token: str, window: int = 300) -> str:
    """Inclusion/file error that names `token` and is not in the baseline."""
    text = re.sub(r"<[^>]+>", "", text)
    for rx in _ERRORS:
        if rx.search(baseline):
            continue
        for m in rx.finditer(text):
            lo, hi = max(0, m.start() - window), m.end() + window
            if token in text[lo:hi]:
                start = text.rfind("\n", 0, m.start()) + 1
                if start < m.start() - 100:  # long line: cut at a word boundary
                    start = text.find(" ", m.start() - 100) + 1
                return shorten(text[start:m.end() + 60])
    return ""


def shorten(value: str, width: int = 120) -> str:
    value = " ".join(value.split())
    return value if len(value) <= width else value[:width - 3] + "..."


# --------------------------------------------------------------------------
# computed markers / timing
# --------------------------------------------------------------------------

def numbers() -> tuple[int, int]:
    """Two random 5-digit operands; their product is a 9-10 digit canary."""
    return random.randint(10000, 99999), random.randint(10000, 99999)


def timed(fn: Callable[[], object]) -> tuple[object, float]:
    start = time.monotonic()
    resp = fn()
    return resp, time.monotonic() - start


def time_confirm(probe: Callable[[float], float | None], delay: float) -> str:
    """Confirm a time-based injection.

    probe(seconds) sends the payload asking for a `seconds` sleep and returns
    the elapsed time (None on error/timeout). Two rounds, the second with a
    doubled delay; each round needs the sleep request to take at least the
    delay and to exceed its own sleep-0 control by 80% of the delay.
    """
    seen = []
    for d in (delay, delay * 2):
        slow = probe(d)
        if slow is None or slow < d * 0.9:
            return ""
        ctl = probe(0)
        if ctl is None or slow - ctl < d * 0.8:
            return ""
        seen.append(f"sleep {d:g}s took {slow:.1f}s vs {ctl:.1f}s control")
    return "; ".join(seen)
