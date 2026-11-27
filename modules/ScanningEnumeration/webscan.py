#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Webserver enumeration -- services and web servers of the target's IPs from Censys."""

from __future__ import annotations

import socket

from core.methods import modkit as kit
from core.methods.print import pscan
from modules.ScanningEnumeration.getcensys import censys_session, describe, lookup_host

info = ("This module looks up the IP addresses of the target in the Censys Platform "
        "database and fingerprints their services and web servers (needs a Censys "
        "Platform personal access token, CENSYS_API_TOKEN).")
searchinfo = "Webserver enumeration"
properties = {}


def addresses(web) -> list[str]:
    """All IPv4 addresses of the target."""
    name = kit.host(web)
    if kit.is_ip(name):
        return [name]
    try:
        return sorted(set(socket.gethostbyname_ex(name)[2]))
    except (OSError, UnicodeError):
        ip = kit.resolve(web)
        return [ip] if ip else []


def header(headers, wanted: str) -> str:
    """Value of a header from Censys' (dict or list shaped) header data."""
    if isinstance(headers, dict):
        items = headers.items()
    elif isinstance(headers, list):
        items = ((h.get("key") or h.get("name"), h.get("value") or h.get("values"))
                 for h in headers if isinstance(h, dict))
    else:
        return ""
    for key, value in items:
        if str(key).lower().replace("_", "-") != wanted:
            continue
        if isinstance(value, dict):
            value = value.get("headers") or value.get("value") or ""
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        return str(value)
    return ""


def http_info(svc: dict) -> tuple[str, str]:
    """(title, server) of an HTTP service record."""
    title = server = ""
    for ep in svc.get("endpoints") or [svc]:
        web_data = ep.get("http") or {}
        title = title or str(web_data.get("html_title") or web_data.get("title") or "")
        server = server or header(web_data.get("headers"), "server")
    return title.strip(), server.strip()


def show(ip: str, resource: dict) -> list[str]:
    """Print the services of a Censys host record; returns lines to store."""
    lines = []
    services = sorted(resource.get("services") or [], key=lambda s: s.get("port") or 0)
    ports = ", ".join(f"{s.get('port')}/{s.get('protocol') or '?'}" for s in services)
    kit.found(f"IP {ip}", ports or "no services indexed")
    lines.append(f"IP :> {ip} - Services :> {ports}")
    asn = resource.get("autonomous_system") or {}
    if asn:
        kit.bullet(f"AS{asn.get('asn', '?')} {asn.get('name', '')}".strip())
    for svc in services:
        port, proto = svc.get("port"), svc.get("protocol") or "?"
        software = ", ".join(filter(None, (describe(s) for s in svc.get("software") or [])))
        title, server = http_info(svc) if "HTTP" in proto.upper() else ("", "")
        print()
        kit.found(f"Port {port}", proto)
        kit.kv_table([("Software", software), ("Server", server), ("Title", title)])
        if server:
            lines.append(f"{ip}:{port} Server :> {server}")
        if title:
            lines.append(f"{ip}:{port} Title :> {title}")
    return lines


def webscan(web):
    pscan("webserver enumeration")
    token = kit.apikey("CENSYS_API_TOKEN")
    if not token:
        kit.bad("Censys Search v1/v2 was decommissioned; create a Platform personal access token.")
        return {}
    name = kit.host(web)
    ips = addresses(web)
    if not ips:
        kit.bad(f"Cannot resolve {name}.")
        return {}
    kit.found("Identified IPs", ", ".join(ips))
    kit.info("Querying Censys for the target's servers...")

    session = censys_session(token)
    record = kit.Recorder(web, kit.SCAN, "webscan")
    results = {}
    for ip in ips:
        try:
            resource = lookup_host(session, ip)
        except PermissionError as e:
            kit.bad(str(e))
            return results
        if resource is None:
            continue
        if not resource:
            kit.bad(f"Censys has no record of {ip}.")
            continue
        results[ip] = resource
        print()
        kit.good(f"Censys record found for {ip}")
        record(show(ip, resource))

    if not results:
        kit.bad(f"No Censys data found for {name}.")
        record(f"No Censys data found for {name}")
    return results


def attack(web):
    webscan(web)
