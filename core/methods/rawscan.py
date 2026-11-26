#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""
Raw-packet (scapy) port scanning engine shared by the SYN/FIN/XMAS/NULL scanners.

    classify("syn", reply)        -> "open" / "closed" / "filtered"
    probe(ip, ports, "fin")       -> {port: state}
    run(target, properties, "xmas", lvl2="xmasscan")  -> whole module flow

Response classification follows nmap:

    SYN        SYN/ACK -> open, RST -> closed,
               no reply / ICMP unreachable (type 3, code 1,2,3,9,10,13) -> filtered
    FIN/XMAS/  no reply -> open|filtered, RST -> closed,
    NULL       ICMP unreachable -> filtered

The classifiers are pure functions of a (crafted or received) scapy packet,
so they can be tested offline. scapy itself is imported lazily: it is slow to
import and chatty, and only needed when packets are actually sent.
"""

from __future__ import annotations

import logging
import random
import sys
import time
from types import SimpleNamespace

import core.variables as variables
from core.methods import modkit as kit
from core.methods import portscan

OPEN = "open"
CLOSED = "closed"
FILTERED = "filtered"
OPEN_FILTERED = "open|filtered"

# TCP flags sent by each scan type
FLAGS = {"syn": "S", "fin": "F", "xmas": "FPU", "null": ""}

TCP_SYN, TCP_RST, TCP_ACK = 0x02, 0x04, 0x10
ICMP_UNREACH = 3
ICMP_FILTER_CODES = frozenset((1, 2, 3, 9, 10, 13))

DEFAULT_TIMEOUT = 2   # seconds to wait for late replies after a batch
RETRIES = 1           # resend unanswered probes once (packet loss != state)
BATCH = 64            # probes per sr() call, multiplied by core.variables.processes


# --------------------------------------------------------------------------
# classification (pure, offline-testable)
# --------------------------------------------------------------------------

def _icmp_filtered(reply) -> bool | None:
    """True for an ICMP 'administratively filtered' style unreachable,
    False for any other ICMP message, None when the reply is not ICMP."""
    icmp = reply.getlayer("ICMP")
    if icmp is None:
        return None
    return int(icmp.type) == ICMP_UNREACH and int(icmp.code) in ICMP_FILTER_CODES


def classify_syn(reply) -> str:
    """State of a port from the reply to a SYN probe (None = no reply)."""
    if reply is None:
        return FILTERED
    if _icmp_filtered(reply) is not None:   # ICMP first: errors quote our TCP header
        return FILTERED
    tcp = reply.getlayer("TCP")
    if tcp is None:
        return FILTERED
    flags = int(tcp.flags)
    if flags & TCP_RST:
        return CLOSED
    if flags & TCP_SYN:                     # SYN/ACK (or a bare SYN: split handshake)
        return OPEN
    return FILTERED


def classify_inverse(reply) -> str:
    """State of a port from the reply to a FIN / XMAS / NULL probe."""
    if reply is None:
        return OPEN_FILTERED
    icmp = _icmp_filtered(reply)
    if icmp is not None:
        return FILTERED if icmp else OPEN_FILTERED
    tcp = reply.getlayer("TCP")
    if tcp is not None and int(tcp.flags) & TCP_RST:
        return CLOSED
    return OPEN_FILTERED


def classify(kind: str, reply) -> str:
    return classify_syn(reply) if kind == "syn" else classify_inverse(reply)


# --------------------------------------------------------------------------
# packets
# --------------------------------------------------------------------------

def require_root(alternative: str = "tcpconnectscan") -> bool:
    """True when raw packets can be sent; otherwise explain and return False."""
    if kit.is_root():
        return True
    kit.bad("This scan crafts raw packets and needs root privileges.")
    kit.info(f"Run the console as root (sudo), or use the '{alternative}' module instead.")
    return False


def load_scapy() -> SimpleNamespace:
    """Import the bits of scapy we need, quietly."""
    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
    logging.getLogger("scapy.loading").setLevel(logging.ERROR)
    from scapy.config import conf
    conf.verb = 0
    from scapy.layers.inet import ICMP, IP, TCP
    from scapy.sendrecv import send, sr
    return SimpleNamespace(conf=conf, IP=IP, TCP=TCP, ICMP=ICMP, sr=sr, send=send)


def build(scapy, ip: str, ports: list[int], kind: str, sport: int) -> list:
    return [scapy.IP(dst=ip) / scapy.TCP(sport=sport, dport=p, flags=FLAGS[kind],
                                         seq=random.randint(0, 2 ** 32 - 1))
            for p in ports]


def _loopback_socket(scapy, ip: str):
    """Linux needs a plain raw socket to talk to 127.0.0.0/8; returns the
    previous L3 socket class to restore, or None if nothing was changed."""
    if not (ip.startswith("127.") and sys.platform.startswith("linux")):
        return None
    from scapy.supersocket import L3RawSocket
    previous, scapy.conf.L3socket = scapy.conf.L3socket, L3RawSocket
    return previous


def probe(ip: str, ports: list[int], kind: str, timeout: float = DEFAULT_TIMEOUT,
          retry: int = RETRIES) -> dict[int, str]:
    """Send one probe per port (in batches) and classify every reply.

    SYN/ACKs are answered with a RST so no half-open connection lingers on
    the target (what nmap does). Raises OSError on send failures.
    """
    scapy = load_scapy()
    sport = random.randint(1025, 65000)
    states = {}
    batch = max(BATCH, BATCH * variables.processes)
    previous = _loopback_socket(scapy, ip)
    try:
        for i in range(0, len(ports), batch):
            chunk = ports[i:i + batch]
            answered, _ = scapy.sr(build(scapy, ip, chunk, kind, sport),
                                   timeout=timeout, retry=retry, verbose=0)
            replies = {int(sent.dport): reply for sent, reply in answered}
            resets = []
            for port in chunk:
                reply = replies.get(port)
                states[port] = classify(kind, reply)
                if kind == "syn" and states[port] == OPEN:
                    resets.append(scapy.IP(dst=ip) / scapy.TCP(
                        sport=sport, dport=port, flags="R", seq=int(reply["TCP"].ack)))
            if resets:
                scapy.send(resets, verbose=0)
    finally:
        if previous is not None:
            scapy.conf.L3socket = previous
    return states


# --------------------------------------------------------------------------
# module flow
# --------------------------------------------------------------------------

def run(target, properties: dict, kind: str, lvl2: str) -> list[tuple[int, str]]:
    """Complete raw scan module: options, probing, report and persistence.

    Returns the interesting (port, state) rows: open ports for SYN scans,
    open|filtered and filtered ports for FIN/XMAS/NULL scans.
    """
    if not require_root():
        return []
    ports = portscan.ports_option(properties)
    if not ports:
        kit.bad("No valid ports to scan.")
        return []
    timeout = max(0.2, kit.number(properties, "TIMEOUT", "Seconds to wait for replies", DEFAULT_TIMEOUT))
    verbose = kit.flag(properties, "VERBOSE", "Show closed ports too?", False)
    portscan.warn_tor()
    ip = portscan.resolve_ip(target)
    if not ip:
        return []

    name = kit.host(target)
    kit.info(f"{kind.upper()} scanning {len(ports)} ports on {name} ({ip})...")
    start = time.time()
    try:
        states = probe(ip, ports, kind, timeout=timeout)
    except KeyboardInterrupt:
        kit.bad("Scan interrupted by user.")
        return []
    except ImportError:
        kit.bad("scapy is not installed: pip install scapy")
        return []
    except Exception as e:  # scapy raises OSError / Scapy_Exception subclasses
        kit.bad(f"Could not send packets: {e}")
        return []
    elapsed = time.time() - start

    shown = (OPEN,) if kind == "syn" else (OPEN, OPEN_FILTERED, FILTERED)
    hits = [(p, s) for p, s in sorted(states.items()) if s in shown]
    counts = {s: sum(1 for v in states.values() if v == s) for s in set(states.values())}

    record = kit.Recorder(target, kit.PORTSCAN, lvl2)
    if hits:
        kit.good(f"{len(hits)} port(s) {'open' if kind == 'syn' else 'open or filtered'}")
        if kind != "syn" and len(hits) == len(ports) and len(ports) > 1:
            kit.warn("No port answered at all: the host is down or drops these probes.")
        print()
        rows = [(p, s) for p, s in sorted(states.items()) if verbose or s in shown]
        portscan.report((p, s.upper()) for p, s in rows)
        for state in shown:
            group = [p for p, s in hits if s == state]
            if group:
                record(f"{state.title()} Ports: {group}")
    else:
        none = "No open ports found." if kind == "syn" else "No open/filtered ports found."
        kit.bad(none)
        record(none)
    hidden = len(ports) - len(hits)
    if hidden and not verbose:
        summary = ", ".join(f"{n} {s}" for s, n in sorted(counts.items()) if s not in shown)
        kit.info(f"{summary} ports not shown")
    kit.good(f"Host {name} scanned in {elapsed:.2f} seconds")
    return hits
