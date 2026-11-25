#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TCP stealth scanner -- half-open SYN scan (needs root)."""

from core.methods import rawscan
from core.methods.print import pscan

info = ("TCP stealth (half-open SYN) scan: sends a SYN to every port, SYN/ACK means "
        "open, RST closed, silence or ICMP unreachable filtered. The handshake is never "
        "completed (a RST is sent back), so many services do not log the probe. Needs "
        "root.")
searchinfo = "TCP Stealth Scan"
properties = {
    "PORTS": ["Ports to scan (e.g. 21,22,80,8000-8100; empty = common ports)", ""],
    "TIMEOUT": ["Seconds to wait for replies (default 2)", ""],
    "VERBOSE": ["Show closed ports in the report too (y/n)", ""],
}


def tcpstealthscan(web):
    pscan("tcp stealth scan")
    return rawscan.run(web, properties, "syn", lvl2="tcpstealthscan")


def attack(web):
    tcpstealthscan(web)
