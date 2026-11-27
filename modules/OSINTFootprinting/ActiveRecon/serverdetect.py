#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Server detection -- resolves the target and fingerprints its web server."""

import socket

from core.methods import modkit as kit
from core.methods.print import posintact

info = ("Checks that the target resolves and answers, then identifies the web "
        "server and backend technology from the response headers (Server, "
        "X-Powered-By, ...), flagging CDNs/WAFs such as Cloudflare.")
searchinfo = "Server Detection module"
properties = {}

TECH_HEADERS = ("Server", "X-Powered-By", "X-AspNet-Version", "X-AspNetMvc-Version",
                "X-Generator", "X-Drupal-Cache", "X-Varnish", "Via", "X-Cache")


def serverdetect(web):
    """Fingerprint `web` (Target or URL string). Returns the detected headers."""
    posintact("detect server")
    record = kit.Recorder(web, kit.ACTIVE, "serverdetect")
    host = kit.host(web)

    kit.info("Checking server status...")
    try:
        ips = sorted(set(socket.gethostbyname_ex(host)[2]))
    except (socket.gaierror, UnicodeError) as e:
        kit.bad(f"Could not resolve {host}: {e}")
        return {}
    kit.good("Server resolves")
    kit.found("Server IP", ", ".join(ips))
    record("IP: " + ", ".join(ips))

    kit.info("Trying to identify backend...")
    try:
        r = kit.http().get(kit.url(web))
    except Exception as e:
        kit.bad(f"Server did not answer over HTTP: {type(e).__name__}")
        return {}

    seen = {h: r.headers[h] for h in TECH_HEADERS if h in r.headers}
    if not seen:
        kit.bad("The server does not disclose any technology header.")
        record("Server: not disclosed")
    for name, value in seen.items():
        kit.found(name, value)
        record(f"{name}: {value}")

    if "cloudflare" in seen.get("Server", "").lower() or "CF-RAY" in r.headers:
        kit.warn("The website is behind Cloudflare.")
        kit.info('Use the "Cloudflare" VulnLysis module to try bypassing it.')
        record("CDN: Cloudflare")
    return seen


def attack(web):
    serverdetect(web)
