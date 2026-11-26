#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Clickjacking -- can a foreign origin frame the target page?"""

import html
import os

from core.methods import modkit as kit
from core.methods import secheaders as sh
from core.methods.print import pvln

info = ("This module analyses if the target is clickjackable: whether a cross-origin page "
        "may frame it, applying the browsers' rules (enforced CSP frame-ancestors wins over "
        "X-Frame-Options; ALLOW-FROM and invalid values are ignored; conflicting values deny). "
        "For frameable HTML pages a PoC is written to tmp/logs/<host>-logs/.")
searchinfo = "Clickjack Tester"
properties = {}

POC = """<!doctype html>
<html>
  <head><title>Clickjack test page</title></head>
  <body>
    <p>If the target page shows below, it is vulnerable to clickjacking.</p>
    <iframe src="{url}" width="1000" height="600" style="opacity:0.6"></iframe>
  </body>
</html>
"""


def clickjack(web):
    pvln("clickjacking")
    record = kit.Recorder(web, kit.MISCONFIG, "clickjack")
    resp = sh.fetch(web)
    if resp is None:
        return False

    framing = sh.analyze_framing(sh.raw_values(resp, "X-Frame-Options"),
                                 sh.raw_values(resp, "Content-Security-Policy"))
    kit.kv_table([("URL", resp.url), ("Status", resp.status_code),
                  ("X-Frame-Options", resp.headers.get("X-Frame-Options")),
                  ("CSP frame-ancestors", " | ".join(" ".join(f) for f in
                                                     sh.frame_ancestors(sh.raw_values(
                                                         resp, "Content-Security-Policy"))))])
    if sh.raw_values(resp, "Content-Security-Policy-Report-Only") and \
            "frame-ancestors" in resp.headers.get("Content-Security-Policy-Report-Only", ""):
        kit.info("frame-ancestors in a Report-Only policy is not enforced.")

    if not framing.frameable:
        kit.good(f"Not clickjackable: framing blocked by {framing.reason}.")
        record(f"Not clickjackable: framing blocked by {framing.reason}.")
        return False
    if not sh.is_html(resp):
        kit.info(f"Frameable ({framing.reason}), but the response is not HTML "
                 f"({resp.headers.get('Content-Type', 'no Content-Type')}): low impact.")
        record(f"Frameable but not HTML ({framing.reason}).")
        return False

    kit.found("Clickjackable", framing.reason)
    path = os.path.join(kit.logdir(web), "clickjack-poc.html")
    try:
        with open(path, "w") as fh:
            fh.write(POC.format(url=html.escape(resp.url, quote=True)))
        kit.info(f"PoC saved to {path}")
        record(f"Clickjackable: {framing.reason}. PoC: {path}")
    except OSError as e:
        kit.bad(f"Could not write the PoC: {e}")
        record(f"Clickjackable: {framing.reason}.")
    return True


def attack(web):
    clickjack(web)
