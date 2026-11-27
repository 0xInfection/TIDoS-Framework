#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""OS command injection."""

from __future__ import annotations

from urllib.parse import quote

from core.methods import fileinj, inject
from core.methods import modkit as kit
from core.methods import webinj
from core.methods.print import pvln

info = ("Finds OS command injection in request parameters. Separator templates (DICT) append a "
        "command to each parameter's value: echo of a random marker followed by a shell arithmetic "
        "expansion (cmd.exe: set /a) whose computed result must appear in the response and not in the "
        "baseline -- an echoed payload never contains it. Hits are re-confirmed with a second command "
        "(printf concatenation / new operands). With BLIND, sleep N (ping -n on Windows) is timed "
        "against a sleep-0 control, twice with growing delays.")
searchinfo = "OS Command Injection Scanner"
DEFAULT_DICT = "files/payload-db/rce_payloads.lst"
properties = {
    **inject.OPTIONS,
    **webinj.COOKIE_OPTION,
    "DICT": [f"Separator templates with a {{cmd}} placeholder (default {DEFAULT_DICT})", ""],
    "BLIND": ["Also run time-based (sleep) checks (y/n, default y)", ""],
    "SLEEP": ["Seconds to sleep in time-based checks (default 5)", ""],
}

CONFIRMED = "Command injection (confirmed)"
BLIND = "Command injection (time-based, likely)"


def payload(tpl: str, cmd: str) -> str:
    """Fill a template; when it carries its own %XX escapes the command is encoded too."""
    tpl = tpl[4:] if tpl.startswith("win:") else tpl
    if fileinj.encoded(tpl):
        cmd = quote(cmd, safe="")
    return tpl.replace("{cmd}", cmd)


def commands(win: bool):
    """(command, expected output, second command, expected output) with fresh values."""
    if win:  # set /a is 32-bit: keep the product small
        a, b, c, d = (fileinj.numbers()[0] // 10 for _ in range(4))
        return f"set /a {a}*{b}", str(a * b), f"set /a {c}*{d}", str(c * d)
    a, b = fileinj.numbers()
    m, x, y = inject.marker(5), inject.marker(5), inject.marker(5)
    return f"echo {m}$(({a}*{b}))", f"{m}{a * b}", f"printf %s%s {x} {y}", x + y


def sleeper(win: bool, seconds: float) -> str:
    n = int(seconds)
    return f"ping -n {n + 1} 127.0.0.1" if win else f"sleep {n}"


def check(point: inject.Point, s, templates: list[str], delay: int):
    baseline = fileinj.body(point.send(s, point.original)) + fileinj.body(point.send(s, inject.marker()))

    def run(tpl: str, cmd: str) -> str:
        return fileinj.body(fileinj.send(point, s, payload(tpl, cmd), append=True))

    for tpl in templates:
        win = tpl.startswith("win:")
        cmd1, out1, cmd2, out2 = commands(win)
        if out1 in baseline or out1 not in run(tpl, cmd1):
            continue
        if out2 in baseline or out2 not in run(tpl, cmd2):
            continue
        yield inject.Finding(point, payload(tpl, cmd1),
                             f"'{cmd1}' -> {out1}; '{cmd2}' -> {out2}", CONFIRMED)
        return

    if not delay:
        return
    for tpl in templates:
        win = tpl.startswith("win:")

        def probe(d: float, tpl=tpl, win=win):
            resp, took = fileinj.timed(
                lambda: fileinj.send(point, s, payload(tpl, sleeper(win, d)), append=True))
            return took if resp is not None else None
        ev = fileinj.time_confirm(probe, delay)
        if ev:
            yield inject.Finding(point, payload(tpl, sleeper(win, delay)), ev, BLIND)
            return


def rce(web):
    pvln("os command injection")
    rec = kit.Recorder(web, kit.CRITICAL, "rce")
    templates = [t for t in inject.payloads(properties, DEFAULT_DICT, label="template") if "{cmd}" in t]
    if not templates:
        kit.bad("No templates with a {cmd} placeholder.")
        return []
    blind = kit.flag(properties, "BLIND", "Run time-based checks", True)
    delay = max(1, kit.integer(properties, "SLEEP", "Seconds to sleep in time-based checks", 5)) if blind else 0
    points = inject.discover(web, properties)
    if not points:
        rec("No injection points found.")
        return []
    s = webinj.session(properties, timeout=max(15, 2 * delay + 15))
    findings = inject.scan(points, lambda p: check(p, s, templates, delay))
    inject.report(findings, rec, clean="No command injection found.")
    return findings


def attack(web):
    rce(web)
