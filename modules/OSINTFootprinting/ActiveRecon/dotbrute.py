#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Hidden File Enumeration -- part of the TIDoS bruteforce recon family (see filebrute)."""

from core.methods import dirbrute
from core.methods.print import posintact

info = "Looks for exposed dot files (.htaccess, .git, .env, ...) on the target's webserver."
searchinfo = "Hidden File Enumeration"
properties = {
    "WORDLIST": ["Wordlist of paths to request", ""],
}


def dotbrute(web):
    posintact("dot file brute")
    return dirbrute.run(web, properties, noun="dot files",
                        wordlist="files/fuzz-db/dot_paths.lst", lvl3="dotbrute")


def attack(web):
    dotbrute(web)
