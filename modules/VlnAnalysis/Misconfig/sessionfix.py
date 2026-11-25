#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Session fixation (heuristic) -- does the server accept attacker-chosen session IDs?"""

from __future__ import annotations

import random
import string

import requests

from core.methods import modkit as kit
from core.methods import secheaders as sh
from core.methods.print import pvln

info = ("This module hunts for Session Fixation (heuristic, no login performed). It reads the "
        "session cookie the target issues, then sends a forged ID of the same format: if the "
        "server keeps using the forged ID instead of issuing a fresh one, an attacker can plant "
        "a known session ID on a victim. It also checks whether the session ID is accepted "
        "from the URL (?PHPSESSID=..., ;jsessionid=...). Point it at a page that starts a "
        "session (e.g. the login page). Confirm manually that the ID survives login.")
searchinfo = "Session Fixation Check"
properties = {
    "COOKIE": ["Extra cookies sent with every request, name=value; ... ('none' if none)", ""],
}

MAX_COOKIES = 3


def issued(resp) -> dict[str, str]:
    """name -> value of every (non-deleting) Set-Cookie along the redirect chain."""
    out = {}
    for r in (*resp.history, resp):
        for raw in sh.raw_values(r, "Set-Cookie"):
            c = sh.parse_set_cookie(raw)
            if c and not c.deleted:
                out[c.name] = c.value
    return out


def forge(value: str) -> str:
    """Random value with the same length and alphabet as a real session ID."""
    if value and all(c in string.hexdigits for c in value):
        alphabet = "0123456789abcdef" if value.lower() == value else string.hexdigits
    else:
        alphabet = "".join(sorted(set(value) & set(string.ascii_letters + string.digits))) \
            or string.ascii_lowercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(max(len(value), 16)))


class Client:
    """GETs without a cookie jar: every request carries exactly the cookies we pass."""

    def __init__(self, extra: str):
        self.session = kit.http()
        self.extra = extra

    def get(self, url: str, cookies: str = ""):
        self.session.cookies.clear()
        cookie = "; ".join(c for c in (self.extra, cookies) if c)
        try:
            return self.session.get(url, headers={"Cookie": cookie} if cookie else None)
        except requests.RequestException as e:
            kit.bad(f"Request failed: {type(e).__name__}")
            return None


def test_cookie(client: Client, url: str, name: str, legit: str) -> str | None:
    forged = forge(legit)
    first = client.get(url, f"{name}={forged}")
    if first is None:
        return None
    new = issued(first).get(name)
    if new == forged:
        return f"[confirmed] {name}: server re-issued the attacker-chosen ID {forged}"
    if new is not None:
        kit.bullet(f"{name}: forged ID replaced by a fresh one (good)")
        return None
    # silent acceptance: make sure the server does issue IDs when it rejects one
    again = client.get(url, f"{name}={forged}")
    if again is None or issued(again).get(name) not in (None, forged):
        kit.bullet(f"{name}: forged ID replaced on the second request (good)")
        return None
    return (f"[likely] {name}: forged ID {forged} accepted on two requests without a new "
            f"session being issued (fresh visitors get one)")


def test_url(client: Client, url: str, name: str, legit: str) -> str | None:
    forged = forge(legit)
    sep = "&" if "?" in url else "?"
    variants = [f"{url}{sep}{name}={forged}"]
    if name.lower() == "jsessionid":
        variants.insert(0, url.rstrip("/") + f"/;jsessionid={forged}")
    for v in variants:
        r = client.get(v)
        if r is None:
            continue
        if issued(r).get(name) == forged:
            return f"[confirmed] {name}: session ID accepted from the URL ({v}) and set as cookie"
        if r.status_code < 400 and f"{name.lower()}={forged}" in r.text.lower():
            return f"[confirmed] {name}: session ID from the URL propagated into page links ({v})"
    return None


def sessionfix(web):
    pvln("session fixation")
    record = kit.Recorder(web, kit.MISCONFIG, "sessionfix")
    extra = kit.option(properties, "COOKIE", "Extra cookies to send (enter for none)", "")
    client = Client(extra)
    url = kit.url(web) + "/"

    fresh = client.get(url)
    if fresh is None:
        return []
    cookies = issued(fresh)
    candidates = [(n, v) for n, v in cookies.items()
                  if sh.SESSION_NAME.search(n) and not sh.CSRF_NAME.search(n)]
    if not candidates:
        msg = ("No session cookie issued on this page; run it against a page that starts a "
               "session (e.g. the login form).")
        kit.bad(msg)
        record(msg)
        return []

    kit.good("Session cookie(s): " + ", ".join(n for n, _ in candidates))
    findings = []
    for name, legit in candidates[:MAX_COOKIES]:
        for test in (test_cookie, test_url):
            hit = test(client, url, name, legit)
            if hit:
                kit.found("Session fixation", hit)
                findings.append(hit)

    if not findings:
        kit.good("Forged session IDs are rejected and replaced.")
        record("Not vulnerable to session fixation (forged session IDs are replaced).")
        return []
    kit.warn("Heuristic result: verify that the session ID is not rotated at login.")
    for f in findings:
        record(f + " (heuristic, verify at login)")
    return findings


def attack(web):
    sessionfix(web)
