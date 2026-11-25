#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DNS zone transfer (AXFR) against the domain's name servers."""

from __future__ import annotations

import os

import dns.exception
import dns.query
import dns.rcode
import dns.xfr
import dns.zone

from core.methods import dnsmisc
from core.methods import modkit as kit
from core.methods.print import pvln

info = ("Zone transfer module: asks every authoritative name server of the target's domain "
        "(or only the server set in DNSV) for a full zone transfer (AXFR). A successful "
        "transfer discloses every host name of the zone; it is saved to "
        "tmp/logs/<host>-logs/<domain>-axfr-<server>.txt.")
searchinfo = "Zone Transfer module"
properties = {
    "DNSV": ["DNS server to test (name or IP; default: all NS of the domain)", ""],
}

TIMEOUT = 10
SHOW = 25


def axfr(ip: str, domain: str):
    """dns.zone.Zone on success; (None, reason) otherwise."""
    try:
        zone = dns.zone.from_xfr(dns.query.xfr(ip, domain, timeout=TIMEOUT, lifetime=TIMEOUT * 3))
        return zone, ""
    except dns.xfr.TransferError as e:
        return None, f"refused ({dns.rcode.to_text(e.rcode)})"
    except dns.exception.FormError:
        return None, "refused (malformed/empty answer)"
    except (dns.exception.Timeout, TimeoutError):
        return None, "timed out"
    except EOFError:
        return None, "connection closed (refused)"
    except (ConnectionError, OSError) as e:
        return None, f"connection failed ({e.strerror or type(e).__name__})"
    except dns.exception.DNSException as e:
        return None, f"failed ({type(e).__name__})"


def zone_lines(zone) -> list[str]:
    return [line for line in zone.to_text(relativize=False).splitlines() if line.strip()]


def servers(domain: str, override: str) -> list[tuple[str, str]]:
    """(name, ip) pairs to test."""
    names = [override] if override else dnsmisc.ns(domain)
    out = []
    for name in names:
        if kit.is_ip(name) or ":" in name:
            ips = [name]
        else:  # IPv4 first: IPv6 is often unroutable from the scanning host
            ips = dnsmisc.addresses(name, ipv6=False) or dnsmisc.addresses(name)
        if not ips:
            kit.bad(f"{name} does not resolve.")
        out += [(name, ip) for ip in ips]
    return out


def zone(web):
    pvln("zone transfer")
    record = kit.Recorder(web, kit.MISCONFIG, "zone")
    domain = kit.domain(web)
    if kit.is_ip(domain):
        kit.bad("Target is an IP address; a zone transfer needs a domain name.")
        record("Not applicable: target is an IP address.")
        return []
    dnsmisc.warn_tor()
    override = kit.option(properties, "DNSV", "DNS server to test (enter for all NS)", "")
    targets = servers(domain, override)
    if not targets:
        kit.bad(f"No name servers found for {domain}.")
        record(f"No name servers found for {domain}.")
        return []
    kit.info(f"Testing {len(targets)} name server address(es) for {domain}")

    vulnerable = []
    for name, ip in targets:
        z, why = axfr(ip, domain)
        label = name if name == ip else f"{name} ({ip})"
        if z is None:
            kit.bullet(f"{label}: {why}")
            continue
        lines = zone_lines(z)
        hosts = sorted({str(n) for n in z.nodes})
        kit.found("Zone transfer allowed", f"{label}: {len(lines)} records, {len(hosts)} names")
        for line in lines[:SHOW]:
            print(f"    {line}")
        if len(lines) > SHOW:
            kit.info(f"... {len(lines) - SHOW} more")
        path = os.path.join(kit.logdir(web), f"{domain}-axfr-{ip.replace(':', '_')}.txt")
        try:
            with open(path, "w") as fh:
                fh.write("\n".join(lines) + "\n")
            kit.info(f"Zone saved to {path}")
        except OSError as e:
            kit.bad(f"Could not save the zone: {e}")
        vulnerable.append(label)
        record(f"[HIGH] Zone transfer allowed by {label}: {len(lines)} records\n" + "\n".join(lines))

    if not vulnerable:
        kit.good("All name servers refuse zone transfers.")
        record(f"Zone transfer refused by: {', '.join(n for n, _ in targets)}")
    return vulnerable


def attack(web):
    zone(web)
