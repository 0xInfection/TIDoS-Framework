#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""OS fingerprinting -- best-effort OS guess from TTL, banners, Censys and nmap."""

from __future__ import annotations

import re
import socket
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from core.methods import modkit as kit
from core.methods import portscan
from core.methods.print import pscan
from modules.ScanningEnumeration.getcensys import censys_os

info = ("This module tries to find out the OS the target is using. It combines the TTL "
        "of a ping reply, service banners of open ports, Censys host data (when "
        "CENSYS_API_TOKEN is set) and, when running as root, an nmap OS scan, and labels "
        "the confidence of its guess.")
searchinfo = "OS Fingerprinter"
properties = {
    "PORTS": ["Ports to grab banners from (e.g. 21,22,80; empty: common ports)", ""],
    "NMAP": ["Run an nmap OS scan (nmap -O, needs root) (y/n)", "y"],
}

# weight of each evidence source in the final verdict
WEIGHTS = {"nmap": 4, "censys": 3, "banner": 2, "ttl": 1}
FAMILIES = [
    ("Windows", r"windows|microsoft|win32|win64|\biis\b"),
    ("macOS", r"darwin|mac ?os"),
    ("BSD", r"freebsd|openbsd|netbsd|dragonfly"),
    ("Linux", r"linux|ubuntu|debian|centos|red ?hat|rhel|fedora|alpine|suse|raspbian|"
              r"amazon linux|almalinux|rocky"),
    ("Solaris", r"solaris|sunos"),
    ("Cisco IOS", r"cisco|\bios\b"),
]
DISTRO = re.compile(r"ubuntu|debian|centos|red ?hat|fedora|alpine|suse|raspbian|"
                    r"freebsd|openbsd|netbsd|win32|win64", re.I)
HTTP_PORTS = {80, 443, 8000, 8008, 8080, 8443, 8888}
# (initial TTL, family) -- the reply TTL is the initial one minus the hops
UNIX = "Unix-like"
TTLS = [(64, UNIX), (128, "Windows"), (255, "Solaris/network device")]


def family(text: str) -> str:
    for name, pattern in FAMILIES:
        if re.search(pattern, text, re.I):
            return name
    return ""


def ttl_guess(ip: str) -> str:
    """OS family implied by the TTL of a ping reply ('' if no reply)."""
    out = kit.command(["ping", "-c", "1", ip], timeout=10) or ""
    match = re.search(r"ttl[=:](\d+)", out, re.I)
    if not match:
        kit.bad("No ping reply (ICMP filtered?); skipping the TTL check.")
        return ""
    ttl = int(match.group(1))
    initial, fam = next((i, f) for i, f in TTLS if ttl <= i)
    kit.found("Ping TTL", f"{ttl} (initial {initial}, ~{initial - ttl} hops) -> {fam}")
    return fam


def banner(ip: str, port: int, web) -> str:
    """Server banner of a port: Server/X-Powered-By headers for HTTP,
    the greeting line for talk-first services (SSH, FTP, SMTP...)."""
    if port in HTTP_PORTS:
        scheme = "https" if port in (443, 8443) else "http"
        try:
            resp = kit.http(timeout=8).head(f"{scheme}://{kit.host(web)}:{port}/",
                                            allow_redirects=False)
        except Exception:
            return ""
        return " ".join(filter(None, (resp.headers.get("Server"),
                                      resp.headers.get("X-Powered-By"))))
    try:
        with socket.create_connection((ip, port), timeout=3) as sock:
            sock.settimeout(3)
            data = sock.recv(512)
    except OSError:
        return ""
    return data.decode("latin-1").strip().splitlines()[0] if data.strip() else ""


def banner_guesses(ip: str, ports: list[int], web) -> list[tuple[str, str]]:
    """(family, evidence) pairs from service banners of the open ports."""
    open_ports = portscan.connect_scan(ip, ports)
    if not open_ports:
        kit.bad("No open ports to grab banners from.")
        return []
    kit.info(f"Open ports: {', '.join(map(str, open_ports))}")
    with ThreadPoolExecutor(max_workers=min(16, len(open_ports))) as pool:
        banners = list(pool.map(lambda p: banner(ip, p, web), open_ports))
    guesses = []
    for port, text in zip(open_ports, banners):
        if not text:
            continue
        kit.found(f"Banner {port}/{portscan.service(port)}", text)
        fam = family(text)
        if fam:
            distro = DISTRO.search(text)
            guesses.append((fam, distro.group(0) if distro else text))
    if not guesses:
        kit.info("No banner reveals the operating system.")
    return guesses


