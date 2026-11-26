#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Bruteforce Recon -- runs any combination of the path-hunting modules."""

from core.methods import modkit as kit
from core.methods.print import posintact
from modules.OSINTFootprinting.ActiveRecon.backbrute import backbrute
from modules.OSINTFootprinting.ActiveRecon.backupbrute import backupbrute
from modules.OSINTFootprinting.ActiveRecon.dotbrute import dotbrute
from modules.OSINTFootprinting.ActiveRecon.indexmulbrute import indexmulbrute
from modules.OSINTFootprinting.ActiveRecon.logbrute import logbrute
from modules.OSINTFootprinting.ActiveRecon.passbrute import passbrute
from modules.OSINTFootprinting.ActiveRecon.proxybrute import proxybrute

SCANS = {
    "backdoor": ("Common backdoor paths (c99.php, .shell, ...)", backbrute),
    "backup":   ("Common backup locations (.bak, .db, ...)", backupbrute),
    "dot":      ("Common dot files (.htaccess, .git, ...)", dotbrute),
    "pass":     ("Common password files (.pgp, .skg, ...)", passbrute),
    "proxy":    ("Proxy auto-config locations (.pac, ...)", proxybrute),
    "index":    ("Alternative index pages (index1, ...)", indexmulbrute),
    "log":      ("Common log locations (.log, changelogs, ...)", logbrute),
}

info = ("Looks for interesting files on the webserver: backdoors, backups, hidden "
        "files, password files, proxy configs, alternate index pages and logs. "
        "TYPES is a comma separated list of: " + ", ".join(SCANS) + " (or 'all').")
searchinfo = "Bruteforce Recon"
properties = {
    "TYPES": ["Scans to run, comma separated, or 'all'", ""],
}


def filebrute(web):
    posintact("bruteforce recon")
    if kit.interactive() and not properties["TYPES"][1].strip():
        for key, (desc, _) in SCANS.items():
            kit.bullet(f"{key:<9} {desc}")
    choice = kit.option(properties, "TYPES", "Scans to run (comma separated, or 'all')", "all")
    wanted = list(SCANS) if choice.strip().lower() == "all" else \
        [c.strip().lower() for c in choice.split(",") if c.strip()]

    unknown = [w for w in wanted if w not in SCANS]
    if unknown:
        kit.bad(f"Unknown scan type(s): {', '.join(unknown)}")
    for key in (w for w in wanted if w in SCANS):
        SCANS[key][1](web)


def attack(web):
    filebrute(web)
