#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nmap frontend -- runs predefined nmap scan profiles and summarises the XML output."""

from __future__ import annotations

import re
import shlex
import time
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit

import core.variables as variables
from core.Core.colors import C, P, color
from core.methods import modkit as kit
from core.methods.print import pscan

TOR_PROXY = "socks4://127.0.0.1:9050"
WEB_PORTS = "80,443"

# name -> description, nmap arguments, default ports, needs root,
#         can be proxied through Tor, uses the target's web port(s)
PROFILES = {
    "basic": ("Basic port scan (top 1000 ports)", [], None, False, True, False),
    "ports": ("Scan only the ports given in PORTS", [], None, False, True, False),
    "fast": ("Fast scan of the 100 most common ports", ["-F"], None, False, True, False),
    "connect": ("TCP connect scan", ["-sT"], None, False, True, False),
    "syn": ("TCP SYN (half-open) scan", ["-sS"], None, True, False, False),
    "udp": ("UDP scan of common UDP services", ["-sU"], "123,161,162", True, False, False),
    "os": ("OS detection", ["-O"], None, True, False, False),
    "aggressive": ("OS, version, script detection and traceroute (-A)", ["-A"], None, True, False, False),
    "reflectors": ("Detect UDP DDoS reflectors",
                   ["-sU", "-Pn", "-n", "--script=ntp-monlist,dns-recursion,snmp-sysdescr"],
                   "U:19,53,123,161", True, False, False),
    "version": ("Service and version detection", ["-sV"], None, False, True, False),
    "scripts": ("Default NSE scripts with version detection", ["-sC", "-sV"], None, False, True, False),
    "titles": ("Gather page titles of web services", ["-sV", "--script=http-title"], None, False, True, True),
    "dnsbrute": ("Brute force DNS hostnames (subdomains)", ["--script=dns-brute"], "80", False, False, False),
    "xss": ("Detect stored / DOM based XSS",
            ["-sV", "--script=http-stored-xss,http-dombased-xss"], None, False, True, True),
    "sqli": ("Detect SQL injection", ["-sV", "--script=http-sql-injection"], None, False, True, True),
    "heartbleed": ("Detect the Heartbleed SSL vulnerability",
                   ["-sV", "--script=ssl-heartbleed"], "443", False, True, False),
    "evade": ("Firewall/IDS evasion: decoys, fragmented packets, slow timing",
              ["-sS", "-sV", "-T1", "--mtu", "24", "--data-length", "1227"], None, True, False, False),
    "webapps": ("Discover web applications in use", ["-sV", "--script=http-enum"], None, False, True, True),
}
DEFAULT_PROFILE = "basic"

# options that would clash with our XML-on-stdout output or change the targets
FORBIDDEN_EXTRA = ("-o", "-i", "--resume", "--stylesheet", "--webxml", "--proxies", "--proxy")

info = ("TIDoS frontend to the Nmap scanner. PROFILE selects the scan: "
        + ", ".join(PROFILES) + f" (default {DEFAULT_PROFILE}). PORTS overrides "
        "the profile's ports (nmap syntax, e.g. 22,80,U:53), TIMING sets the -T "
        "template (0-5), DECOY the decoys of the evade profile and EXTRA adds raw "
        "nmap arguments. syn, udp, os, aggressive, reflectors and evade need root. "
        "Nmap's SOCKS support only covers NSE and version probes, so with Tor on "
        "scans are refused unless LEAK=y; even then only TCP connect based "
        "profiles run, with NSE/version traffic proxied.")
searchinfo = "NMap Scanner"
properties = {
    "PROFILE": ["Scan profile: " + ", ".join(PROFILES), ""],
    "PORTS": ["Ports to scan, nmap syntax (e.g. 22,80,8000-8100,U:53)", ""],
    "TIMING": ["Timing template 0 (paranoid) - 5 (insane)", ""],
    "DECOY": ["Decoys for the evade profile (e.g. RND:5 or 1.2.3.4,ME)", ""],
    "EXTRA": ["Extra nmap arguments (e.g. --script=banner --top-ports 50)", ""],
    "TIMEOUT": ["Abort the scan after this many seconds", ""],
    "LEAK": ["With Tor on, scan anyway although nmap's port scan bypasses Tor (y/n)", ""],
}


def show_profiles() -> None:
    kit.info("Available scan profiles:")
    kit.kv_table((name, desc + (" [root]" if root else ""))
                 for name, (desc, _, _, root, _, _) in PROFILES.items())
    print()


def web_ports(web) -> str:
    """Explicit port of the target URL, else the usual web ports."""
    try:
        port = urlsplit(kit.url(web)).port
    except ValueError:
        port = None
    return str(port) if port else WEB_PORTS


def valid_target(host: str) -> bool:
    return bool(host) and not host.startswith("-") and bool(re.fullmatch(r"[A-Za-z0-9._:\[\]-]+", host))


