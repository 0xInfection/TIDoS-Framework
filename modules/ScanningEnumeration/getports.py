#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Port scanner -- concurrent TCP connect scan of common ports."""

from core.methods import modkit as kit
from core.methods import portscan
from core.methods.print import pscan

info = ("This module checks if common ports are open (TCP connect scan). "
        "PORTS accepts a comma separated list with ranges, e.g. 22,80,8000-8100.")
searchinfo = "Port Scanner"
properties = {
    "PORTS": ["Ports to scan (e.g. 21,22,80,8000-8100)", ""],
}


def getports(web):
    pscan("port scanner")
    return portscan.run(web, properties, kit.SCAN, "getports")


def attack(web):
    getports(web)
