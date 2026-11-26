#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Censys OS identifier -- operating system of the target from Censys host data."""

from __future__ import annotations

from core.methods import modkit as kit
from core.methods.print import pscan

info = ("This module tries to determine the target's OS using the Censys Platform host "
        "data (needs a Censys Platform personal access token, CENSYS_API_TOKEN).")
searchinfo = "OS Identifier"
properties = {}

API = "https://api.platform.censys.io/v3/global/asset/host/"


def censys_session(token: str):
    return kit.http(timeout=20, headers={"Authorization": f"Bearer {token}",
                                         "Accept": "application/json"})


def lookup_host(session, ip: str) -> dict | None:
    """Censys host record of an IP: the resource dict, {} when Censys has no
    record, None on errors (already reported). Raises PermissionError on
    auth/quota failures so callers can stop querying."""
    try:
        resp = session.get(API + ip)
    except Exception as e:
        kit.bad(f"Request to Censys failed: {type(e).__name__}")
        return None
    if resp.status_code == 200:
        try:
            return resp.json().get("result", {}).get("resource") or {}
        except ValueError:
            kit.bad("Censys returned an unreadable answer.")
            return None
    if resp.status_code == 404:
        return {}
    try:
        err = resp.json().get("error", {})
        msg = err.get("message", err) if isinstance(err, dict) else err
    except ValueError:
        msg = resp.reason
    if resp.status_code in (401, 403):
        raise PermissionError(f"Censys refused the token (HTTP {resp.status_code}): {msg}")
    if resp.status_code == 429:
        raise PermissionError("Censys quota exceeded; try again later.")
    kit.bad(f"Censys: HTTP {resp.status_code} {msg}")
    return None


def describe(attr) -> str:
    """'vendor product version' of a Censys software/OS attribute."""
    if not isinstance(attr, dict):
        return str(attr or "")
    parts = [str(attr[k]) for k in ("vendor", "product", "version") if attr.get(k)]
    text = " ".join(dict.fromkeys(parts))
    return text or str(attr.get("cpe") or attr.get("uniform_resource_identifier") or "")


def host_os(resource: dict) -> str:
    """Operating system Censys attributes to a host ('' when unknown)."""
    os_name = describe(resource.get("operating_system"))
    if os_name:
        return os_name
    for svc in resource.get("services") or []:
        for attr in svc.get("operating_systems") or [svc.get("operating_system")]:
            os_name = describe(attr)
            if os_name:
                return os_name
    return ""


def censys_os(ip: str, token: str) -> str | None:
    """OS of `ip` according to Censys: name, '' if unknown, None on failure."""
    try:
        resource = lookup_host(censys_session(token), ip)
    except PermissionError as e:
        kit.bad(str(e))
        return None
    if resource is None:
        return None
    return host_os(resource)


def getos0x00(web):
    pscan("os identification")
    name = kit.host(web)
    token = kit.apikey("CENSYS_API_TOKEN")
    if not token:
        kit.bad("Censys Search v1/v2 was decommissioned; create a Platform personal access token.")
        return ""
    ip = kit.resolve(web)
    if not ip:
        kit.bad(f"Cannot resolve {name}.")
        return ""
    kit.found("Website IP", ip)
    kit.info("Looking up the host in Censys...")

    os_name = censys_os(ip, token)
    if os_name is None:
        return ""
    record = kit.Recorder(web, kit.SCAN, "getcensys")
    if os_name:
        kit.found("Operating System Identified", os_name)
        record(os_name)
    else:
        kit.bad(f"Censys has no Operating System match for {name} ({ip}).")
        record(f"No exact Operating System matches for {name}")
    return os_name


def attack(web):
    getos0x00(web)
