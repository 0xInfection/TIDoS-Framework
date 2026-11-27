#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Logfile Bruteforce -- part of the TIDoS bruteforce recon family (see filebrute)."""

from core.methods import dirbrute
from core.methods.print import posintact

info = "Looks for exposed log files and changelogs on the target's webserver."
searchinfo = "Logfile Bruteforce"
properties = {
    "WORDLIST": ["Wordlist of paths to request", ""],
}


def logbrute(web):
    posintact("log file brute")
    return dirbrute.run(web, properties, noun="log files",
                        wordlist="files/fuzz-db/log_paths.lst", lvl3="logbrute")


def attack(web):
    logbrute(web)
