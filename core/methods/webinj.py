#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helpers shared by the web injection scanners (HTML injection, CRLF, open
redirect, LDAP/XPath injection, CSRF).

    s = webinj.session(properties)                  # kit.http() + COOKIE/HEADERS options
    new = webinj.new_errors(SIGS, body, baselines)  # signatures absent from baselines
    ok, why = webinj.boolean_pair(point, s, true, false, base)
    host = webinj.redirect_host(location, request_url)
"""

from __future__ import annotations

import re
from urllib.parse import urljoin, urlsplit

from core.methods import inject
from core.methods import modkit as kit

COOKIE_OPTION = kit.AUTH_OPTIONS  # COOKIE + HEADERS


def session(properties: dict, timeout: float = 15):
    """HTTP session (Tor-aware, see kit.http) carrying the COOKIE / HEADERS options."""
    return kit.http(timeout=timeout, headers=kit.request_headers(properties))


# --------------------------------------------------------------------------
# error signatures
# --------------------------------------------------------------------------

def compile_signatures(signatures) -> list[tuple[str, re.Pattern]]:
    """[(label, regex)] -> [(label, compiled case-insensitive regex)]."""
    return [(label, re.compile(rx, re.I)) for label, rx in signatures]


def errors(compiled, body: str) -> dict[str, str]:
    """{label: matched text} of every signature present in `body`."""
    hits = {}
    for label, rx in compiled:
        m = rx.search(body or "")
        if m:
            hits[label] = m.group(0)[:120]
    return hits


def new_errors(compiled, body: str, baselines) -> dict[str, str]:
    """Signatures matching `body` that match none of the baseline bodies."""
    seen = set()
    for b in baselines:
        seen |= set(errors(compiled, b))
    return {k: v for k, v in errors(compiled, body).items() if k not in seen}


# --------------------------------------------------------------------------
# boolean differential
# --------------------------------------------------------------------------

SAME = 0.95     # bodies at least this similar are "the same page"
DIFFERENT = 0.85  # and at most this similar are "a different page"


def boolean_pair(point, s, true_value: str, false_value: str, base: str,
                 rounds: int = 2) -> tuple[bool, str]:
    """True when the TRUE payload reproduces the original page and the FALSE
    payload does not, consistently over `rounds` repetitions.

    The caller should already know the page is stable (base vs a second
    fetch) and that the parameter influences the output at all.
    """
    for _ in range(rounds):
        t = inject.text(point.send(s, true_value))
        f = inject.text(point.send(s, false_value))
        if not t or (not f and not base):
            return False, ""
        rt, rf, tf = inject.ratio(base, t), inject.ratio(base, f), inject.ratio(t, f)
        if not (rt >= SAME and rf <= DIFFERENT and tf <= DIFFERENT):
            return False, ""
    return True, f"TRUE~original {rt:.2f}, FALSE~original {rf:.2f}, TRUE~FALSE {tf:.2f} ({rounds} rounds)"


def stable_and_sensitive(point, s) -> tuple[str, bool]:
    """(original body, usable) where usable means the page is stable across
    two fetches AND a random value changes it (the parameter matters)."""
    base = inject.text(point.send(s, point.original))
    again = inject.text(point.send(s, point.original))
    if not base or inject.ratio(base, again) < SAME:
        return base, False
    rnd = inject.text(point.send(s, inject.marker()))
    return base, inject.ratio(base, rnd) <= DIFFERENT


# --------------------------------------------------------------------------
# redirects
# --------------------------------------------------------------------------

_CTRL = re.compile(r"[\t\n\r]")
_SCHEME = re.compile(r"^([a-z][a-z0-9+.-]*):(.*)$", re.I | re.S)


def browser_url(location: str, request_url: str) -> str:
    """Absolute URL a browser would navigate to for `location`, following
    the WHATWG URL quirks attackers use (backslashes, `https:host`,
    `///host`, leading control characters)."""
    loc = _CTRL.sub("", location or "").strip(" \x00\x0b\x0c")
    base = urlsplit(request_url)
    m = _SCHEME.match(loc)
    if m and m.group(1).lower() in ("http", "https"):
        scheme, rest = m.group(1).lower(), m.group(2).replace("\\", "/")
        if not rest.startswith("/") and scheme == base.scheme:
            return urljoin(request_url, rest)        # http:foo is relative on http pages
        return f"{scheme}://{rest.lstrip('/')}"
    if m:
        return loc                                   # javascript:, data:, ...
    loc = loc.replace("\\", "/")
    if loc.startswith("//"):
        return f"{base.scheme}://{loc.lstrip('/')}"
    return urljoin(request_url, loc)


def redirect_host(location: str, request_url: str) -> str:
    """Lowercase hostname a redirect to `location` lands on ('' if none)."""
    try:
        return (urlsplit(browser_url(location, request_url)).hostname or "").rstrip(".")
    except ValueError:
        return ""


# --------------------------------------------------------------------------
# error-signature + boolean scanners (LDAP, XPath)
# --------------------------------------------------------------------------

def syntax_check(point, s, compiled, payloads: list[str], pairs, kind: str):
    """Error-based then boolean-based detection for one point.

    Error: a payload makes a signature appear that neither the original
    value nor a random harmless value produce.
    Boolean: (true, false) payload templates -- `{v}` is the original value
    -- where TRUE reproduces the original page and FALSE does not; only on
    a stable page whose output depends on the parameter.
    """
    base = inject.text(point.send(s, point.original))
    benign = inject.text(point.send(s, inject.marker()))
    for payload in payloads:
        body = inject.text(point.send(s, payload, append=True))
        hits = new_errors(compiled, body, (base, benign))
        if hits:
            label, text = next(iter(hits.items()))
            return [inject.Finding(point, payload, kind=f"{kind} (error-based, confirmed)",
                                   evidence=f"{label} error not in baseline: {text!r}")]
    if not pairs:
        return []
    base, usable = stable_and_sensitive(point, s)
    if not usable:
        return []
    for true_t, false_t in pairs:
        t, f = true_t.format(v=point.original), false_t.format(v=point.original)
        ok, why = boolean_pair(point, s, t, f, base)
        if ok:
            return [inject.Finding(point, f"{t} / {f}", kind=f"{kind} (boolean-based, likely)",
                                   evidence=why)]
    return []
