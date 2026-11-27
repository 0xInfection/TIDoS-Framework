#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""HTTP header grabber."""

import requests

from core.methods import modkit as kit
from core.methods.print import posintact

info = "HTTP Header Grabber. Prints the response headers the target sends back."
searchinfo = "HTTP Header Grabber"
properties = {}


def grabhead(web):
    posintact("grab http headers")
    url = kit.url(web)
    kit.info("Grabbing HTTP headers...")
    try:
        r = kit.http().get(url, allow_redirects=True)
    except requests.RequestException as e:
        kit.bad(f"Request to {url} failed: {type(e).__name__}")
        return {}

    if r.url.rstrip("/") != url:
        kit.info(f"Followed redirects to {r.url}")
    kit.found("Status", f"{r.status_code} {r.reason}")
    print()
    kit.kv_table(r.headers.items())
    print()
    kit.Recorder(web, kit.ACTIVE, "grabhead")(
        "\n".join(f"{k}: {v}" for k, v in r.headers.items()))
    return dict(r.headers)


def attack(web):
    grabhead(web)
