#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Censys domain recon (Censys Platform API) -- passive recon."""

from __future__ import annotations

import json
import os

from core.methods import modkit as kit
from core.methods.print import posintpas

info = "Find information about domains using CENSYS (needs a Censys Platform personal access token)."
searchinfo = "CENSYS Domain Recon"
properties = {
    "PORTS": ["Web property ports to look up, comma separated", ""],
}

API = "https://api.platform.censys.io/v3/global/asset/webproperty/"


def flatten(obj, prefix: str = ""):
    """Yield ('a.b[0].c', value) pairs for a JSON document."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from flatten(v, f"{prefix}.{k}" if prefix else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from flatten(v, f"{prefix}[{i}]")
    else:
        yield prefix, obj


def lookup(session, prop: str) -> dict | None:
    resp = session.get(API + prop)
    if resp.status_code == 200:
        return resp.json().get("result", {}).get("resource") or {}
    try:
        err = resp.json().get("error", {})
        msg = err.get("message", err) if isinstance(err, dict) else err
    except ValueError:
        msg = resp.reason
    if resp.status_code in (401, 403):
        raise PermissionError(f"Censys refused the token (HTTP {resp.status_code}): {msg}")
    if resp.status_code == 429:
        raise PermissionError("Censys quota exceeded; try again later or use your own token.")
    kit.bad(f"{prop}: HTTP {resp.status_code} {msg}")
    return None


def censysdom(web):
    posintpas("censys domain recon")
    token = kit.apikey("CENSYS_API_TOKEN")
    if not token:
        kit.bad("Censys Search v1/v2 was decommissioned; create a Platform personal access token.")
        return {}
    name = kit.host(web)
    ports = [p.strip() for p in kit.option(properties, "PORTS", "Ports", "443,80").split(",")
             if p.strip().isdigit()]
    session = kit.http(timeout=20, headers={"Authorization": f"Bearer {token}",
                                            "Accept": "application/json"})

    results = {}
    for port in ports:
        prop = f"{name}:{port}"
        kit.info(f"Looking up web property {prop}...")
        try:
            data = lookup(session, prop)
        except PermissionError as e:
            kit.bad(str(e))
            return {}
        except Exception as e:
            kit.bad(f"Request to Censys failed: {e}")
            continue
        if not data:
            continue
        results[prop] = data
        kit.good(f"Found info for {prop}!")
        kit.kv_table(flatten(data))

    record = kit.Recorder(web, kit.PASSIVE, "censysdom")
    if not results:
        kit.bad(f"Did not find any info about domain {name}.")
        record(f"Did not find any info about domain {name}")
        return {}

    dump = json.dumps(results, indent=4, ensure_ascii=True)
    record(dump)
    path = os.path.join(kit.logdir(web), f"{name}-censys-data.json")
    with open(path, "w") as fh:
        fh.write(dump)
    kit.good(f"Censys data stored in {os.path.abspath(path)}")
    return results


def attack(web):
    censysdom(web)
