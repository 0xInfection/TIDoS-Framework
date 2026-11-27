#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Reflected cross-site scripting scanner."""

from core.methods import inject
from core.methods import modkit as kit
from core.methods import webinj
from core.methods import xss as engine
from core.methods.print import pvln

info = ("Looks for reflected Cross Site Scripting: injects a random marker into every parameter "
        "(PARAM, or the ones found by crawling) and into the User-Agent, Referer and cookies, works "
        "out where it is reflected (HTML text, quoted/unquoted attribute, script string or code, "
        "comment, textarea/title/style) and sends matching breakout payloads. Only payloads that "
        "come back unencoded in an executable position are reported.")
searchinfo = "Cross Site Scripting"
properties = {
    **inject.OPTIONS,
    **webinj.COOKIE_OPTION,
    "TESTHEADERS": ["Also test User-Agent, Referer and cookie reflection (y/n, default y)", ""],
}

MAX_HEADER_URLS = 5


def xss(target):
    pvln("Cross site scripting")
    headers = kit.flag(properties, "TESTHEADERS", "Also test User-Agent/Referer/cookie reflection", True)
    points = inject.discover(target, properties)
    session = webinj.session(properties, timeout=15)
    if headers:
        urls = [kit.url(target)] + [p.url_for(p.original) if p.method == "GET" else p.url for p in points]
        urls = list(dict.fromkeys(urls))[:MAX_HEADER_URLS]
        extra = engine.header_points(session, urls)
        kit.info(f"Testing {len(extra)} header/cookie point(s) on {len(urls)} URL(s) as well.")
        points = list(points) + extra
    if not points:
        return
    findings = inject.scan(points, engine.make_check(session))
    inject.report(findings, kit.Recorder(target, kit.CRITICAL, "xss"),
                  clean="No reflected XSS found.")


def attack(target):
    xss(target)
