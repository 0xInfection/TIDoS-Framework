#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""E-mail spoofing -- SPF and DMARC analysis of the target's domain."""

from __future__ import annotations

from core.methods import dnsmisc
from core.methods import modkit as kit
from core.methods.mailauth import analyze_dmarc, analyze_spf, verdict
from core.methods.print import pvln

info = ("This module checks if the target's mail domain can be spoofed. It parses the SPF "
        "record (all-qualifier, redirect, include chain, the 10-DNS-lookup limit, overly broad "
        "ip4 ranges, multiple records) and the DMARC policy (p=, sp=, pct=, organisational "
        "fallback for subdomains). Without an enforced DMARC policy the visible From: header "
        "can be forged even when SPF is strict.")
searchinfo = "Mail Spoofer"
properties = {
    "DOMAIN": ["Mail domain to check (default: the target's registrable domain)", ""],
}


def mailspoof(web):
    pvln("mail spoofer")
    record = kit.Recorder(web, kit.MISCONFIG, "mailspoof")
    domain = kit.option(properties, "DOMAIN", "Mail domain", kit.domain(web)).lower().strip(".")
    if kit.is_ip(domain):
        kit.bad("Target is an IP address; set DOMAIN to the mail domain.")
        record("Not applicable: no mail domain.")
        return None
    dnsmisc.warn_tor()
    kit.info(f"Checking SPF/DMARC of {domain}")

    has_mx = bool(dnsmisc.mx(domain))
    spf, spf_notes = analyze_spf(domain, dnsmisc.txt)
    kit.found("SPF", spf)
    for n in spf_notes:
        kit.bullet(n)
    org = kit.domain(domain)
    dmarc, dmarc_notes = analyze_dmarc(domain, org, dnsmisc.txt)
    kit.found("DMARC", dmarc)
    for n in dmarc_notes:
        kit.bullet(n)
    if not has_mx:
        kit.info(f"{domain} has no MX record: a domain that sends no mail should publish "
                 "'v=spf1 -all' and 'p=reject'.")

    severity, sentence = verdict(spf, dmarc)
    if severity == "OK":
        kit.good(sentence[0].upper() + sentence[1:])
    else:
        kit.found(f"Mail spoofing [{severity}]", sentence)
    record(f"[{severity}] {domain}: {sentence}")
    record(f"SPF {spf}: " + "; ".join(spf_notes))
    record(f"DMARC {dmarc}: " + "; ".join(dmarc_notes))
    return severity


def attack(web):
    mailspoof(web)