def valid_ports(spec: str) -> bool:
    return bool(re.fullmatch(r"[TUS:0-9,\-]+", spec))


def extra_args(spec: str) -> list[str] | None:
    """Split EXTRA like a shell would (no shell involved); None if invalid."""
    try:
        args = shlex.split(spec)
    except ValueError as e:
        kit.bad(f"Invalid EXTRA arguments: {e}")
        return None
    for arg in args:
        if arg.startswith(FORBIDDEN_EXTRA):
            kit.bad(f"EXTRA may not contain '{arg}' (output, input and proxy options are managed by TIDoS).")
            return None
    return args


def build(host: str, profile: str, ports: str, timing: str, decoy: str, extra: list[str]) -> list[str]:
    _, args, _, _, _, _ = PROFILES[profile]
    if ports:  # nmap refuses -F together with an explicit port list
        args = [a for a in args if a != "-F"]
    cmd = ["nmap"] + args
    if variables.tor:
        cmd += [a for a in ("-sT", "-Pn") if a not in args] + ["--proxies", TOR_PROXY]
    if profile == "evade":
        cmd += ["-D", decoy]
    if ports:
        cmd += ["-p", ports]
    if timing:
        cmd.append(f"-T{timing}")
    return cmd + extra + ["-oX", "-", "--", host]


def parse(xml: str) -> list[dict]:
    """Hosts of an nmap -oX document: address, names, ports, OS and scripts.

    Raises ValueError with nmap's message when the run ended in an error.
    """
    root = ET.fromstring(xml)
    finished = root.find("runstats/finished")
    if finished is not None and finished.get("exit") == "error":
        raise ValueError(finished.get("errormsg") or "nmap exited with an error")
    hosts = []
    for node in root.iter("host"):
        status = node.find("status")
        entry = {
            "addr": next((a.get("addr") for a in node.findall("address")
                          if a.get("addrtype") in ("ipv4", "ipv6")), ""),
            "mac": next((f"{a.get('addr')} {a.get('vendor', '')}".strip() for a in node.findall("address")
                         if a.get("addrtype") == "mac"), ""),
            "state": status.get("state", "") if status is not None else "",
            "names": list(dict.fromkeys(h.get("name") for h in node.iter("hostname") if h.get("name"))),
            "ports": [],
            "os": [f"{m.get('name')} ({m.get('accuracy')}%)" for m in node.iter("osmatch")],
            "scripts": [(s.get("id"), s.get("output", "").strip())
                        for s in node.findall("hostscript/script")],
        }
        for port in node.iter("port"):
            state = port.find("state")
            svc = port.find("service")
            svc = svc.attrib if svc is not None else {}
            entry["ports"].append({
                "port": int(port.get("portid", 0)),
                "proto": port.get("protocol", "tcp"),
                "state": state.get("state", "") if state is not None else "",
                "service": svc.get("name", ""),
                "version": " ".join(v for v in (svc.get("product"), svc.get("version")) if v)
                           + (f" ({svc['extrainfo']})" if svc.get("extrainfo") else ""),
                "scripts": [(s.get("id"), s.get("output", "").strip()) for s in port.findall("script")],
            })
        hosts.append(entry)
    return hosts


def summary(host: dict) -> str:
    """Plain-text summary of one parsed host for the results database."""
    lines = [f"Host: {host['addr']} ({', '.join(host['names']) or 'no PTR'}) is {host['state']}"]
    if host["mac"]:
        lines.append(f"MAC: {host['mac']}")
    for p in host["ports"]:
        lines.append(f"{p['port']}/{p['proto']} {p['state']} {p['service']} {p['version']}".rstrip())
        lines += [f"  {sid}: {out}" for sid, out in p["scripts"]]
    if host["os"]:
        lines.append("OS: " + "; ".join(host["os"]))
    lines += [f"{sid}: {out}" for sid, out in host["scripts"]]
    return "\n".join(lines)


def table(ports: list[dict]) -> None:
    """PORT / STATE / SERVICE / VERSION table in the style of portscan.report()."""
    width = min(max([7] + [len(p["version"]) for p in ports]), 40)
    line = f"{P}    +-----------+---------------+------------------+{'-' * (width + 2)}+{color.END}"
    print(line)
    print(f"{P}    |{C}   PORT    {P}|{C}     STATE     {P}|{C}  SERVICE         "
          f"{P}|{C} {'VERSION'.ljust(width)} {P}|{color.END}")
    print(line)
    for p in ports:
        port = f"{p['port']}/{p['proto']}"
        print(f"{P}    |{C} {port:>9} {P}|{C} {p['state']:^13.13} {P}|{C}  {p['service'] or 'unknown':<16.16}"
              f"{P}|{C} {p['version'][:width].ljust(width)} {P}|{color.END}")
    print(line)


def script(name: str, output: str) -> None:
    kit.bullet(f"{name}: " + output.replace("\n", "\n" + " " * 7))


