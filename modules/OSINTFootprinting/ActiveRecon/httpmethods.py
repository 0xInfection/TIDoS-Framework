#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""HTTP methods lister -- what an OPTIONS request says the server allows."""

import requests

from core.methods import modkit as kit
from core.methods.print import posintact

info = ("Lists the HTTP methods the target allows (OPTIONS request; Allow, Public and "
        "CORS headers) and flags the risky ones.")
searchinfo = "HTTP Methods Lister"
properties = {}

RISKY = {"PUT", "DELETE", "TRACE", "TRACK", "CONNECT", "PATCH", "PROPFIND",
         "PROPPATCH", "MKCOL", "COPY", "MOVE", "LOCK", "UNLOCK", "SEARCH"}
HEADERS = ("Allow", "Public", "Access-Control-Allow-Methods")


def httpmethods(web):
    posintact("http methods")
    url = kit.url(web)
    record = kit.Recorder(web, kit.ACTIVE, "httpmethods")
    try:
        r = kit.http().options(url, allow_redirects=False)
    except requests.RequestException as e:
        kit.bad(f"OPTIONS request failed: {type(e).__name__}")
        return []

    methods = []
    for header in HEADERS:
        for m in r.headers.get(header, "").split(","):
            m = m.strip().upper()
            if m and m not in methods:
                methods.append(m)

    if not methods:
        kit.bad(f"HTTP method OPTIONS request unsuccessful (HTTP {r.status_code}, no Allow header).")
        record("HTTP Method Options Request Unsuccessful.")
        return []

    kit.good("The following HTTP methods are allowed...")
    for m in methods:
        kit.bullet(f"{m}  (risky)" if m in RISKY else m)
    risky = [m for m in methods if m in RISKY]
    if risky:
        kit.warn(f"Potentially dangerous methods enabled: {', '.join(risky)}")
    record(", ".join(methods))
    return methods


def attack(web):
    httpmethods(web)