def nmap_guess(ip: str) -> str:
    """'Running:' / 'OS details:' of an nmap OS scan ('' if no match)."""
    out = kit.command(["nmap", "-Pn", "-O", "--osscan-guess", "-F", "-T4", ip], timeout=600)
    if not out:
        return ""
    found = {}
    for label in ("Running", "Aggressive OS guesses", "OS details", "OS CPE"):
        match = re.search(rf"^{label}(?: \(JUST GUESSING\))?:\s*(.+)$", out, re.M)
        if match:
            found[label] = match.group(1).strip()
            kit.found(f"nmap {label}", found[label])
    if not found:
        kit.bad("nmap found no OS match.")
    return found.get("OS details") or found.get("Running") or found.get("Aggressive OS guesses", "")


def merge_unix(evidence: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    """A 64 TTL supports whichever Unix the other sources name."""
    unix = [f for s, f, _ in evidence if s != "ttl" and f in ("Linux", "macOS", "BSD")]
    if not unix:
        return evidence
    return [(s, unix[-1] if f == UNIX else f, d) for s, f, d in evidence]


def verdict(evidence: list[tuple[str, str, str]]) -> tuple[str, str]:
    """(family, confidence) from (source, family, detail) evidence."""
    scores = Counter()
    for source, fam, _ in evidence:
        scores[fam] += WEIGHTS[source]
    fam = scores.most_common(1)[0][0]
    sources = {s for s, f, _ in evidence if f == fam}
    contested = len(scores) > 1
    if sources & {"nmap", "censys"} or (len(sources) >= 2 and not contested):
        confidence = "high" if not contested else "medium"
    elif "banner" in sources:
        confidence = "medium" if not contested else "low"
    else:
        confidence = "low"
    return fam, confidence


def osdetect(web):
    pscan("os fingerprinting")
    ip = portscan.resolve_ip(web)
    if not ip:
        return ""
    ports = portscan.ports_option(properties)
    use_nmap = kit.flag(properties, "NMAP", "Run an nmap OS scan (needs root)?", True)
    portscan.warn_tor()
    evidence = []

    kit.info("[1] Checking the TTL of a ping reply...")
    fam = ttl_guess(ip)
    if fam:
        evidence.append(("ttl", fam, "ping TTL"))

    kit.info("[2] Grabbing service banners...")
    for fam, detail in banner_guesses(ip, ports, web):
        evidence.append(("banner", fam, detail))

    kit.info("[3] Querying Censys host data...")
    token = kit.apikey("CENSYS_API_TOKEN", quiet=True)
    if not token:
        kit.info("CENSYS_API_TOKEN not set; skipping Censys.")
    else:
        os_name = censys_os(ip, token)
        if os_name:
            kit.found("Censys OS", os_name)
            evidence.append(("censys", family(os_name) or os_name, os_name))
        elif os_name == "":
            kit.info("Censys has no OS for this host.")

    if use_nmap:
        kit.info("[4] Running an nmap OS scan...")
        if not kit.is_root():
            kit.warn("nmap OS detection needs raw packets (root); skipping. Run TIDoS as root to enable it.")
        else:
            detail = nmap_guess(ip)
            if detail:
                evidence.append(("nmap", family(detail) or detail, detail))

    record = kit.Recorder(web, kit.SCAN, "osdetect")
    print()
    if not evidence:
        kit.bad("Could not fingerprint the operating system.")
        record("No OS matches found.")
        return ""
    evidence = merge_unix(evidence)
    fam, confidence = verdict(evidence)
    details = "; ".join(f"{s}: {d}" for s, f, d in evidence if f == fam)
    kit.found("Operating System", f"{fam} (confidence: {confidence})")
    kit.bullet(f"evidence -- {details}")
    others = sorted({f for _, f, _ in evidence if f != fam})
    if others:
        kit.warn(f"Conflicting hints: {', '.join(others)}")
    record(f"{fam} (confidence: {confidence}; {details})")
    kit.good("OS Fingerprinting Module Completed!")
    return fam


def attack(web):
    osdetect(web)
