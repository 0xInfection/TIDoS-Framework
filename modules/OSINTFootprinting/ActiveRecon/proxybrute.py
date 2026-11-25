#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Proxy Bruteforce -- part of the TIDoS bruteforce recon family (see filebrute)."""

from core.methods import dirbrute
from core.methods.print import posintact

info = "Looks for exposed proxy auto-config files (.pac, wpad.dat, ...) on the target's webserver."
searchinfo = "Proxy Bruteforce"
properties = {
    "WORDLIST": ["Wordlist of paths to request", ""],
}


def proxybrute(web):
    posintact("proxy brute")
    return dirbrute.run(web, properties, noun="proxy config files",
                        wordlist="files/fuzz-db/proxy_paths.lst", lvl3="proxybrute")


def attack(web):
    proxybrute(web)
