#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""ARP scanner -- finds live hosts on the local network with a scapy ARP sweep."""

from __future__ import annotations

import importlib.util
import ipaddress

from core.methods import modkit as kit
from core.methods.print import pscan

MAX_PREFIX = 16  # refuse sweeps larger than a /16 unless FORCE is set

info = ("A simple ARP scanner to detect potential targets on your local network "
        "(to then proceed with port scanning and web attacks). Needs root. IP is "
        "an address of the network (e.g. the gateway), NMASK its netmask as a "
        "prefix length or dotted quad (24 or 255.255.255.0). Sweeps larger than "
        f"/{MAX_PREFIX} need FORCE=y.")
searchinfo = "ARP Network Scanner"
properties = {
    "IP": ["IP of the network's gateway", ""],
    "NMASK": ["Netmask of the network (e.g. 24 or 255.255.255.0)", ""],
    "TIMEOUT": ["Seconds to wait for ARP replies", ""],
    "FORCE": ["Allow sweeping networks larger than /16 (y/n)", ""],
}


def network(ip: str, mask: str) -> ipaddress.IPv4Network | None:
    """IPv4 network of IP/NMASK, or None after saying why."""
    if "/" in ip:  # IP given in CIDR notation wins over NMASK
        ip, _, mask = ip.partition("/")
    try:
        return ipaddress.IPv4Network(f"{ip.strip()}/{mask.strip()}", strict=False)
    except ValueError as e:
        kit.bad(f"Invalid network '{ip}/{mask}': {e}")
        return None


def vendor(mac: str) -> str:
    """Manufacturer of a MAC address from scapy's OUI database ('' if unknown)."""
    try:
        from scapy.all import conf
        name = conf.manufdb._get_manuf(mac)
    except Exception:  # manuf database missing or API changed: purely cosmetic
        return ""
    return "" if not name or name == mac else name


def sweep(net: ipaddress.IPv4Network, timeout: float) -> list[tuple[str, str]]:
    """(ip, mac) of every host answering an ARP who-has on `net`."""
    from scapy.all import ARP, Ether, conf, srp
    from scapy.error import Scapy_Exception
    conf.verb = 0
    try:
        answered, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=str(net)), timeout=timeout, retry=1)
    except Scapy_Exception as e:  # e.g. no permission on the capture device
        raise OSError(str(e)) from e
    hosts = {rcv.psrc: rcv.hwsrc for _, rcv in answered}
    return sorted(hosts.items(), key=lambda h: ipaddress.IPv4Address(h[0]))


def arp(web=""):
    pscan("arp-scan")
    ip = kit.option(properties, "IP", "Network address (e.g. 192.168.1.0 or 192.168.1.0/24)", "")
    if not ip:
        kit.bad("No network given: set IP and NMASK (e.g. 192.168.1.1 and 24).")
        return []
    mask = kit.option(properties, "NMASK", "Netmask (e.g. 24 or 255.255.255.0)", "" if "/" in ip else "24")
    net = network(ip, mask)
    if net is None:
        return []
    if net.prefixlen < MAX_PREFIX and not kit.flag(properties, "FORCE", f"Sweep {net.num_addresses} addresses", False):
        kit.bad(f"{net} has {net.num_addresses} addresses; refusing sweeps larger than /{MAX_PREFIX} (set FORCE=y).")
        return []
    if not kit.is_root():
        kit.bad("ARP scanning sends raw packets: run TIDoS as root.")
        return []
    if importlib.util.find_spec("scapy") is None:
        kit.bad("scapy is not installed (pip install scapy).")
        return []
    timeout = max(1, min(kit.integer(properties, "TIMEOUT", "Seconds to wait for replies", 3), 60))

    kit.info(f"ARP sweeping {net} ({net.num_addresses} addresses)...")
    try:
        hosts = sweep(net, timeout)
    except KeyboardInterrupt:
        kit.bad("Scan interrupted by user.")
        return []
    except (ImportError, OSError) as e:
        kit.bad(f"ARP sweep failed: {e}")
        return []

    record = kit.Recorder(str(net.network_address), kit.SCAN, "arpscan")
    if not hosts:
        kit.bad(f"No live hosts found on {net}.")
        record(f"No live hosts found on {net}.")
        return []

    kit.good(f"{len(hosts)} live host(s) on {net}")
    print()
    rows = [(addr, mac, vendor(mac)) for addr, mac in hosts]
    kit.kv_table((addr, f"{mac}  {name}".rstrip()) for addr, mac, name in rows)
    print()
    record("\n".join(f"{addr} {mac} {name}".rstrip() for addr, mac, name in rows))
    return [addr for addr, _ in hosts]


def attack(web):
    return arp(web)
