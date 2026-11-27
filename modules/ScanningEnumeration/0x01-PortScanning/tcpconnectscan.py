#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""TCP connect scanner -- full three-way handshake, no privileges needed."""

import time

from core.methods import modkit as kit
from core.methods import portscan
from core.methods.print import pscan

info = ("TCP connect scan: completes a full TCP handshake with every port, which "
        "works without root and through any OS but is easily logged. PORTS accepts "
        "a comma separated list with ranges, e.g. 22,80,8000-8100.")
searchinfo = "TCP Connect Scanner"
properties = {
    "PORTS": ["Ports to scan (e.g. 21,22,80,8000-8100; empty = common ports)", ""],
    "VERBOSE": ["Show closed ports in the report too (y/n)", ""],
}


def tcpconnectscan(web):
    pscan("tcp connect scan")
    ports = portscan.ports_option(properties)
    if not ports:
        kit.bad("No valid ports to scan.")
        return []
    verbose = kit.flag(properties, "VERBOSE", "Show closed ports too?", False)
    portscan.warn_tor()
    ip = portscan.resolve_ip(web)
    if not ip:
        return []

    host = kit.host(web)
    kit.info(f"Connecting to {len(ports)} ports on {host} ({ip})...")
    start = time.time()
    try:
        open_ports = portscan.connect_scan(ip, ports)
    except KeyboardInterrupt:
        kit.bad("Scan interrupted by user.")
        return []
    elapsed = time.time() - start

    record = kit.Recorder(web, kit.PORTSCAN, "tcpconnectscan")
    if open_ports:
        kit.good(f"{len(open_ports)} port(s) open")
        print()
        up = set(open_ports)
        shown = ports if verbose else open_ports
        portscan.report((p, "OPEN" if p in up else "CLOSED") for p in shown)
        record(f"Open Ports: {open_ports}")
    else:
        kit.bad("No open ports found!")
        record("No open ports found.")
    if not verbose and len(ports) > len(open_ports):
        kit.info(f"{len(ports) - len(open_ports)} closed ports not shown")
    kit.good(f"Host {host} scanned in {elapsed:.2f} seconds")
    return open_ports


def attack(web):
    tcpconnectscan(web)
