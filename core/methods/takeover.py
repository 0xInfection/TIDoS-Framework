#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""
Subdomain takeover detection.

    result = takeover.check("blog.example.com")          # live DNS + HTTP
    result = takeover.check(name, lookup=fake, fetch=fake)  # tests

check() follows the CNAME chain of a name, matches every name of the chain
against files/signaturedb/takeover_signatures.py and returns a Result:

    result.findings  -- [Takeover] with service, status, confidence, evidence
    result.notes     -- dangling CNAMEs to unknown services (manual review)

A takeover is reported only when the chain points at a service AND
    * the service's HTTP fingerprint is in the subdomain's response, or
    * the service is an NXDOMAIN-signal service and the chain dangles, or
    * the chain dangles into a registrable domain that is not registered.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable

from core.methods import modkit as kit
from files.signaturedb.takeover_signatures import TAKEOVER_SIGNATURES

OK, NXDOMAIN, NOANSWER, ERROR = "ok", "nxdomain", "noanswer", "error"
MAX_HOPS = 10

# lookup(name, rdtype) -> (status, [answers])
Lookup = Callable[[str, str], "tuple[str, list[str]]"]
# fetch(name) -> response body ('' / None when unreachable)
Fetch = Callable[[str], "str | None"]


@dataclass(frozen=True)
class Signature:
    service: str
    cname: tuple
    fingerprint: re.Pattern | None
    nxdomain: bool
    status: str


SIGNATURES = [
    Signature(s["service"], tuple(re.compile(c, re.I) for c in s["cname"]),
              re.compile(s["fingerprint"], re.I) if s["fingerprint"] else None,
              s["nxdomain"], s["status"])
    for s in TAKEOVER_SIGNATURES
]


@dataclass
class Takeover:
    subdomain: str
    service: str
    status: str          # vulnerable / edge / unregistered
    confidence: str      # confirmed / likely / verify
    evidence: str
    chain: list[str]

    def __str__(self) -> str:
        return (f"{self.subdomain} -> {' -> '.join(self.chain[1:])} : {self.service} "
                f"[{self.confidence}] {self.evidence}")


@dataclass
class Result:
    subdomain: str
    chain: list[str] = field(default_factory=list)
    state: str = ""
    findings: list[Takeover] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


# --------------------------------------------------------------------------
# DNS
# --------------------------------------------------------------------------

def _resolver():
    import dns.resolver
    r = dns.resolver.Resolver()
    r.lifetime = 6.0
    r.timeout = 3.0
    return r


def dns_lookup(name: str, rdtype: str, resolver=None) -> tuple[str, list[str]]:
    """(status, answers) of a DNS query with dnspython."""
    import dns.exception
    import dns.resolver
    resolver = resolver or _resolver()
    try:
        ans = resolver.resolve(name, rdtype)
    except dns.resolver.NXDOMAIN:
        return NXDOMAIN, []
    except dns.resolver.NoAnswer:
        return NOANSWER, []
    except (dns.resolver.NoNameservers, dns.exception.Timeout, dns.exception.DNSException):
        return ERROR, []
    return OK, [r.to_text().rstrip(".").lower() for r in ans]


def cname_chain(name: str, lookup: Lookup) -> tuple[list[str], str]:
    """([name, cname1, cname2, ...], state of the last name).

    state: ok (has addresses), nxdomain, noanswer (exists, no A/AAAA) or error.
    """
    chain = [name.lower().rstrip(".")]
    for _ in range(MAX_HOPS):
        status, answers = lookup(chain[-1], "CNAME")
        if status == OK and answers:
            if answers[0] in chain:
                return chain, ERROR  # loop
            chain.append(answers[0])
            continue
        if status in (NXDOMAIN, ERROR):
            return chain, status
        break
    for rdtype in ("A", "AAAA"):
        status, answers = lookup(chain[-1], rdtype)
        if status == OK and answers:
            return chain, OK
        if status in (NXDOMAIN, ERROR):
            return chain, status
    return chain, NOANSWER


def registrable(name: str) -> str:
    try:
        import tldextract
        ext = tldextract.extract(name)
        if ext.domain and ext.suffix:
            return f"{ext.domain}.{ext.suffix}"
    except Exception:
        pass
    parts = name.split(".")
    return ".".join(parts[-2:])


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------

def http_fetch(name: str, timeout: float = 10) -> str | None:
    s = kit.http(timeout=timeout)
    for scheme in ("https", "http"):
        try:
            return s.get(f"{scheme}://{name}/").text
        except Exception:
            continue
    return None


# --------------------------------------------------------------------------
# check
# --------------------------------------------------------------------------

def services(chain: list[str]) -> list[tuple[Signature, str]]:
    """(signature, matching chain name) for every service the chain points at."""
    out = []
    for sig in SIGNATURES:
        for name in chain[1:]:
            if any(rx.search(name) for rx in sig.cname):
                out.append((sig, name))
                break
    return out


def check(subdomain: str, lookup: Lookup | None = None, fetch: Fetch | None = None) -> Result:
    lookup = lookup or dns_lookup
    fetch = fetch or http_fetch
    chain, state = cname_chain(subdomain, lookup)
    res = Result(chain[0], chain, state)
    if len(chain) < 2:
        return res  # no CNAME: nothing to take over here

    matched = services(chain)
    body = None
    for sig, name in matched:
        if sig.nxdomain:
            if state == NXDOMAIN:
                res.findings.append(Takeover(
                    res.subdomain, sig.service, sig.status,
                    "confirmed" if sig.status == "vulnerable" else "verify",
                    f"CNAME {name} does not resolve (NXDOMAIN): the resource can be re-created", chain))
            continue
        if sig.fingerprint is None or state == NXDOMAIN:
            continue
        if body is None:
            body = fetch(res.subdomain) or ""
        m = sig.fingerprint.search(body)
        if m:
            res.findings.append(Takeover(
                res.subdomain, sig.service, sig.status,
                "confirmed" if sig.status == "vulnerable" else "verify",
                f"CNAME {name} and the service's unclaimed-resource page: {m.group(0)[:80]!r}", chain))

    if state == NXDOMAIN and not matched:
        apex = registrable(chain[-1])
        if apex and apex != registrable(res.subdomain) and lookup(apex, "NS")[0] == NXDOMAIN:
            res.findings.append(Takeover(
                res.subdomain, f"unregistered domain {apex}", "unregistered", "likely",
                f"CNAME target {chain[-1]} is in {apex}, which does not exist: "
                f"registering it takes over the subdomain (confirm with whois)", chain))
        else:
            res.notes.append(f"{res.subdomain} -> {' -> '.join(chain[1:])}: dangling CNAME "
                             "(NXDOMAIN) to an unknown service; review manually")
    return res
