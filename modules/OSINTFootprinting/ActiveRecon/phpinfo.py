#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""PHPInfo finder -- looks for exposed phpinfo() pages."""

import re

from core.methods import dirbrute
from core.methods import modkit as kit
from core.methods.print import posintact

info = ("Tries to find phpinfo() pages on the target's webserver. Candidate paths "
        "are requested concurrently, then each hit is confirmed by its content.")
searchinfo = "PHPInfo search"
properties = {
    "WORDLIST": ["Wordlist of candidate phpinfo paths", ""],
}

DEFAULT_WORDLIST = "files/fuzz-db/phpinfo_paths.lst"
SIGNATURE = re.compile(r"<title>phpinfo\(\)</title>|<h1 class=\"p\">PHP Version", re.I)
VERSION = re.compile(r"PHP Version\s*(?:</[^>]+>\s*<[^>]+>\s*)?([\d.]+[\w.-]*)", re.I)


def confirm(session, url):
    """Return the PHP version string if `url` really is a phpinfo page."""
    try:
        body = session.get(url).text
    except Exception:
        return None
    if not SIGNATURE.search(body):
        return None
    m = VERSION.search(body)
    return m.group(1) if m else "unknown"


def phpinfo(web):
    posintact("phpinfo finder")
    record = kit.Recorder(web, kit.ACTIVE, "phpinfo")

    paths = kit.wordlist(kit.option(properties, "WORDLIST", "Wordlist of phpinfo paths",
                                    DEFAULT_WORDLIST))
    if not paths:
        return []

    kit.info(f"Probing {len(paths)} candidate paths on {kit.url(web)}")
    hits = dirbrute.scan(web, paths, codes={200}, quiet=True)

    session = kit.http()
    pages = []
    for hit in hits:
        version = confirm(session, hit.url)
        if version:
            kit.found(f"PHPInfo page (PHP {version})", hit.url)
            pages.append(hit.url)
            record(f"phpinfo @ {hit.url} (PHP {version})")

    if not pages:
        kit.bad("Did not find any PHPInfo page.")
        record("Did not find PHPInfo file.")
    else:
        kit.good(f"{len(pages)} PHPInfo page(s) confirmed")
    return pages


def attack(web):
    phpinfo(web)
