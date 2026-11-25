#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTML injection -- reflected, marker based."""

from __future__ import annotations

import re

from core.methods import inject
from core.methods import modkit as kit
from core.methods import webinj
from core.methods.print import pvln

info = ("Finds reflected HTML injection: every parameter (PARAM, or found by crawling) "
        "receives a tag carrying a random marker, plain and with breakouts for attribute, "
        "<textarea>/<title> and comment contexts. A parameter is reported only when the "
        "tag comes back unencoded and outside any raw-text, comment or attribute context, "
        "i.e. where a browser would render it as markup.")
searchinfo = "HTML Injection Test"
properties = {**inject.OPTIONS, **webinj.COOKIE_OPTION}

# breakout prefixes: none, attribute values, RCDATA/raw-text elements, comments
PREFIXES = ("", "\">", "'>", "</textarea>", "</title>", "-->")

# elements whose content is not parsed as markup
RAW_TEXT = ("script", "style", "textarea", "title", "xmp", "noembed", "noframes",
            "iframe", "noscript", "plaintext")

OPEN_TAG = re.compile(r"<[a-z]")
FULL_TAG = re.compile(r"""<[a-zA-Z][^\s/>]*(?:[\s/]+[^\s"'=<>/]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+))?)*[\s/]*>""")


def _payload(mark: str) -> tuple[str, re.Pattern]:
    tag = f"<b id={mark}>{mark}</b>"
    return tag, re.compile(rf"<b\s+id=[\"']?{mark}[\"']?\s*>{mark}</b>", re.I)


def rendered(body: str, pos: int) -> bool:
    """True when position `pos` of `body` is parsed as markup by a browser:
    not inside a tag/attribute, a comment or a raw-text element."""
    before = body[:pos].lower()
    if before.rfind("<!--") > before.rfind("-->"):
        return False
    start = max((m.start() for m in OPEN_TAG.finditer(before)), default=-1)
    if start >= 0:
        tag = FULL_TAG.match(body, start)
        if not tag or tag.end() > pos:
            return False   # inside a tag, e.g. value="&quot;><b ...>"
    for name in RAW_TEXT:
        opened = max(before.rfind(f"<{name}>"), before.rfind(f"<{name} "), before.rfind(f"<{name}\n"))
        if opened > before.rfind(f"</{name}"):
            return False
    return True


def check(point, s):
    for prefix in PREFIXES:
        mark = inject.marker()
        tag, rx = _payload(mark)
        resp = point.send(s, prefix + tag, append=True)
        body = inject.text(resp)
        if mark not in body:
            if not prefix:
                return []  # not reflected at all: breakouts won't help
            continue
        for m in rx.finditer(body):
            if rendered(body, m.start()):
                ctype = (resp.headers.get("Content-Type") or "").lower()
                if ctype and "html" not in ctype:
                    return []  # reflected in JSON/text: not rendered as HTML
                where = f" after breakout {prefix!r}" if prefix else ""
                return [inject.Finding(point, prefix + tag, kind="HTML injection",
                                       evidence=f"tag reflected unencoded in markup context{where}: "
                                                f"{m.group(0)}")]
    return []


def htmli(web):
    pvln("html injection")
    record = kit.Recorder(web, kit.CRITICAL, "htmli")
    points = inject.discover(web, properties)
    if not points:
        record("No injection points found.")
        return []
    s = webinj.session(properties)
    findings = inject.scan(points, lambda p: check(p, s))
    inject.report(findings, record, "No HTML injection found.")
    return findings


def attack(web):
    htmli(web)
