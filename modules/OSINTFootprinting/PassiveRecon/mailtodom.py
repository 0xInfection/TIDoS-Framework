#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Email to domain -- passive recon (reverse WhoIS on an email address)."""

from __future__ import annotations

import re

import requests

from core.methods import modkit as kit
from core.methods.print import posintpas

info = ("This module tries to find the domain for a given email address "
        "(reverse WhoIS via the ViewDNS API, needs VIEWDNS_API_KEY).")
searchinfo = "Find domain from email"
properties = {
    "EMAIL": ["Email address to look up", ""],
}

API = "https://api.viewdns.info/reversewhois/"
EMAIL_RX = re.compile(r"[^@\s]+@[^@\s]+\.[A-Za-z]{2,}")


def lookup(email: str, key: str) -> list[dict] | None:
    """Domains registered with `email`, or None on API failure."""
    try:
        resp = kit.http(timeout=30).get(API, params={"q": email, "apikey": key, "output": "json"})
        data = resp.json()
    except (requests.RequestException, ValueError) as e:
        kit.bad(f"ViewDNS request failed: {e}")
        return None
    if data.get("success") is False or "error" in data:
        err = data.get("error")
        kit.bad(f"ViewDNS: {err.get('message', err) if isinstance(err, dict) else err}")
        return None
    return (data.get("response") or {}).get("matches") or []


def mailtodom(web=None):
    posintpas("email to domain")
    email = kit.option(properties, "EMAIL", "Enter the email")
    if not EMAIL_RX.fullmatch(email):
        kit.bad(f"'{email}' is not a valid email address (set EMAIL)." if email
                else "No email given (set EMAIL).")
        return []
    key = kit.apikey("VIEWDNS_API_KEY")
    if not key:
        return []

    kit.info(f"Looking up domains registered with {email} ...")
    matches = lookup(email, key)
    if matches is None:
        return []
    if not matches:
        kit.bad(f"Empty domain result for email: {email}")
        return []
    domains = []
    for m in matches:
        m = m if isinstance(m, dict) else {"domain": str(m)}
        extra = ", ".join(filter(None, (m.get("created_date"), m.get("registrar"))))
        kit.found("Received domain", f"{m.get('domain')} ({extra})" if extra else m.get("domain"))
        domains.append(m.get("domain", ""))
    kit.good(f"{len(domains)} domain(s) registered with {email}.")
    kit.Recorder(web or email.split("@")[1], kit.PASSIVE, "mailtodom")([email] + domains)
    return domains


def attack(web):
    mailtodom(web)
