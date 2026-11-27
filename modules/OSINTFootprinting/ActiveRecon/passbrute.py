#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Password hunter -- part of the TIDoS bruteforce recon family (see filebrute)."""

from core.methods import dirbrute
from core.methods.print import posintact

info = "Looks for exposed password and key files (.pgp, .skg, htpasswd, ...) on the target's webserver."
searchinfo = "Password hunter"
properties = {
    "WORDLIST": ["Wordlist of paths to request", ""],
}


def passbrute(web):
    posintact("password brute")
    return dirbrute.run(web, properties, noun="password files",
                        wordlist="files/fuzz-db/pass_paths.lst", lvl3="passbrute")


def attack(web):
    passbrute(web)
