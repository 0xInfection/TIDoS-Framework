#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""
Tor support: HTTP sessions for modules and the `tor on|off` switch.

`tor on` only succeeds after the Tor Project's own check endpoint confirms
that traffic sent through the local SOCKS proxy exits via Tor. From then on
every session() routes HTTP (and its DNS, via socks5h) through Tor.
Raw sockets (port scans, ping, DNS libraries, TLS grabs) are NOT covered.
"""

from __future__ import annotations

import socket

import requests

import core.variables as vars

TOR_HOST, TOR_PORT = "127.0.0.1", 9050
TOR_PROXY = f"socks5h://{TOR_HOST}:{TOR_PORT}"
CHECK_URL = "https://check.torproject.org/api/ip"   # {"IsTor": bool, "IP": "..."}
IP_URL = "https://api.ipify.org"
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


class TorError(RuntimeError):
    """Tor was requested but cannot be used safely."""


def _session(tor: bool) -> requests.Session:
    s = requests.session()
    s.headers["User-Agent"] = USER_AGENT
    s.proxies = {"http": TOR_PROXY, "https": TOR_PROXY} if tor else {"http": None, "https": None}
    return s


def session() -> requests.Session:
    """Session for module traffic: through Tor when `tor on` is active."""
    return _session(vars.tor)


def presession() -> requests.Session:
    """Kept for compatibility with older modules; same as session()."""
    return session()


def proxy_listening(timeout: float = 2.0) -> bool:
    """True when something accepts connections on the Tor SOCKS port."""
    try:
        with socket.create_connection((TOR_HOST, TOR_PORT), timeout=timeout):
            return True
    except OSError:
        return False


def verify(timeout: float = 30) -> tuple[bool, str]:
    """(is_tor, exit_ip) as reported by check.torproject.org via the proxy."""
    try:
        data = _session(tor=True).get(CHECK_URL, timeout=timeout).json()
    except requests.exceptions.InvalidSchema as e:  # PySocks missing
        raise TorError("SOCKS support missing: pip install PySocks") from e
    except (requests.RequestException, ValueError) as e:
        raise TorError(f"Tor check failed: {type(e).__name__}") from e
    return bool(data.get("IsTor")), str(data.get("IP", "?"))


def initcheck() -> str:
    """Record the direct (non-Tor) public IP, for display only."""
    vars.initip = _session(tor=False).get(IP_URL, timeout=15).text.strip()
    return vars.initip


def torpipe(controller: bool) -> bool:
    """Switch Tor routing on/off. Turning it on requires a verified Tor exit.

    Returns True on success. On failure Tor stays OFF and the reason is printed.
    """
    from core.Core.colors import R, color

    def fail(msg: str) -> bool:
        vars.tor = False
        print(f"{R} [-] {color.END}{color.UNDERLINE}\033[1m{msg}{color.END}")
        return False

    if not controller:
        vars.tor = False
        return True
    if not proxy_listening():
        return fail(f"No Tor SOCKS proxy on {TOR_HOST}:{TOR_PORT}. Is the tor service running?")
    try:
        is_tor, exit_ip = verify()
    except TorError as e:
        return fail(str(e))
    if not is_tor:
        return fail(f"Traffic via {TOR_HOST}:{TOR_PORT} does NOT exit through Tor "
                    f"(exit IP {exit_ip}). Refusing to enable Tor mode.")
    vars.tor = True
    before = f"{vars.initip} > " if vars.initip else ""
    print(f" [+] Verified Tor exit (check.torproject.org). IP {before}{exit_ip}")
    return True


def torcheck() -> bool:
    """Re-verify a running Tor session; turns Tor mode off if it's broken."""
    if not vars.tor:
        return False
    try:
        ok, _ = verify()
    except TorError:
        ok = False
    if not ok:
        vars.tor = False
        raise TorError("Tor exit could not be verified any more; Tor mode switched OFF.")
    return True
