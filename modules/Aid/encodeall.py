#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""String encoder -- common encodings of a string, side by side."""

from __future__ import annotations

import base64
import binascii
import gzip
import html
from urllib.parse import quote_plus

from core.methods import modkit as kit

info = ("Encodes a string into several common encodings at once (URL, HTML entities, "
        "Base64, hex, octal, binary and gzip+Base64). Set STRING to run "
        "non-interactively; otherwise you are prompted.")
searchinfo = "String Encoder"
properties = {"STRING": ["Text to encode (empty: prompt)", ""]}


def encodings(text: str) -> list[tuple[str, str]]:
    raw = text.encode("utf-8", "surrogatepass")
    return [
        ("URL", quote_plus(text)),
        ("HTML", html.escape(text)),
        ("Base64", base64.b64encode(raw).decode()),
        ("Hex", binascii.hexlify(raw).decode()),
        ("Octal", "".join("\\%o" % b for b in raw)),
        ("Binary", " ".join(format(b, "08b") for b in raw)),
        ("Gzip+Base64", base64.b64encode(gzip.compress(raw)).decode()),
    ]


def attack(web):
    text = kit.option(properties, "STRING", "Enter the string to encode")
    if not text:
        kit.bad("No string given; set STRING or run interactively.")
        return
    kit.info("Encoding string...")
    for label, value in encodings(text):
        kit.found(label, value)
