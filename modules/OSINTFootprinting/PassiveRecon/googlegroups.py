#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Google e-mail enumeration -- passive recon."""

from __future__ import annotations

import re

from bs4 import BeautifulSoup

from core.methods import modkit as kit
from core.methods.google import Blocked, blocked_hint, pages
from core.methods.print import posintpas

info = "This module uses Google to enumerate email addresses of the target's domain."
searchinfo = "Enumeration using Google Groups"
properties = {
    "LIMIT": ["Number of Google results to go through", ""],
}


def emails_in(html: str, domain: str) -> list[str]:
    text = BeautifulSoup(html, "lxml").get_text(" ")
    found = re.findall(rf"[\w.+-]+@{re.escape(domain)}\b", text, re.I)
    return list(dict.fromkeys(e.lower() for e in found))


def googlegroups(web):
    posintpas("google groups")
    domain = kit.domain(web)
    limit = kit.integer(properties, "LIMIT", "Number of Google results to go through", 100)
    record = kit.Recorder(web, kit.PASSIVE, "googlegroups")

    kit.info(f"Enumerating e-mails of @{domain} via Google...")
    emails: list[str] = []
    try:
        for html in pages(f'"@{domain}"', limit):
            for email in emails_in(html, domain):
                if email not in emails:
                    emails.append(email)
                    kit.found("Received e-mail", email)
    except Blocked:
        blocked_hint()
        return emails
    except Exception as e:
        kit.bad(f"Error connecting to Google: {e}")
        return emails

    if emails:
        kit.good(f"{len(emails)} e-mail address(es) found.")
        record(emails)
    else:
        kit.bad("No e-mail addresses found via Google.")
        record("No results found via enumeration on Google Groups.")
    return emails


def attack(web):
    googlegroups(web)
