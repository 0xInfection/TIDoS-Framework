#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""(N)Ping enumeration -- ICMP ping plus an nping TCP probe of the web port."""

import shutil
from urllib.parse import urlsplit

from core.methods import modkit as kit
from core.methods.print import posintact

info = ("Pings the target (ICMP) and probes its web port with nping (TCP connect). "
        "Uses the local nping binary when installed, otherwise the HackerTarget "
        "nping API (needs HACKERTARGET_API_KEY).")
searchinfo = "(N)Ping Enumeration"
properties = {
    "COUNT": ["Number of probes to send", ""],
}



def web_port(web) -> int:
    parts = urlsplit(kit.url(web))
    try:
        return parts.port or (443 if parts.scheme == "https" else 80)
    except ValueError:
        return 80


def ping(host, count):
    kit.info(f"Pinging {host} ({count} packets)...")
    out = kit.command(["ping", "-c", str(count), host], timeout=count * 5 + 10)
    if out:
        print(out.rstrip() + "\n")
    return out


def nping(host, port, count):
    if shutil.which("nping"):
        kit.info(f"Probing {host}:{port} with nping (TCP connect)...")
        return kit.command(["nping", "--tcp-connect", "-p", str(port), "-c", str(count), host],
                           timeout=count * 5 + 10)

    kit.warn("nping is not installed, falling back to the HackerTarget API...")
    if not kit.apikey("HACKERTARGET_API_KEY"):  # nping endpoint is key-only
        return None
    return kit.hackertarget("nping", host)


def piwebenum(web):
    posintact("(n)ping enumeration")
    record = kit.Recorder(web, kit.ACTIVE, "piwebenum")
    host = kit.host(web)
    count = max(1, kit.integer(properties, "COUNT", "Number of probes", 5))

    results = []
    out = ping(host, count)
    if out:
        results.append(">> ping:\n" + out)

    out = nping(host, web_port(web), count)
    if out:
        print(out.rstrip() + "\n")
        results.append(">> nping:\n" + out)

    if results:
        record("\n".join(results))
        kit.good("Enumeration done.")
    else:
        kit.bad("Neither ping nor nping returned results.")
        record("No ping/nping results.")
    return results


def attack(web):
    piwebenum(web)
