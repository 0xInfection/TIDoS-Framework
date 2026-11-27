#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""SSL certificate info -- dumps the target's TLS certificate and session details."""

import hashlib
import os
import socket
import ssl
import tempfile
from datetime import datetime, timezone
from urllib.parse import urlsplit

from core.methods import modkit as kit
from core.methods.print import posintact

info = ("Connects to the target over TLS (SNI aware, any port) and displays the "
        "certificate: subject, issuer, validity, SANs, serial, fingerprint, whether "
        "it is trusted, and the negotiated protocol/cipher. PORT defaults to the "
        "target's port for https:// URLs, else 443.")
searchinfo = "SSL Cert Info"
properties = {
    "PORT": ["TLS port to connect to", ""],
}


def default_port(web) -> int:
    parts = urlsplit(kit.url(web))
    try:
        if parts.scheme == "https" and parts.port:
            return parts.port
    except ValueError:
        pass
    return 443


def handshake(host, port, verify):
    """TLS handshake; returns (DER cert, cipher tuple, protocol)."""
    ctx = ssl.create_default_context()
    if not verify:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    # CPython only sends SNI for names; for IPs it matches the cert's IP SANs.
    with socket.create_connection((host, port), timeout=kit.DEFAULT_TIMEOUT) as raw:
        with ctx.wrap_socket(raw, server_hostname=host) as tls:
            return tls.getpeercert(binary_form=True), tls.cipher(), tls.version()


def decode(der):
    """Parse a DER certificate into getpeercert()-style dict (stdlib only)."""
    fd, path = tempfile.mkstemp(suffix=".pem")
    try:
        with os.fdopen(fd, "w") as fh:
            fh.write(ssl.DER_cert_to_PEM_cert(der))
        return ssl._ssl._test_decode_cert(path)
    except Exception:
        return {}
    finally:
        os.unlink(path)


def name(rdns):
    return ", ".join(f"{k}={v}" for rdn in rdns or () for k, v in rdn)


def describe(cert, der, cipher, proto, trusted):
    not_after = cert.get("notAfter")
    days = None
    if not_after:
        expiry = datetime.fromtimestamp(ssl.cert_time_to_seconds(not_after), timezone.utc)
        days = (expiry - datetime.now(timezone.utc)).days
    sans = [v for k, v in cert.get("subjectAltName", ()) if k in ("DNS", "IP Address")]
    return [
        ("Subject", name(cert.get("subject"))),
        ("Issuer", name(cert.get("issuer"))),
        ("Self-signed", "yes" if cert.get("subject") == cert.get("issuer") else "no"),
        ("Trusted", trusted),
        ("Valid from", cert.get("notBefore")),
        ("Valid until", f"{not_after} ({days} days left)" if days is not None else not_after),
        ("Alt names", ", ".join(sans)),
        ("Serial number", cert.get("serialNumber")),
        ("Version", cert.get("version")),
        ("SHA-256", hashlib.sha256(der).hexdigest()),
        ("Protocol", proto),
        ("Cipher suite", cipher[0]),
        ("Cipher bits", cipher[2]),
    ]


def sslcert(web):
    posintact("ssl certificate info")
    record = kit.Recorder(web, kit.ACTIVE, "sslcert")
    host = kit.host(web)
    port = kit.integer(properties, "PORT", "TLS port", default_port(web))

    kit.info(f"Connecting to {host}:{port}...")
    try:
        der, cipher, proto = handshake(host, port, verify=False)
    except (OSError, ssl.SSLError) as e:
        kit.bad(f"TLS handshake with {host}:{port} failed: {e}")
        return {}

    try:
        handshake(host, port, verify=True)
        trusted = "yes"
    except ssl.SSLCertVerificationError as e:
        trusted = f"no ({e.verify_message})"
    except (OSError, ssl.SSLError) as e:
        trusted = f"unknown ({type(e).__name__})"

    cert = decode(der)
    if not cert:
        kit.warn("Could not decode the certificate; showing session details only.")
    details = describe(cert, der, cipher, proto, trusted)
    kit.good("Certificate retrieved")
    kit.kv_table(details)
    record("\n".join(f"{k} :> {v}" for k, v in details if v not in (None, "")))
    return cert


def attack(web):
    sslcert(web)
