#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Cross-site request forgery -- heuristic form analysis."""

from __future__ import annotations

import math
import re
from collections import Counter
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from core.methods import modkit as kit
from core.methods.print import pvln

info = ("Heuristic CSRF review (nothing is submitted). Crawls the target (DEPTH) and, for "
        "every state-changing form (POST, not a search box), looks for an anti-CSRF token: "
        "hidden fields with token-like names or high-entropy values, or a csrf meta tag for "
        "JavaScript frameworks. Each page is loaded twice in one session and once in a fresh "
        "session to see whether the token is per-request, per-session or static. Session "
        "cookies are checked for SameSite. Verdicts are heuristic and per form.")
searchinfo = "Cross Site Request Forgery module"
properties = {
    "DEPTH": ["Crawl depth for finding forms (default 1; 0 = target page only)", ""],
    **kit.AUTH_OPTIONS,
}

DEFAULT_DEPTH = 1
MAX_PAGES = 60

TOKEN_NAME = re.compile(
    r"csrf|xsrf|_token|token$|^token|nonce|authenticity|requestverification|form_?key|"
    r"__requestdigest|antiforgery|^_?state$|form_build_id|^sesskey$|^ticket$", re.I)
META_TOKEN = re.compile(r"csrf|xsrf|request-?verification|antiforgery", re.I)
SESSION_COOKIE = re.compile(r"sess|sid$|^sid|auth|token|login|user|jwt|remember|"
                            r"^_?_?(?:host-|secure-)", re.I)
SEARCH_FIELD = re.compile(r"^(?:q|s|query|search|keywords?|term|k|lang(?:uage)?|locale|sort|page)$", re.I)
SKIP_TYPES = ("submit", "button", "image", "reset")
LABELS = {
    "vulnerable": "Likely CSRF",
    "weak": "Weak CSRF protection",
    "possible": "No CSRF token (needs review)",
    "mitigated": "CSRF mitigated by SameSite",
    "protected": "CSRF protected",
}
RISKY = ("vulnerable", "weak")


def entropy(value: str) -> float:
    """Shannon entropy in bits per character."""
    if not value:
        return 0.0
    n = len(value)
    return -sum(c / n * math.log2(c / n) for c in Counter(value).values())


def random_looking(value: str) -> bool:
    return len(value) >= 16 and entropy(value) >= 3.5 and not value.isalpha()


def forms_of(page_url: str, html: str) -> list[dict]:
    """Forms of a page: method, action, fields {name: (type, value)}, tokens."""
    soup = BeautifulSoup(html, "lxml")
    meta = [m.get("name") or m.get("property") for m in soup.find_all("meta", content=True)
            if META_TOKEN.search(m.get("name") or m.get("property") or "")]
    out = []
    for f in soup.find_all("form"):
        fields = {}
        for i in f.find_all(("input", "select", "textarea", "button"), attrs={"name": True}):
            fields[i["name"]] = ((i.get("type") or i.name).lower(), i.get("value") or "")
        tokens = {name: value for name, (typ, value) in fields.items()
                  if typ == "hidden" and (TOKEN_NAME.search(name) or random_looking(value))}
        out.append({
            "method": (f.get("method") or "GET").upper(),
            "action": urljoin(page_url, f.get("action") or page_url),
            "fields": fields,
            "tokens": tokens,
            "meta": meta,
        })
    return out


def _key(form: dict) -> tuple:
    return form["method"], form["action"], tuple(sorted(form["fields"]))


def state_changing(form: dict) -> bool:
    if form["method"] != "POST":
        return False
    names = [n for n, (typ, _) in form["fields"].items() if typ not in SKIP_TYPES and typ != "hidden"]
    return not names or not all(SEARCH_FIELD.match(n) for n in names)


def cookie_flags(session) -> list[tuple[str, str]]:
    """(name, SameSite value or '') of session-looking cookies the site set."""
    flags = []
    for c in session.cookies:
        if SESSION_COOKIE.search(c.name):
            same = ""
            for k, v in c._rest.items():  # http.cookiejar keeps unknown attributes here
                if k.lower() == "samesite":
                    same = (v or "").capitalize()
            flags.append((c.name, same))
    return flags


def token_behaviour(name: str, first: dict, again: dict | None, other: dict | None) -> str:
    v1 = first["tokens"].get(name, "")
    v2 = (again or {}).get("tokens", {}).get(name)
    v3 = (other or {}).get("tokens", {}).get(name)
    if v3 is not None and v3 == v1:
        return "static"           # same value in two independent sessions
    if v2 is not None and v2 != v1:
        return "per-request"
    if v3 is not None:
        return "per-session"
    return "unknown"


