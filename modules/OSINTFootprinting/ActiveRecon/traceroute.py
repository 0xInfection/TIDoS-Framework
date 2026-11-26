#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Traceroute -- maps the network path to the target with the system traceroute."""

import os
import sys

from core.methods import modkit as kit
from core.methods.print import posintact

info = ("Runs the system traceroute against the target. PROTO selects the probe "
        "type: udp (default, unprivileged), icmp (ECHO) or tcp (SYN, usually needs "
        "root). FRAGMENT=n sets the don't-fragment bit, DEBUG=y enables socket "
        "level debugging.")
searchinfo = "Traceroute module"
properties = {
    "PROTO": ["Probe type: udp, icmp or tcp", ""],
    "FRAGMENT": ["Allow fragmented packets (y/n); n sets don't-fragment", ""],
    "DEBUG": ["Enable socket level debugging (y/n)", ""],
    "MAXHOPS": ["Maximum number of hops", ""],
}

PROTOS = {"udp": "udp", "u": "udp", "icmp": "icmp", "i": "icmp", "tcp": "tcp", "t": "tcp"}


def build(host, proto, fragment, debug, maxhops):
    args = ["traceroute", "-m", str(maxhops), "-w", "2"]
    if proto == "icmp":
        args.append("-I")
    elif proto == "tcp":
        args += ["-T"] if sys.platform.startswith("linux") else ["-P", "tcp"]
    if not fragment:
        args.append("-F")
    if debug:
        args.append("-d")
    return args + [host]


def traceroute(web):
    posintact("traceroute")
    record = kit.Recorder(web, kit.ACTIVE, "traceroute")
    host = kit.host(web)

    choice = kit.option(properties, "PROTO", "Probe type [udp/icmp/tcp]", "udp").lower()
    proto = PROTOS.get(choice)
    if not proto:
        kit.bad(f"Unknown probe type '{choice}' (use udp, icmp or tcp).")
        return None
    fragment = kit.flag(properties, "FRAGMENT", "Allow fragmented packets", True)
    debug = kit.flag(properties, "DEBUG", "Enable socket level debugging", False)
    maxhops = max(1, min(kit.integer(properties, "MAXHOPS", "Maximum hops", 30), 64))

    if proto != "udp" and sys.platform.startswith("linux") and os.geteuid() != 0:
        kit.warn(f"{proto.upper()} traceroute usually needs root; it may fail.")

    kit.info(f"Tracing route to {host} using {proto.upper()} "
             f"({'fragmented' if fragment else 'unfragmented'} packets, max {maxhops} hops)...")
    out = kit.command(build(host, proto, fragment, debug, maxhops), timeout=maxhops * 3 * 2 + 30)
    if not out:
        record("Traceroute failed.")
        return None

    print(out.rstrip() + "\n")
    hops = [line for line in out.splitlines() if line.strip()[:1].isdigit()]
    kit.good(f"Traceroute done ({len(hops)} hops).")
    record(out)
    return out


def attack(web):
    traceroute(web)