def show(host: dict) -> None:
    kit.found("Host", f"{host['addr']} ({', '.join(host['names']) or 'no PTR'}) is {host['state']}")
    if host["mac"]:
        kit.found("MAC", host["mac"])
    ports = [p for p in host["ports"] if p["state"] not in ("closed", "filtered")]
    if ports:
        print()
        table(ports)
        for p in ports:
            for sid, out in p["scripts"]:
                script(f"{p['port']}/{p['proto']} {sid}", out)
        print()
    else:
        kit.bad("No open ports found!")
    hidden = len(host["ports"]) - len(ports)
    if hidden:
        kit.info(f"{hidden} closed/filtered port(s) not shown")
    if host["os"]:
        kit.found("OS guess", "; ".join(host["os"][:3]))
    for sid, out in host["scripts"]:
        script(sid, out)


def nmapmain(web):
    pscan("nmap")
    host = kit.host(web)
    if not valid_target(host):
        kit.bad(f"Invalid target '{host}'.")
        return []

    if not str(properties["PROFILE"][1]).strip() and kit.interactive():
        show_profiles()
    profile = kit.option(properties, "PROFILE", "Scan profile", DEFAULT_PROFILE).lower()
    if profile not in PROFILES:
        kit.bad(f"Unknown profile '{profile}'. Choose one of: {', '.join(PROFILES)}")
        return []
    desc, _, default_ports, root, proxyable, web_profile = PROFILES[profile]
    if root and not kit.is_root():
        kit.bad(f"The '{profile}' profile needs raw sockets: run TIDoS as root.")
        return []
    if variables.tor:
        if not proxyable:
            kit.bad(f"The '{profile}' profile cannot be routed through Tor; turn Tor off "
                    "or pick a TCP connect based profile (basic, fast, connect, version, ...).")
            return []
        kit.warn("Nmap only sends NSE and version probes through its SOCKS proxy: host "
                 "discovery, the port scan itself and DNS go out directly, from your IP.")
        if not kit.flag(properties, "LEAK", "Scan anyway without full Tor coverage", False):
            kit.bad("Refusing to leak your address while Tor is on (set LEAK=y to scan anyway).")
            return []

    if web_profile:
        default_ports = web_ports(web)
    ports = kit.option(properties, "PORTS", "Ports to scan (nmap syntax, enter for profile default)",
                       default_ports or "").replace(" ", "")
    if profile == "ports" and not ports:
        kit.bad("The 'ports' profile needs PORTS (e.g. 22,80,8000-8100).")
        return []
    if ports and not valid_ports(ports):
        kit.bad(f"Invalid port specification '{ports}'.")
        return []
    timing = kit.option(properties, "TIMING", "Timing template 0-5 (enter for default)", "")
    if timing and timing not in ("0", "1", "2", "3", "4", "5"):
        kit.bad(f"Invalid timing template '{timing}' (use 0-5).")
        return []
    decoy = ""
    if profile == "evade":
        decoy = kit.option(properties, "DECOY", "Decoys (e.g. RND:5 or 1.2.3.4,ME)", "RND:5")
        if not re.fullmatch(r"[A-Za-z0-9.:,_-]+", decoy) or decoy.startswith("-"):
            kit.bad(f"Invalid decoy list '{decoy}'.")
            return []
    extra = extra_args(kit.option(properties, "EXTRA", "Extra nmap arguments (enter for none)", ""))
    if extra is None:
        return []
    timeout = kit.integer(properties, "TIMEOUT", "Scan timeout in seconds",
                          7200 if profile == "evade" else 900)

    if profile == "evade":
        kit.warn("This scan is extremely stealthy and therefore slow; limit PORTS to keep it short.")
    cmd = build(host, profile, ports, timing, decoy, extra)
    kit.info(f"Profile: {profile} -- {desc}")
    kit.info(f"Running: {' '.join(shlex.quote(a) for a in cmd)}")
    start = time.time()
    out = kit.command(cmd, timeout=max(30, timeout))
    record = kit.Recorder(web, kit.SCAN, "nmap", profile)
    if not out:
        record(f"Nmap {profile} scan failed.")
        return []

    try:
        hosts = parse(out)
    except ET.ParseError as e:
        kit.bad(f"Could not parse nmap output: {e}")
        print(out.rstrip())
        record(out)
        return []
    except ValueError as e:
        kit.bad(f"Nmap failed: {str(e).strip()}")
        record(f"Nmap {profile} scan failed: {e}")
        return []
    if not hosts:
        kit.bad(f"Host {host} seems down or did not respond (try EXTRA=-Pn).")
        record("Host down or not responding.")
        return []

    for entry in hosts:
        show(entry)
        record(summary(entry))
    kit.good(f"Nmap {profile} scan of {host} finished in {time.time() - start:.2f} seconds")
    return hosts


def attack(web):
    nmapmain(web)