def verdict(form: dict, again: dict | None, other: dict | None, cookies,
            supplied: bool = False) -> tuple[str, str]:
    """(level, explanation); level is one of LABELS. `supplied`: the session
    cookie came from the COOKIE option, so its SameSite attribute is unknown."""
    samesite = {s for _, s in cookies}
    strict = bool(cookies) and samesite <= {"Strict", "Lax"}
    if form["tokens"]:
        notes = []
        for name in form["tokens"]:
            notes.append(f"{name} ({token_behaviour(name, form, again, other)})")
        if all("(static)" in n for n in notes):
            return "weak", "token is static (identical across sessions): " + ", ".join(notes)
        return "protected", "anti-CSRF token: " + ", ".join(notes)
    if form["meta"]:
        return "protected", f"no form token, but page exposes a CSRF meta tag ({', '.join(form['meta'])}) " \
                            "for JavaScript submission -- verify the request carries it"
    if strict:
        return "mitigated", "no anti-CSRF token; session cookies are SameSite=" + "/".join(sorted(samesite))
    if not cookies and supplied:
        return "possible", "no anti-CSRF token; the session cookie was supplied via COOKIE, so its " \
                           "SameSite attribute is unknown -- check the Set-Cookie at login " \
                           "(SameSite=None, or unset outside Chromium's Lax default, makes this exploitable)"
    if not cookies:
        return "possible", "no anti-CSRF token, but no session cookie was set while " \
                           "unauthenticated -- re-check when logged in"
    detail = ", ".join(f"{n}=SameSite:{s or 'unset'}" for n, s in cookies)
    return "vulnerable", f"no anti-CSRF token; session cookies without SameSite protection ({detail})"


def fetch_forms(session, url: str) -> list[dict]:
    try:
        r = session.get(url)
    except Exception:
        return []
    if "html" not in (r.headers.get("Content-Type") or "text/html").lower():
        return []
    return forms_of(r.url, r.text)


def pages_with_forms(web, depth: int, headers: dict) -> list[str]:
    from core.methods import crawler  # late import: bs4/lxml
    start = kit.url(web)
    if depth <= 0:
        return [start]
    kit.info(f"Crawling {start} (depth {depth}) for forms...")
    res = crawler.crawl(web, depth, max_pages=MAX_PAGES, headers=headers)
    if res.error:
        kit.warn(f"{res.error} Analysing the target page only.")
    pages = list(dict.fromkeys(f.page for f in res.forms))
    return pages or [start]


def analyse(url: str, headers: dict):
    """[(form, level, explanation)] for the state-changing forms of `url`.

    `a` is the user's session (COOKIE/HEADERS), `b` a second visitor that
    shares only the non-cookie headers, to see whether tokens are per session."""
    other_headers = {k: v for k, v in headers.items() if k.lower() != "cookie"}
    a, b = kit.http(headers=headers), kit.http(headers=other_headers)
    first = fetch_forms(a, url)
    again = {_key(f): f for f in fetch_forms(a, url)}
    other = {_key(f): f for f in fetch_forms(b, url)}
    cookies = cookie_flags(a)
    supplied = any(k.lower() == "cookie" for k in headers)
    out = []
    for form in first:
        if state_changing(form):
            level, why = verdict(form, again.get(_key(form)), other.get(_key(form)), cookies, supplied)
            out.append((form, level, why))
    return out


def csrf(web):
    pvln("cross site request forgery")
    record = kit.Recorder(web, kit.CRITICAL, "csrf")
    depth = max(0, kit.integer(properties, "DEPTH", "Crawl depth", DEFAULT_DEPTH))
    headers = kit.request_headers(properties)
    results, seen = [], set()
    for page in pages_with_forms(web, depth, headers):
        for form, level, why in analyse(page, headers):
            key = (_key(form), level)   # same form on many pages: report once per verdict
            if key in seen:
                continue
            seen.add(key)
            results.append((page, form, level, why))

    if not results:
        kit.bad("No state-changing (POST) forms found.")
        record("No state-changing (POST) forms found.")
        return []

    lines = []
    for page, form, level, why in results:
        label = LABELS[level]
        fields = ", ".join(n for n, (t, _) in form["fields"].items() if t not in SKIP_TYPES)
        line = f"[{label}] POST {form['action']} (form on {page}; fields: {fields}) -- {why}"
        if level in RISKY:
            kit.found(label, f"POST {form['action']}")
        elif level == "possible":
            kit.warn(f"{label}: POST {form['action']}")
        else:
            kit.info(f"{label}: POST {form['action']}")
        kit.bullet(why, 6)
        lines.append(line)
    risky = [lvl for _, _, lvl, _ in results if lvl in RISKY]
    print()
    if risky:
        kit.good(f"{len(risky)} of {len(results)} form(s) lack effective CSRF protection "
                 "(heuristic: confirm by replaying the request cross-site).")
    else:
        review = sum(1 for _, _, lvl, _ in results if lvl == "possible")
        kit.bad(f"No clearly unprotected forms among {len(results)} state-changing form(s)"
                + (f"; {review} without a token need review (see above)." if review else "."))
    record(["Heuristic CSRF analysis (per form):"] + lines)
    return results


def attack(web):
    csrf(web)
