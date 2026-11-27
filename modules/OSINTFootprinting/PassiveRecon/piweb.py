#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Ping check -- passive recon (pings the target from check-host.net's nodes)."""

from __future__ import annotations

import time

import requests

from core.methods import modkit as kit
from core.methods.print import posintpas

info = "Ping the target using an external API (check-host.net nodes around the world)."
searchinfo = "Ping Check"
properties = {
    "NODES": ["Number of check-host.net nodes to ping from", ""],
}

API = "https://check-host.net"
WAIT = 20  # seconds to wait for all nodes to report


def _summary(node: str, where: list, result) -> str:
    place = ", ".join(where[1:3]) if len(where) >= 3 else node
    probes = (result or [[]])[0] or []
    if not probes or probes[0] is None:
        return f"{place:<28} could not resolve / ping"
    ok = [p[1] for p in probes if p and p[0] == "OK"]
    ip = next((p[2] for p in probes if p and len(p) > 2), "")
    line = f"{place:<28} {ip:<16} {len(ok)}/{len(probes)} replies"
    if ok:
        line += f", avg {sum(ok) / len(ok) * 1000:.1f} ms"
    return line


def piweb(web):
    posintpas("ping check")
    host = kit.host(web)
    nodes = kit.integer(properties, "NODES", "Number of nodes to ping from", 5)
    s = kit.http(timeout=20, headers={"Accept": "application/json"})

    kit.info(f"Pinging {host} from {nodes} external node(s) ...")
    try:
        job = s.get(f"{API}/check-ping", params={"host": host, "max_nodes": nodes}).json()
        if not job.get("ok"):
            kit.bad(f"check-host.net refused the request: {job.get('error', job)}")
            return []
        results: dict = {}
        deadline = time.monotonic() + WAIT
        while time.monotonic() < deadline:
            time.sleep(2)
            results = s.get(f"{API}/check-result/{job['request_id']}").json()
            if all(v is not None for v in results.values()):
                break
    except (requests.RequestException, ValueError, KeyError) as e:
        kit.bad(f"check-host.net request failed: {e}")
        return []

    lines = [_summary(node, where, results.get(node)) for node, where in job["nodes"].items()
             if results.get(node) is not None]
    if not lines:
        kit.bad("No node answered in time.")
        return []
    kit.good(f"Ping results for {host}:")
    for line in lines:
        kit.bullet(line)
    kit.info(f"Full report: {job.get('permanent_link', '')}")
    kit.Recorder(web, kit.PASSIVE, "piweb")(lines)
    return lines


def attack(web):
    piweb(web)
