#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Backdoor Hunter -- part of the TIDoS bruteforce recon family (see filebrute)."""

from core.methods import dirbrute
from core.methods.print import posintact

info = "Looks for common webshells and backdoors (c99.php, .shell, ...) on the target's webserver."
searchinfo = "Backdoor Hunter"
properties = {
    "WORDLIST": ["Wordlist of paths to request", ""],
}


def backbrute(web):
    posintact("backdoor brute")
    return dirbrute.run(web, properties, noun="backdoors",
                        wordlist="files/fuzz-db/backdoor_paths.lst", lvl3="backbrute")


def attack(web):
    backbrute(web)
