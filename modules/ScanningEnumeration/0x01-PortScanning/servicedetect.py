#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Service detection -- connect scan plus banner grabbing on the open ports."""

from __future__ import annotations

import re
import socket
import ssl
import time
from concurrent.futures import ThreadPoolExecutor

import core.variables as variables
from core.Core.colors import C, P, color
from core.methods import modkit as kit
from core.methods import portscan
from core.methods.print import pscan

info = ("Finds out which services the target runs: TCP connect scan, then a banner "
        "grab on every open port (waits for the service to talk first, then nudges "
        "it with an HTTP HEAD request; TLS ports are wrapped first). Shows the "
        "service and the first banner line. No root needed.")
searchinfo = "Service Detection"
properties = {
    "PORTS": ["Ports to scan (e.g. 21,22,80,8000-8100; empty = common ports)", ""],
    "TIMEOUT": ["Seconds to wait for a banner (default 2)", ""],
}

# well-known names for ports the OS service database lacks or names poorly
COMMON_PORTS = {
    20: "ftp-data", 21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns",
    67: "dhcp", 68: "dhcp", 69: "tftp", 80: "http", 109: "pop2", 110: "pop3",
    111: "rpcbind", 123: "ntp", 137: "netbios-ns", 138: "netbios-dgm",
    139: "netbios-ssn", 143: "imap", 156: "sql-server", 161: "snmp", 162: "snmptrap",
    179: "bgp", 389: "ldap", 443: "https", 445: "microsoft-ds", 512: "exec",
    513: "login", 546: "dhcpv6-client", 547: "dhcpv6-server", 636: "ldaps",
    993: "imaps", 995: "pop3s", 1099: "rmiregistry", 2049: "nfs", 2082: "cpanel",
    2083: "cpanel-ssl", 2086: "whm", 2087: "whm-ssl", 2121: "ftp", 3306: "mysql",
    3632: "distcc", 5061: "sip-tls", 5432: "postgresql", 5900: "vnc", 6000: "x11",
    6379: "redis", 6667: "irc", 8009: "ajp13", 8080: "http-proxy", 8180: "http",
    8443: "https-alt", 10000: "webmin", 27017: "mongodb",
}
# ports where we speak first (HTTP) instead of waiting for a greeting
WEB_PORTS = {80, 81, 443, 591, 3000, 5000, 8000, 8008, 8080, 8081, 8180, 8443, 8888, 9443}
TLS_PORTS = {443, 465, 636, 993, 995, 2083, 2087, 5061, 8443, 9443}

# (banner regex, service) -- first match wins
SIGNATURES = [
    (r"^SSH-", "ssh"),
    (r"^HTTP/\d", "http"),
    (r"^220[ -].*ftp", "ftp"),
    (r"^220[ -].*(smtp|mail|postfix|exim|sendmail)", "smtp"),
    (r"^\+OK", "pop3"),
    (r"^\* (OK|PREAUTH)", "imap"),
    (r"^RFB \d", "vnc"),
    (r"mysql|mariadb", "mysql"),
    (r"^-(ERR|NOAUTH)|^\+PONG", "redis"),
    (r"^AMQP", "amqp"),
]
SIGNATURES = [(re.compile(rx, re.I), name) for rx, name in SIGNATURES]

READ_SIZE = 2048
BANNER_WIDTH = 60


def _read(sock) -> bytes:
    try:
        return sock.recv(READ_SIZE)
    except (socket.timeout, OSError):
        return b""


def _nudge(sock, host: str) -> bytes:
    try:
        sock.sendall(f"HEAD / HTTP/1.0\r\nHost: {host}\r\nUser-Agent: {kit.USER_AGENT}\r\n\r\n".encode())
    except OSError:
        return b""
    return _read(sock)


