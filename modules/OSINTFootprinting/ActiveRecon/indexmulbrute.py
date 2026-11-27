#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Index Path Bruteforce -- part of the TIDoS bruteforce recon family (see filebrute)."""

from core.methods import dirbrute
from core.methods.print import posintact

info = "Looks for alternative index pages (index1, index_old, ...) on the target's webserver."
searchinfo = "Index Path Bruteforce"
properties = {
    "WORDLIST": ["Wordlist of paths to request", ""],
}


def indexmulbrute(web):
    posintact("multiple index brute")
    return dirbrute.run(web, properties, noun="index pages",
                        wordlist="files/fuzz-db/multipleindex_paths.lst", lvl3="indexmulbrute")


def attack(web):
    indexmulbrute(web)
