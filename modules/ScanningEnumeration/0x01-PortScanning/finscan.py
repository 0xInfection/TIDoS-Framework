#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""FIN scanner -- inverse TCP scan with a lone FIN flag (needs root)."""

from core.methods import rawscan
from core.methods.print import pscan

info = ("FIN scan: sends packets with only the FIN flag set. RFC 793 stacks answer "
        "closed ports with a RST and stay silent on open ones (open|filtered); ICMP "
        "unreachable means filtered. Windows and some network gear reply RST to "
        "everything. Needs root.")
searchinfo = "FIN Scanner"
properties = {
    "PORTS": ["Ports to scan (e.g. 21,22,80,8000-8100; empty = common ports)", ""],
    "TIMEOUT": ["Seconds to wait for replies (default 2)", ""],
    "VERBOSE": ["Show closed ports in the report too (y/n)", ""],
}


def finscan(web):
    pscan("fin scan")
    return rawscan.run(web, properties, "fin", lvl2="finscan")


def attack(web):
    finscan(web)