def grab(ip: str, port: int, host: str = "", timeout: float = 2.0) -> tuple[bytes, bool]:
    """Banner of ip:port and whether TLS was used; b'' if the service stays silent."""
    tls = port in TLS_PORTS
    try:
        sock = socket.create_connection((ip, port), timeout=timeout)
    except OSError:
        return b"", False
    try:
        if tls:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            try:
                sock = ctx.wrap_socket(sock, server_hostname=host or None)
            except (ssl.SSLError, OSError):
                sock.close()
                tls = False  # not TLS after all: start over in plaintext
                sock = socket.create_connection((ip, port), timeout=timeout)
        banner = b"" if port in WEB_PORTS else _read(sock)
        return banner or _nudge(sock, host or ip), tls
    except OSError:
        return b"", tls
    finally:
        sock.close()


def first_line(banner: bytes) -> str:
    """First printable line of a banner; for HTTP, the status plus Server header."""
    text = banner.decode("utf-8", errors="replace")
    lines = [re.sub(r"[^\x20-\x7e]+", " ", l).strip() for l in text.splitlines()]
    lines = [l for l in lines if l]
    if not lines:
        return ""
    line = lines[0]
    if line.startswith("HTTP/"):
        server = next((l.split(":", 1)[1].strip() for l in lines[1:]
                       if l.lower().startswith("server:")), "")
        if server:
            line = f"{line} ({server})"
    return line


def identify(port: int, banner: str, tls: bool = False) -> str:
    for rx, name in SIGNATURES:
        if rx.search(banner):
            if name == "http" and tls:
                return "https"
            return name
    return COMMON_PORTS.get(port) or portscan.service(port)


def report(rows: list[tuple[int, str, str]]) -> None:
    line = f"{P}    +--------+------------------+{'-' * (BANNER_WIDTH + 2)}+{color.END}"
    print(line)
    print(f"{P}    |{C}  PORT  {P}|{C}  SERVICE         {P}|{C} {'BANNER':<{BANNER_WIDTH}} {P}|{color.END}")
    print(line)
    for port, name, banner in rows:
        print(f"{P}    |{C} {port:>6} {P}|{C}  {name:<16.16}{P}|"
              f"{C} {banner or '-':<{BANNER_WIDTH}.{BANNER_WIDTH}} {P}|{color.END}")
    print(line)


def servicedetect(web):
    pscan("service detection")
    ports = portscan.ports_option(properties)
    if not ports:
        kit.bad("No valid ports to scan.")
        return []
    timeout = max(0.2, kit.number(properties, "TIMEOUT", "Seconds to wait for a banner", 2))
    portscan.warn_tor()
    ip = portscan.resolve_ip(web)
    if not ip:
        return []

    host = kit.host(web)
    kit.info(f"Scanning {len(ports)} ports on {host} ({ip})...")
    start = time.time()
    try:
        open_ports = portscan.connect_scan(ip, ports)
        if open_ports:
            kit.info(f"Grabbing banners from {len(open_ports)} open port(s)...")
        workers = max(1, min(variables.processes * 4, len(open_ports) or 1, 64))
        with ThreadPoolExecutor(max_workers=workers) as pool:
            grabs = list(pool.map(lambda p: grab(ip, p, host, timeout), open_ports))
    except KeyboardInterrupt:
        kit.bad("Scan interrupted by user.")
        return []
    elapsed = time.time() - start

    rows = []
    for port, (raw, tls) in zip(open_ports, grabs):
        banner = first_line(raw)
        rows.append((port, identify(port, banner, tls), banner))

    record = kit.Recorder(web, kit.PORTSCAN, "servicedetect")
    if rows:
        kit.good(f"{len(rows)} port(s) open")
        print()
        report(rows)
        record("Port:Service >>\n" + "\n".join(
            f"{p}:{name}" + (f" | {banner}" if banner else "") for p, name, banner in rows))
    else:
        kit.bad("No open ports found!")
        record("No open ports found.")
    if len(ports) > len(rows):
        kit.info(f"{len(ports) - len(rows)} closed ports not shown")
    kit.good(f"Host {host} scanned in {elapsed:.2f} seconds")
    return rows


def attack(web):
    servicedetect(web)
