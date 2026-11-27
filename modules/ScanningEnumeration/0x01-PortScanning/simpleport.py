#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Simple port scanner -- quick TCP connect check of a port list."""

import time

from core.methods import modkit as kit
from core.methods import portscan
from core.methods.print import pscan

info = ("A simple port scanner: quickly checks which ports accept TCP connections "
        "(no root needed). PORTS accepts a comma separated list with ranges, "
        "e.g. 22,80,8000-8100; empty scans the common ports.")
searchinfo = "Simple Port Scanner"
properties = {
    "PORTS": ["Ports to scan (e.g. 21,22,80,8000-8100; empty = common ports)", ""],
}


def simpleport(web):
    pscan("simple port scanner")
    ports = portscan.ports_option(properties)
    if not ports:
        kit.bad("No valid ports to scan.")
        return []
    portscan.warn_tor()
    ip = portscan.resolve_ip(web)
    if not ip:
        return []

    host = kit.host(web)
    kit.info(f"Scanning {len(ports)} ports on {host} ({ip})...")
    start = time.time()
    try:
        open_ports = portscan.connect_scan(ip, ports)
    except KeyboardInterrupt:
        kit.bad("Scan interrupted by user.")
        return []
    elapsed = time.time() - start

    record = kit.Recorder(web, kit.PORTSCAN, "simpleport")
    if open_ports:
        kit.good(f"{len(open_ports)} port(s) open")
        print()
        portscan.report((p, "OPEN") for p in open_ports)
        record(f"Open Ports: {open_ports}")
    else:
        kit.bad("No open ports found!")
        record("No open ports found.")
    if len(ports) > len(open_ports):
        kit.info(f"{len(ports) - len(open_ports)} closed ports not shown")
    kit.good(f"Host {host} scanned in {elapsed:.2f} seconds")
    return open_ports


def attack(web):
    simpleport(web)
