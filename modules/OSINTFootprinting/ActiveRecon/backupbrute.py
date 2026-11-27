#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Backup Harvester -- part of the TIDoS bruteforce recon family (see filebrute)."""

from core.methods import dirbrute
from core.methods.print import posintact

info = "Looks for backup files and archives (.bak, .old, .sql, ...) left on the target's webserver."
searchinfo = "Backup Harvester"
properties = {
    "WORDLIST": ["Wordlist of paths to request", ""],
}


def backupbrute(web):
    posintact("backup brute")
    return dirbrute.run(web, properties, noun="backup files",
                        wordlist="files/fuzz-db/backup_paths.lst", lvl3="backupbrute")


def attack(web):
    backupbrute(web)
