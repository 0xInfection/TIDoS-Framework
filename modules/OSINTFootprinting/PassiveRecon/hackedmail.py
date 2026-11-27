#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Data breach checker (XposedOrNot) -- passive recon."""

from __future__ import annotations

import re

from core.methods import modkit as kit
from core.methods.print import posintpas

info = "This module looks up if an email address was found in a data breach (via XposedOrNot)."
searchinfo = "Data Breach Checker"
properties = {
    "EMAIL": ["E-mail address(es) to check, comma separated (default: the target's known e-mails)", ""],
}

API = "https://api.xposedornot.com/v1/breach-analytics"
EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def breaches(session, email: str) -> list[dict] | None:
    """Breach details for an address ([] if clean, None on error)."""
    try:
        resp = session.get(API, params={"email": email})
    except Exception as e:
        kit.bad(f"Can't reach XposedOrNot: {e}")
        return None
    try:
        data = resp.json()
    except ValueError:
        kit.bad(f"Unexpected answer from XposedOrNot (HTTP {resp.status_code}).")
        return None
    return ((data.get("ExposedBreaches") or {}).get("breaches_details")) or []


def hackedmail(web=None):
    posintpas("hacked email")
    default = ",".join(getattr(web, "emails", None) or [])
    raw = kit.option(properties, "EMAIL", "Enter the email(s)", default)
    emails = [e.strip() for e in raw.split(",") if e.strip()]
    invalid = [e for e in emails if not EMAIL_RE.fullmatch(e)]
    for e in invalid:
        kit.bad(f"Not a valid e-mail address: {e}")
    emails = [e for e in emails if e not in invalid]
    if not emails:
        kit.bad("No e-mail address to check (set EMAIL).")
        return {}

    session = kit.http()
    record = kit.Recorder(web or "", kit.PASSIVE, "hackedmail")
    results = {}
    for email in emails:
        kit.info(f"Looking up {email}...")
        found = breaches(session, email)
        if found is None:
            continue
        results[email] = found
        if not found:
            kit.good(f"Email {email} not found in any breaches!")
            record(f"Email {email} not found in any breaches!")
            continue
        kit.warn(f"{email} found in {len(found)} breach(es):")
        lines = []
        for b in found:
            line = f"{b.get('breach')} ({b.get('xposed_date', '?')})"
            kit.found(email, f"{line} -- {b.get('xposed_data', '').replace(';', ', ')}")
            lines.append(f"{email} found in : {line}")
        record(lines)
    return results


def attack(web):
    hackedmail(web)
