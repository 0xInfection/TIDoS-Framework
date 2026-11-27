#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Threat intelligence -- passive recon (checks public block/threat lists)."""

from __future__ import annotations

import ipaddress
import re
import socket
from concurrent.futures import ThreadPoolExecutor
from typing import NamedTuple
from urllib.parse import urlsplit

import requests

from core.methods import modkit as kit
from core.methods.print import posintpas

info = "Find out if the target site is harmful or not."
searchinfo = "Threat Intelligence Module"
properties = {}


class Feed(NamedTuple):
    name: str
    url: str
    kind: str     # "ip": list of IPs/CIDRs, "host": list of domains or URLs
    verdict: str  # what a hit means


BLOCKLIST_DE = "https://lists.blocklist.de/lists/{}.txt"

FEEDS = [
    Feed("BlockList.de SSH", BLOCKLIST_DE.format("ssh"), "ip", "attacks on SSH services"),
    Feed("BlockList.de Mail", BLOCKLIST_DE.format("mail"), "ip", "attacks on SMTP services"),
    Feed("BlockList.de SIP", BLOCKLIST_DE.format("sip"), "ip", "attacks on SIP / VoIP services"),
    Feed("BlockList.de FTP", BLOCKLIST_DE.format("ftp"), "ip", "attacks on FTP services"),
    Feed("BlockList.de POP3", BLOCKLIST_DE.format("pop3"), "ip", "attacks on POP3 services"),
    Feed("BlockList.de IMAP", BLOCKLIST_DE.format("imap"), "ip", "attacks on IMAP services"),
    Feed("BlockList.de Bots", BLOCKLIST_DE.format("bots"), "ip", "acting as HTTPD / bad bot"),
    Feed("BlockList.de Strong IPs", BLOCKLIST_DE.format("strongips"), "ip", "persistent attacks (strong IPs)"),
    Feed("BlockList.de Apache", BLOCKLIST_DE.format("apache"), "ip", "attacks on Apache services"),
    Feed("BlockList.de Brute-force", BLOCKLIST_DE.format("bruteforcelogin"), "ip", "brute-force logins"),
    Feed("Emerging Threats", "https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt",
         "ip", "listed in the Emerging Threats block list"),
    Feed("Emerging Threats Compromised", "https://rules.emergingthreats.net/blockrules/compromised-ips.txt",
         "ip", "known compromised host"),
    Feed("Binary Defense", "https://www.binarydefense.com/banlist.txt", "ip", "banned by the Artillery feed"),
    Feed("Feodo Tracker", "https://feodotracker.abuse.ch/downloads/ipblocklist.txt", "ip", "botnet C2 server"),
    Feed("Project Honey Pot", "https://www.projecthoneypot.org/list_of_ips.php", "ip", "malicious activity"),
    Feed("OpenPhish", "https://openphish.com/feed.txt", "host", "hosting phishing pages"),
    Feed("Phishing Army", "https://phishing.army/download/phishing_army_blocklist.txt", "host", "phishing domain"),
]

IP_RX = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}(?:/\d{1,2})?\b")


def listed(feed: Feed, body: str, host: str, ip: str) -> bool:
    """Exact match of the target's IP (or CIDR containing it) / hostname."""
    if feed.kind == "ip":
        if not ip:
            return False
        tokens = IP_RX.findall(body)
        if ip in tokens:
            return True
        addr = ipaddress.ip_address(ip)
        for cidr in (t for t in tokens if "/" in t):
            try:
                if addr in ipaddress.ip_network(cidr, strict=False):
                    return True
            except ValueError:
                continue
        return False
    wanted = {host.lower(), ip}
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name = urlsplit(line).hostname if "://" in line else line.split()[0]
        if (name or "").lower() in wanted:
            return True
    return False


def fetch(session, feed: Feed) -> str | Exception:
    try:
        resp = session.get(feed.url)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        return e


def threatintel(web):
    posintpas("threat intelligence")
    host = kit.host(web)
    try:
        ip = host if kit.is_ip(host) else socket.gethostbyname(host)
        kit.found("DNS", ip)
    except OSError:
        ip = ""
        kit.warn(f"Could not resolve {host}; only domain-based lists will be checked.")

    kit.info(f"Checking {len(FEEDS)} threat lists (data refreshed daily by their maintainers) ...")
    session = kit.http(timeout=30)
    with ThreadPoolExecutor(max_workers=8) as pool:
        bodies = list(pool.map(lambda f: fetch(session, f), FEEDS))

    flagged, failed = [], []
    for feed, body in zip(FEEDS, bodies):
        if isinstance(body, Exception):
            kit.bad(f"{feed.name}: list unavailable ({body.__class__.__name__})")
            failed.append(feed.name)
        elif listed(feed, body, host, ip):
            kit.warn(f"{feed.name}: {host} is listed -- {feed.verdict}")
            flagged.append(feed.name.lower())
        else:
            kit.good(f"{feed.name}: {host} is clean")

    if flagged:
        kit.warn(f"{host} appeared on {len(flagged)} threat list(s).")
        data = f"{host} appeared as a threat on the following lists: {flagged}"
    else:
        kit.good(f"{host} seems to be clean ({len(FEEDS) - len(failed)} list(s) checked).")
        data = f"{host} seems to be clean."
    kit.Recorder(web, kit.PASSIVE, "threatintel")(data)
    return flagged


def attack(web):
    threatintel(web)
