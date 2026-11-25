#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`netinfo` console command: local addresses, interface and public/exit IP."""

from __future__ import annotations

import platform
import socket
import subprocess

import core.variables as vars
from core.Core.colors import C, G, O, color
from core.methods.tor import IP_URL, session


def _default_interface() -> str:
    """Interface of the default route (Linux `ip route`), else the configured one."""
    try:
        out = subprocess.run(["ip", "route", "show", "default"], capture_output=True,
                             text=True, timeout=5).stdout.split()
        return out[out.index("dev") + 1]
    except (OSError, ValueError, IndexError, subprocess.SubprocessError):
        return vars.interface


def _mac(iface: str) -> str:
    try:
        with open(f"/sys/class/net/{iface}/address") as fh:
            return fh.read().strip()
    except OSError:
        return "unknown"


def _local_ip() -> str:
    # connecting a UDP socket sends nothing; it just picks the outgoing address
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("192.0.2.1", 9))
            return s.getsockname()[0]
    except OSError:
        return "unknown"


def _public_ip() -> str:
    """Public IP as seen by targets: the Tor exit IP while `tor on` is active."""
    try:
        return session().get(IP_URL, timeout=15).text.strip()
    except Exception as e:
        return f"unavailable ({type(e).__name__})"


def info() -> None:
    iface = _default_interface()
    rows = [
        ("Mac Address", _mac(iface)),
        ("Local address", _local_ip()),
        ("Public IP" + (" (Tor exit)" if vars.tor else ""), _public_ip()),
        ("Tor", "ON (verified)" if vars.tor else "OFF"),
        ("Operating System", platform.system()),
        ("Name", platform.node()),
        ("Interface", iface),
    ]
    print()
    for label, value in rows:
        print(f"  |:  {O}{label}:{C}{color.TR3}{C}{G}{value}{C}{color.TR2}{C}")
    print()
