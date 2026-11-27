#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Same-site scripting -- localhost.<domain> resolving to the loopback address."""

from __future__ import annotations

import ipaddress
import os

from core.methods import dnsmisc
from core.methods import modkit as kit
from core.methods.inject import marker
from core.methods.print import pvln

info = ("This module hunts for Same-Site Scripting: a 'localhost.<domain>' DNS record (or any "
        "known subdomain) pointing to 127.0.0.1/::1/0.0.0.0. A page served by any local "
        "service on the victim's machine then counts as same-site with the target and can "
        "read cookies scoped to the domain. Subdomains found earlier by the Subdomain Gatherer "
        "(tmp/logs/<host>-logs/<host>-subdomains.lst) are checked too.")
searchinfo = "Same Site Scripting"
properties = {}


def loopback(ips: list[str]) -> list[str]:
    out = []
    for ip in ips:
        try:
            a = ipaddress.ip_address(ip)
        except ValueError:
            continue
        if a.is_loopback or a.is_unspecified:
            out.append(ip)
    return out


def known_subdomains(web) -> list[str]:
    logs = kit.logdir(web)
    stem = os.path.basename(logs)[:-len("-logs")]
    path = os.path.join(logs, f"{stem}-subdomains.lst")
    return kit.wordlist(path) if os.path.exists(path) else []


def ssscript(web):
    pvln("same-site scripting")
    record = kit.Recorder(web, kit.MISCONFIG, "ssscript")
    host = kit.host(web)
    if kit.is_ip(host):
        kit.bad("Target is an IP address; same-site scripting needs a domain name.")
        record("Not applicable: target is an IP address.")
        return []
    dnsmisc.warn_tor()
    domain = kit.domain(web)

    names = list(dict.fromkeys(f"localhost.{d}" for d in (domain, host)))
    subs = known_subdomains(web)
    if subs:
        kit.info(f"Also checking {len(subs)} known subdomains.")
    names += [s for s in subs if s not in names]

    wildcard = loopback(dnsmisc.addresses(f"{marker(10)}.{domain}"))
    if wildcard:
        kit.warn(f"Wildcard DNS of {domain} resolves to {', '.join(wildcard)}: "
                 "every name under it is affected.")

    findings = []
    for name in names:
        ips = dnsmisc.addresses(name)
        bad = loopback(ips)
        if bad:
            line = f"{name} resolves to {', '.join(bad)}"
            kit.found("Same-site scripting", line)
            findings.append(line)
        elif name.startswith("localhost."):
            kit.bullet(f"{name}: " + (", ".join(ips) if ips else "does not resolve"))

    if wildcard and not findings:
        findings.append(f"*.{domain} (wildcard) resolves to {', '.join(wildcard)}")
    if not findings:
        kit.good("No name of the domain points to the loopback address.")
        record("Not vulnerable to same-site scripting.")
        return []
    for f in findings:
        record(f"[MEDIUM] Same-site scripting: {f}")
    kit.info("Remove these records: any local service on a visitor's machine becomes same-site "
             "with the target.")
    return findings


def attack(web):
    ssscript(web)
