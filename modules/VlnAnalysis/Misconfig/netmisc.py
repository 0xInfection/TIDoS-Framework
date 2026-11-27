#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Telnet exposure -- cleartext remote login reachable on the target."""

from __future__ import annotations

import socket
import time

import core.variables as variables
from core.methods import modkit as kit
from core.methods.print import pvln

info = ("This module discovers Telnet misconfiguration: it connects to the Telnet port(s) and "
        "confirms the service by its option negotiation (IAC commands) or login banner. "
        "Telnet sends credentials in cleartext. Raw TCP: not routed through Tor.")
searchinfo = "Telnet Checker"
properties = {
    "PORT": ["Telnet port(s), comma separated", ""],
}

IAC = 0xFF
COMMANDS = range(0xFB, 0xFF)    # WILL WONT DO DONT
LOGIN_HINTS = (b"login:", b"username:", b"user name:", b"password:", b"telnet")


def probe(ip: str, port: int, timeout: float = 5.0):
    """('closed'|'telnet'|'open', banner text)."""
    try:
        sock = socket.create_connection((ip, port), timeout=timeout)
    except OSError:
        return "closed", ""
    data = b""
    with sock:
        sock.settimeout(1.5)
        end = time.monotonic() + 4
        while time.monotonic() < end and len(data) < 2048:
            try:
                chunk = sock.recv(1024)
            except OSError:
                break
            if not chunk:
                break
            data += chunk
            if any(h in data.lower() for h in LOGIN_HINTS):
                break
    negotiates = any(data[i] == IAC and data[i + 1] in COMMANDS for i in range(len(data) - 1))
    text = " ".join(bytes(b for b in data if 32 <= b < 127 or b in (9, 10, 13)).decode().split())
    if negotiates or any(h in data.lower() for h in LOGIN_HINTS):
        return "telnet", text
    return "open", text


def netmisc(web):
    pvln("network misconf.")
    record = kit.Recorder(web, kit.MISCONFIG, "netmisc")
    if variables.tor:
        kit.warn("Raw TCP connections do NOT go through Tor.")
    ip = kit.resolve(web)
    if not ip:
        kit.bad(f"Could not resolve {kit.host(web)}.")
        return []
    raw = kit.option(properties, "PORT", "Telnet port(s)", "23")
    ports = [int(p) for p in raw.replace(" ", "").split(",") if p.isdigit() and 0 < int(p) < 65536]
    if not ports:
        kit.warn(f"Invalid PORT '{raw}', using 23.")
        ports = [23]

    findings = []
    for port in ports:
        kit.info(f"Connecting to {ip}:{port}...")
        state, banner = probe(ip, port)
        if state == "closed":
            kit.bullet(f"{port}/tcp closed or filtered")
            record(f"{port}/tcp closed: Telnet not exposed.")
        elif state == "telnet":
            kit.found("Telnet exposed", f"{ip}:{port}" + (f" -- {banner[:80]}" if banner else ""))
            findings.append(port)
            record(f"[MEDIUM] Telnet service on {port}/tcp (cleartext login)"
                   + (f": {banner[:200]}" if banner else ""))
        else:
            kit.warn(f"{port}/tcp open but does not speak Telnet"
                     + (f" (banner: {banner[:80]})" if banner else ""))
            record(f"{port}/tcp open, not Telnet" + (f": {banner[:200]}" if banner else ""))
    if not findings:
        kit.good("Telnet is not exposed.")
    return findings


def attack(web):
    netmisc(web)
