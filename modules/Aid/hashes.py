#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Hash calculator -- common digests of a string."""

from __future__ import annotations

import hashlib

from core.methods import modkit as kit

info = ("Calculates MD5, SHA-1, SHA-224, SHA-256, SHA-384 and SHA-512 digests of a "
        "string. Set STRING to run non-interactively; otherwise you are prompted.")
searchinfo = "Hash Calculator"
properties = {"STRING": ["Text to hash (empty: prompt)", ""]}

ALGORITHMS = ("md5", "sha1", "sha224", "sha256", "sha384", "sha512")


def hashes(message: str) -> None:
    data = message.encode("utf-8", "surrogatepass")
    kit.info("Generating hashes...")
    for name in ALGORITHMS:
        kit.found(name.upper(), hashlib.new(name, data).hexdigest())


def attack(web):
    message = kit.option(properties, "STRING", "Enter the string to hash")
    if not message:
        kit.bad("No string given; set STRING or run interactively.")
        return
    hashes(message)
