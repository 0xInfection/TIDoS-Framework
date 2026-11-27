#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Apache server-status / server-info hunter."""

import posixpath

import requests

from core.methods import dirbrute
from core.methods import modkit as kit
from core.methods.print import posintact

info = ("Looks for exposed Apache status pages (server-status, server-info, "
        "perl-status, ...). Pages answering 401/403 exist but are protected.")
searchinfo = "Apache Status Hunter"
properties = {
    "WORDLIST": ["Wordlist of status page paths", ""],
}

WORDLIST = "files/fuzz-db/apachestat_paths.lst"


def apachestat(web):
    posintact("apache status")
    path = kit.option(properties, "WORDLIST", "Wordlist of status page paths", WORDLIST)
    # requests/urllib3 resolve dot segments anyway ("/../server-status" is
    # "/server-status" on the wire), so collapse them to avoid duplicate hits
    paths = list(dict.fromkeys(posixpath.normpath("/" + p) for p in kit.wordlist(path)))
    if not paths:
        return []

    try:
        kit.http().head(kit.url(web))
    except requests.RequestException as e:
        kit.bad(f"Target unreachable: {type(e).__name__}")
        return []

    kit.info(f"Hunting status pages on {kit.url(web)} ({len(paths)} paths)")
    hits = dirbrute.scan(web, paths, codes={200, 302, 401, 403})
    record = kit.Recorder(web, kit.ACTIVE, "apachestat")

    exposed = [h for h in hits if h.status in (200, 302)]
    for h in hits:
        if h.status in (401, 403):
            kit.warn(f"Present but protected ({h.status}): {h.url}")
    if exposed:
        for h in exposed:
            kit.found("Apache server status enabled at", h.url)
        record([h.url for h in exposed])
    else:
        kit.bad("No server status enabled!")
        record("No server status enabled.")
    kit.good("Apache server status completed!")
    return exposed


def attack(web):
    apachestat(web)
