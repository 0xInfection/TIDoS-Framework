#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Subdomain gatherer -- concurrent DNS bruteforce plus passive sources."""

import os
import socket
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

import core.variables as variables
from core.methods import modkit as kit
from core.methods.print import posintact

info = ("Finds subdomains of the target's domain by concurrent DNS bruteforce "
        "(wildcard DNS aware) and passive sources (HackerTarget hostsearch, crt.sh "
        "certificate transparency). Results are stored in the database and in "
        "tmp/logs/<host>-logs/<host>-subdomains.lst.")
searchinfo = "Subdomain Gatherer"
properties = {
    "WORDLIST": ["Wordlist of subdomain labels to bruteforce", ""],
    "BRUTE": ["Bruteforce subdomains over DNS (y/n)", ""],
    "PASSIVE": ["Query passive sources: HackerTarget, crt.sh (y/n)", ""],
}

DEFAULT_WORDLIST = "files/fuzz-db/subdomain_paths.lst"
CLEAR_LINE = "\r\033[K"


def resolve(name):
    """Set of IPv4 addresses for `name` (empty if it does not resolve)."""
    try:
        return set(socket.gethostbyname_ex(name)[2])
    except (OSError, UnicodeError):
        return set()


def bruteforce(domain, labels):
    wildcard = resolve(f"{uuid.uuid4().hex[:16]}.{domain}")
    if wildcard:
        kit.warn(f"Wildcard DNS detected ({', '.join(sorted(wildcard))}); "
                 "ignoring hits that resolve only there.")

    names = [f"{label.strip('.')}.{domain}" for label in labels]
    workers = max(1, min(variables.processes, 64))
    progress = sys.stdout.isatty()
    found = {}
    kit.info(f"Bruteforcing {len(names)} names with {workers} threads...")
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(resolve, n): n for n in names}
        for done, fut in enumerate(as_completed(futures), 1):
            name, ips = futures[fut], fut.result()
            if ips and not ips <= wildcard:
                found[name] = ips
                if progress:
                    print(CLEAR_LINE, end="")
                kit.found("Subdomain found", f"{name}  [{', '.join(sorted(ips))}]")
            if progress:
                print(f"{CLEAR_LINE} [*] {done}/{len(names)} names checked", end="", flush=True)
    if progress:
        print(CLEAR_LINE, end="")
    return found


def hackertarget(session, domain):
    text = kit.hackertarget("hostsearch", domain, timeout=40)
    if text is None:
        return None  # kit already said why
    return [line.split(",")[0] for line in text.splitlines() if "," in line]


def crtsh(session, domain):
    r = session.get("https://crt.sh/", params={"q": f"%.{domain}", "output": "json"})
    r.raise_for_status()
    return [n for entry in r.json() for n in entry.get("name_value", "").split("\n")]


def passive(domain):
    session = kit.http(timeout=40)
    names = set()
    for label, source in (("HackerTarget", hackertarget), ("crt.sh", crtsh)):
        kit.info(f"Querying {label}...")
        try:
            hits = source(session, domain)
        except Exception as e:
            kit.bad(f"{label} failed: {str(e)[:120] or type(e).__name__}")
            continue
        if hits is None:
            continue
        hits = {h.strip().lower().lstrip("*.") for h in hits}
        hits = {h for h in hits if h.endswith("." + domain)}
        kit.good(f"{label}: {len(hits)} subdomains")
        names |= hits
    return names


def subdom(web):
    posintact("subdomain gatherer")
    record = kit.Recorder(web, kit.ACTIVE, "subdom")
    domain = kit.domain(web)
    if kit.is_ip(domain):
        kit.bad("Target is an IP address; subdomain enumeration needs a domain name.")
        return []

    results = set()
    if kit.flag(properties, "BRUTE", "Bruteforce subdomains over DNS", True):
        labels = kit.wordlist(kit.option(properties, "WORDLIST", "Subdomain wordlist",
                                         DEFAULT_WORDLIST))
        if labels:
            results |= set(bruteforce(domain, labels))
    if kit.flag(properties, "PASSIVE", "Query passive sources", True):
        results |= passive(domain)

    subs = sorted(results)
    if not subs:
        kit.bad(f"No subdomains found for {domain}")
        record(f"No subdomains found for {domain}")
        return subs

    kit.good(f"{len(subs)} subdomains found for {domain}")
    for s in subs:
        kit.bullet(s)
    logs = kit.logdir(web)
    stem = os.path.basename(logs)[:-len("-logs")]
    path = os.path.join(logs, f"{stem}-subdomains.lst")
    with open(path, "w") as fh:
        fh.write("\n".join(subs) + "\n")
    kit.info(f"Saved to {path}")
    record(subs)
    return subs


def attack(web):
    subdom(web)
