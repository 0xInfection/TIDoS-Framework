#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""
Port-scanning helpers shared by the port scanner modules.

    parse_ports("22,80,8000-8100") -> [22, 80, 8000, ...]
    connect_scan(ip, ports)        -> open ports (concurrent TCP connect)
    report(rows)                   -> boxed PORT / STATE / SERVICE table

Connect scans need no privileges. Raw-packet scans (SYN/FIN/XMAS...) live in
their own modules and can reuse parse_ports(), service() and report().
"""

from __future__ import annotations

import socket
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable

import core.variables as variables
from core.Core.colors import C, P, color
from core.methods import modkit as kit

COMMON_PORTS = [20, 21, 22, 23, 25, 53, 67, 68, 69, 80, 109, 110, 111, 123, 137, 143, 156,
                161, 162, 179, 389, 443, 445, 512, 513, 546, 547, 636, 993, 995, 1099,
                2049, 2121, 3306, 5432, 5900, 6000, 6667, 8080, 8180, 8443, 10000]
TIMEOUT = 1.0


def parse_ports(spec: str) -> list[int]:
    """'22,80,8000-8010' -> sorted unique ports; invalid chunks are skipped."""
    ports = set()
    for chunk in spec.replace(" ", "").split(","):
        if not chunk:
            continue
        try:
            lo, _, hi = chunk.partition("-")
            ports.update(range(int(lo), int(hi or lo) + 1))
        except ValueError:
            kit.warn(f"Ignoring invalid port spec '{chunk}'")
    return sorted(p for p in ports if 0 < p < 65536)


def ports_option(properties: dict, key: str = "PORTS",
                 default: Iterable[int] = COMMON_PORTS) -> list[int]:
    """Resolve a PORTS-style option; empty means `default`."""
    spec = kit.option(properties, key, "Ports to scan (e.g. 22,80,8000-8100; enter for common ports)", "")
    return parse_ports(spec) if spec else list(default)


def resolve_ip(target) -> str:
    """IPv4 of the target, or '' after printing why not."""
    ip = kit.resolve(target)
    if not ip:
        kit.bad(f"Cannot resolve {kit.host(target)}.")
    return ip


def is_open(ip: str, port: int, timeout: float = TIMEOUT) -> bool:
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except OSError:
        return False


def connect_scan(ip: str, ports: list[int], timeout: float = TIMEOUT) -> list[int]:
    """Concurrent TCP connect scan; returns the open ports in order."""
    if not ports:
        return []
    workers = max(1, min(variables.processes * 4, len(ports), 256))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        states = pool.map(lambda p: is_open(ip, p, timeout), ports)
        return [p for p, up in zip(ports, states) if up]


def service(port: int, proto: str = "tcp") -> str:
    try:
        return socket.getservbyport(port, proto)
    except OSError:
        return "unknown"


def warn_tor() -> None:
    if variables.tor:
        kit.warn("Port scans connect directly (not via the SOCKS proxy) and do NOT go through Tor.")


def report(rows: Iterable[tuple[int, str]]) -> None:
    """Print (port, state) rows as a table with service names."""
    rows = list(rows)
    if not rows:
        return
    line = f"{P}    +--------+---------------+------------------+{color.END}"
    print(line)
    print(f"{P}    |{C}  PORT  {P}|{C}     STATE     {P}|{C}  SERVICE         {P}|{color.END}")
    print(line)
    for port, state in rows:
        print(f"{P}    |{C} {port:>6} {P}|{C} {state:^13.13} {P}|{C}  {service(port):<16.16}{P}|{color.END}")
    print(line)


def run(web, properties: dict, section: tuple, lvl2: str) -> list:
    """Full connect-scan module flow: options, resolve, scan, report, record."""
    host = kit.host(web)
    ports = ports_option(properties)
    if not ports:
        kit.bad("No valid ports to scan.")
        return []
    warn_tor()
    ip = resolve_ip(web)
    if not ip:
        return []

    kit.info(f"Scanning {len(ports)} ports on {host} ({ip})...")
    start = time.time()
    try:
        open_ports = connect_scan(ip, ports)
    except KeyboardInterrupt:
        kit.bad("Scan interrupted by user.")
        return []
    elapsed = time.time() - start

    record = kit.Recorder(web, section, lvl2)
    if open_ports:
        kit.good(f"{len(open_ports)} port(s) open")
        print()
        report((p, "OPEN") for p in open_ports)
        record(f"Open Ports: {open_ports}")
    else:
        kit.bad("No open ports found!")
        record("No open ports found.")
    kit.info(f"{len(ports) - len(open_ports)} closed ports not shown")
    kit.good(f"Host {host} scanned in {elapsed:.2f} seconds")
    return open_ports
