#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Credit Card hunter -- information disclosure."""

import re

from core.methods import harvest
from core.methods import modkit as kit
from core.methods.print import pleak
from files.signaturedb.infodisc_signatures import (CARD_CANDIDATE_SIGNATURE,
                                                   CARD_CONTEXT_SIGNATURE, CARD_ISSUERS)

info = ("Finds payment card numbers disclosed in the target's pages. Candidates "
        "must pass the Luhn checksum and match a known issuer prefix (Visa, "
        "MasterCard, Amex, Discover, Diners, JCB); unformatted digit runs also "
        "need card-related wording nearby.")
searchinfo = "Credit Card hunter"
properties = {
    "CRAWL": ["Also scan same-host pages linked from the target (y/n)", ""],
    **kit.AUTH_OPTIONS,
}

CANDIDATE = re.compile(CARD_CANDIDATE_SIGNATURE)
CONTEXT = re.compile(CARD_CONTEXT_SIGNATURE)
CONTEXT_WINDOW = 80  # chars either side of an unformatted number
ISSUERS = [(name, re.compile(sig)) for name, sig in CARD_ISSUERS]


def luhn(number: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(number)):
        d = int(ch)
        if i % 2:
            d = d * 2 - 9 if d > 4 else d * 2
        total += d
    return total % 10 == 0


def issuer(number: str):
    return next((name for name, rx in ISSUERS if rx.match(number)), None)


def extract(body):
    for m in CANDIDATE.finditer(body):
        digits = re.sub(r"\D", "", m.group(0))
        brand = issuer(digits)
        if not (brand and luhn(digits) and len(set(digits)) > 1):
            continue
        if m.group("plain"):
            # a bare 16-digit number passes Luhn 1 time in 10 (IDs, timestamps,
            # hashes...), so only report it when card wording is nearby
            window = body[max(0, m.start() - CONTEXT_WINDOW):m.end() + CONTEXT_WINDOW]
            if not CONTEXT.search(window):
                continue
        yield f"{digits} ({brand})"


def creditcards(web):
    pleak("credit card hunter")
    return harvest.run(web, properties, noun="card numbers", lvl2="creditcards", extract=extract)


def attack(web):
    creditcards(web)
