#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""SSL/TLS scanner -- protocol versions, cipher suites, certificate and known TLS flaws."""

from __future__ import annotations

import re
import socket
import ssl
import warnings
from datetime import datetime, timezone
from urllib.parse import urlsplit

from core import variables
from core.methods import modkit as kit
from core.methods.print import pscan

info = ("SSL/TLS enumeration: lists the protocol versions (SSLv2 to TLS 1.3) and "
        "cipher suites the server accepts, flags weak protocols (SSLv2/3, TLS "
        "1.0/1.1) and weak ciphers (NULL, anonymous, EXPORT, RC4, DES/3DES, MD5), "
        "summarises the certificate and checks Heartbleed, ROBOT, OpenSSL CCS "
        "injection, TLS compression (CRIME), insecure renegotiation and "
        "TLS_FALLBACK_SCSV. Uses sslyze, or the ssl module (protocols only) when "
        "sslyze is missing. PORT defaults to the URL's port for https:// targets, "
        "else 443. Direct connections: this does not go through Tor.")
searchinfo = "SSL Enumeration module"
properties = {
    "PORT": ["TLS port to scan", ""],
}

PROTOCOLS = (  # (sslyze attribute, label, weak)
    ("ssl_2_0_cipher_suites", "SSLv2", True),
    ("ssl_3_0_cipher_suites", "SSLv3", True),
    ("tls_1_0_cipher_suites", "TLS 1.0", True),
    ("tls_1_1_cipher_suites", "TLS 1.1", True),
    ("tls_1_2_cipher_suites", "TLS 1.2", False),
    ("tls_1_3_cipher_suites", "TLS 1.3", False),
)
WEAK_CIPHER = re.compile(r"NULL|EXPORT|EXP\d*[_-]|anon|ADH|AECDH|RC4|RC2|3DES|DES-CBC3|_DES_|DES[_-]CBC|IDEA|MD5", re.I)
NO_PFS = re.compile(r"^TLS_RSA_")


def default_port(web) -> int:
    parts = urlsplit(kit.url(web))
    try:
        if parts.scheme == "https" and parts.port:
            return parts.port
    except ValueError:
        pass
    return 443


def weakness(name: str, key_size: int = 256, anonymous: bool = False) -> str:
    """Why a cipher suite is weak ('' when it isn't)."""
    if anonymous or re.search(r"anon|ADH|AECDH", name, re.I):
        return "anonymous key exchange"
    m = WEAK_CIPHER.search(name)
    if m:
        return m.group(0).strip("_-")
    if key_size and key_size < 112:
        return f"{key_size}-bit key"
    return ""


def reachable(host, port) -> str:
    """'' if a TCP connection can be opened, else why not."""
    try:
        with socket.create_connection((host, port), timeout=kit.DEFAULT_TIMEOUT):
            return ""
    except OSError as e:
        return e.strerror or type(e).__name__


NOT_TLS = ("WRONG_VERSION_NUMBER", "RECORD_LAYER_FAILURE", "HTTP_REQUEST", "PACKET_LENGTH_TOO_LONG")


def speaks_tls(host, port) -> str:
    """'' unless the port clearly is not TLS (plain-text reply, or silence)."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        ctx.set_ciphers("ALL:@SECLEVEL=0")
        ctx.minimum_version = ssl.TLSVersion.MINIMUM_SUPPORTED
    except (ValueError, ssl.SSLError):
        pass
    try:
        with socket.create_connection((host, port), timeout=5) as raw:
            with ctx.wrap_socket(raw, server_hostname=host):
                return ""
    except socket.timeout:
        return "no answer to a TLS ClientHello"
    except ssl.SSLError as e:
        if any(r in str(e) for r in NOT_TLS):
            return "the server answered in plain text"
        return ""  # a TLS peer we cannot talk to locally: let sslyze try
    except OSError as e:
        return e.strerror or type(e).__name__


# --------------------------------------------------------------------------
# sslyze
# --------------------------------------------------------------------------

def run_sslyze(host, port):
    """Completed sslyze ServerScanResult, or an error string."""
    from sslyze import (Scanner, ScanCommand, ServerNetworkConfiguration, ServerNetworkLocation,
                        ServerScanRequest, ServerScanStatusEnum)
    from sslyze.errors import ServerHostnameCouldNotBeResolved

    commands = {
        ScanCommand.CERTIFICATE_INFO, ScanCommand.SSL_2_0_CIPHER_SUITES, ScanCommand.SSL_3_0_CIPHER_SUITES,
        ScanCommand.TLS_1_0_CIPHER_SUITES, ScanCommand.TLS_1_1_CIPHER_SUITES, ScanCommand.TLS_1_2_CIPHER_SUITES,
        ScanCommand.TLS_1_3_CIPHER_SUITES, ScanCommand.HEARTBLEED, ScanCommand.ROBOT,
        ScanCommand.OPENSSL_CCS_INJECTION, ScanCommand.TLS_COMPRESSION, ScanCommand.SESSION_RENEGOTIATION,
        ScanCommand.TLS_FALLBACK_SCSV,
    }
    try:
        location = ServerNetworkLocation(hostname=host, port=port)
    except ServerHostnameCouldNotBeResolved:
        return f"could not resolve {host}"
    request = ServerScanRequest(
        server_location=location,
        network_configuration=ServerNetworkConfiguration(
            tls_server_name_indication=host, network_timeout=kit.DEFAULT_TIMEOUT, network_max_retries=1),
        scan_commands=commands,
    )
    with warnings.catch_warnings():
        # sslyze's bundled trust stores trip cryptography deprecation warnings
        warnings.filterwarnings("ignore", module=r"sslyze\.")
        scanner = Scanner()
        scanner.queue_scans([request])
        for result in scanner.get_results():
            if result.scan_status == ServerScanStatusEnum.ERROR_NO_CONNECTIVITY:
                trace = result.connectivity_error_trace
                reason = str(trace).strip().splitlines()[-1] if trace else "no TLS handshake"
                return reason[:200]
            return result
    return "no result"


def attempt(scan, attr):
    """Result of one sslyze scan command, None if it errored."""
    from sslyze import ScanCommandAttemptStatusEnum
    a = getattr(scan.scan_result, attr)
    if a.status == ScanCommandAttemptStatusEnum.COMPLETED:
        return a.result
    if a.status == ScanCommandAttemptStatusEnum.ERROR:
        kit.warn(f"{attr.replace('_', ' ')} check failed: {a.error_reason.name if a.error_reason else '?'}")
    return None


def report_protocols(scan, lines):
    kit.info("Protocols and cipher suites:")
    supported = []
    for attr, label, weak in PROTOCOLS:
        res = attempt(scan, attr)
        if res is None:
            continue
        accepted = res.accepted_cipher_suites
        if not accepted:
            continue
        supported.append(label)
        if weak:
            kit.warn(f"{label} supported (weak protocol): {len(accepted)} cipher suites")
        else:
            kit.found(f"{label} supported", f"{len(accepted)} cipher suites")
        weak_suites = []
        for c in accepted:
            suite = c.cipher_suite
            why = weakness(suite.name, suite.key_size, suite.is_anonymous)
            note = f"  [WEAK: {why}]" if why else ("  [no forward secrecy]" if NO_PFS.search(suite.name) else "")
            kit.bullet(f"{suite.name} ({suite.key_size} bits){note}", indent=5)
            if why:
                weak_suites.append(f"{suite.name} ({why})")
        lines.append(f"{label} :> " + ", ".join(c.cipher_suite.name for c in accepted))
        if weak_suites:
            lines.append(f"Weak ciphers ({label}) :> " + ", ".join(weak_suites))
    if not supported:
        kit.bad("No protocol version accepted any cipher suite.")
    weak = [label for _, label, w in PROTOCOLS if w and label in supported]
    if weak:
        lines.append("Weak protocols :> " + ", ".join(weak))


def _name(x509_name) -> str:
    try:
        return x509_name.rfc4514_string()
    except Exception:
        return str(x509_name)


def report_certificate(scan, lines):
    res = attempt(scan, "certificate_info")
    if not res or not res.certificate_deployments:
        return
    dep = res.certificate_deployments[0]
    chain = dep.received_certificate_chain
    if not chain:
        return
    leaf = chain[0]
    from cryptography import x509
    from cryptography.hazmat.primitives.asymmetric import ec, rsa

    try:
        sans = leaf.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
        alt = ", ".join(str(v) for v in sans.get_values_for_type(x509.DNSName) + [
            str(i) for i in sans.get_values_for_type(x509.IPAddress)])
    except x509.ExtensionNotFound:
        alt = ""
    key = leaf.public_key()
    if isinstance(key, rsa.RSAPublicKey):
        key_desc = f"RSA {key.key_size} bits"
    elif isinstance(key, ec.EllipticCurvePublicKey):
        key_desc = f"EC {key.curve.name}"
    else:
        key_desc = type(key).__name__.lstrip("_")
    not_before = getattr(leaf, "not_valid_before_utc", None) or leaf.not_valid_before.replace(tzinfo=timezone.utc)
    not_after = getattr(leaf, "not_valid_after_utc", None) or leaf.not_valid_after.replace(tzinfo=timezone.utc)
    days = (not_after - datetime.now(timezone.utc)).days
    trusted = [p.trust_store.name for p in dep.path_validation_results if p.verified_certificate_chain]
    errors = [p.validation_error for p in dep.path_validation_results if p.validation_error]
    reason = "self-signed" if leaf.subject == leaf.issuer else (
        errors[0].split(" (encountered")[0].replace("validation failed: ", "")[:100] if errors else "unknown")
    sig_hash = leaf.signature_hash_algorithm.name if leaf.signature_hash_algorithm else "?"
    details = [
        ("Subject", _name(leaf.subject)),
        ("Issuer", _name(leaf.issuer)),
        ("Self-signed", "yes" if leaf.subject == leaf.issuer else "no"),
        ("Alt names", alt),
        ("Valid from", not_before.strftime("%Y-%m-%d")),
        ("Valid until", f"{not_after:%Y-%m-%d} ({'EXPIRED' if days < 0 else f'{days} days left'})"),
        ("Public key", key_desc),
        ("Signature hash", sig_hash),
        ("Chain length", len(chain)),
        ("Trusted by", ", ".join(trusted) if trusted else f"none ({reason})"),
    ]
    kit.info("Certificate:")
    kit.kv_table(details)
    lines.append("Cert Info :> " + "; ".join(f"{k}: {v}" for k, v in details if v not in ("", None)))
    if days < 0:
        kit.warn("The certificate has expired.")
    if sig_hash in ("md5", "sha1"):
        kit.warn(f"The certificate is signed with {sig_hash.upper()}.")
    if isinstance(key, rsa.RSAPublicKey) and key.key_size < 2048:
        kit.warn(f"Weak RSA key ({key.key_size} bits).")


def report_vulnerabilities(scan, lines):
    from sslyze import RobotScanResultEnum

    checks = []
    r = attempt(scan, "heartbleed")
    if r is not None:
        checks.append(("Heartbleed (CVE-2014-0160)", r.is_vulnerable_to_heartbleed))
    r = attempt(scan, "openssl_ccs_injection")
    if r is not None:
        checks.append(("OpenSSL CCS injection (CVE-2014-0224)", r.is_vulnerable_to_ccs_injection))
    r = attempt(scan, "robot")
    if r is not None:
        vulnerable = r.robot_result in (RobotScanResultEnum.VULNERABLE_WEAK_ORACLE,
                                        RobotScanResultEnum.VULNERABLE_STRONG_ORACLE)
        checks.append((f"ROBOT ({r.robot_result.name.lower()})", vulnerable))
    r = attempt(scan, "tls_compression")
    if r is not None:
        checks.append(("TLS compression (CRIME)", r.supports_compression))
    r = attempt(scan, "session_renegotiation")
    if r is not None:
        checks.append(("Insecure renegotiation", not r.supports_secure_renegotiation))
        checks.append(("Client-initiated renegotiation DoS", r.is_vulnerable_to_client_renegotiation_dos))
    r = attempt(scan, "tls_fallback_scsv")
    if r is not None:
        checks.append(("Downgrade attacks (no TLS_FALLBACK_SCSV)", not r.supports_fallback_scsv))

    kit.info("Known TLS issues:")
    for label, vulnerable in checks:
        if vulnerable:
            kit.warn(f"{label}: VULNERABLE")
        else:
            kit.bullet(f"{label}: not vulnerable")
    issues = [label for label, vulnerable in checks if vulnerable]
    lines.append("Issues :> " + (", ".join(issues) if issues else "none found"))


# --------------------------------------------------------------------------
# stdlib fallback
# --------------------------------------------------------------------------

def stdlib_scan(host, port, lines):
    """Protocol support via the ssl module (limited to what local OpenSSL allows)."""
    kit.warn("sslyze is not available: checking protocol versions only (pip install sslyze).")
    versions = [("TLS 1.0", ssl.TLSVersion.TLSv1, True), ("TLS 1.1", ssl.TLSVersion.TLSv1_1, True),
                ("TLS 1.2", ssl.TLSVersion.TLSv1_2, False), ("TLS 1.3", ssl.TLSVersion.TLSv1_3, False)]
    supported = []
    for label, version, weak in versions:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        try:
            ctx.set_ciphers("ALL:@SECLEVEL=0")
            ctx.minimum_version = ctx.maximum_version = version
            with socket.create_connection((host, port), timeout=kit.DEFAULT_TIMEOUT) as raw:
                with ctx.wrap_socket(raw, server_hostname=host) as tls:
                    cipher = tls.cipher()[0]
        except (OSError, ValueError, ssl.SSLError):
            continue
        supported.append(label)
        why = weakness(cipher)
        if weak or why:
            kit.warn(f"{label} supported" + (" (weak protocol)" if weak else "") + f": {cipher}"
                     + (f" [WEAK: {why}]" if why else ""))
        else:
            kit.found(f"{label} supported", cipher)
        lines.append(f"{label} :> {cipher}")
    if not supported:
        kit.bad("No protocol version could be negotiated (local OpenSSL may not support legacy versions).")
    return supported


# --------------------------------------------------------------------------

def ssltlsscan(web):
    pscan("ssl enumeration")
    record = kit.Recorder(web, kit.SCAN, "ssltlsscan")
    host = kit.host(web)
    port = kit.integer(properties, "PORT", "TLS port", default_port(web))
    if variables.tor:
        kit.warn("Tor is on, but TLS probing uses direct connections: your IP is exposed to the target.")

    kit.info(f"Testing {host}:{port}...")
    why = reachable(host, port)
    if why:
        kit.bad(f"Cannot connect to {host}:{port}: {why}")
        return []

    why = speaks_tls(host, port)
    if why:
        kit.bad(f"{host}:{port} does not speak TLS ({why}).")
        return []

    lines = []
    try:
        scan = run_sslyze(host, port)
    except ImportError:
        stdlib_scan(host, port, lines)
    else:
        if isinstance(scan, str):
            kit.bad(f"No TLS service on {host}:{port} ({scan}).")
            return []
        probe = scan.connectivity_result
        kit.good(f"TLS service found (highest version: {probe.highest_tls_version_supported.name}, "
                 f"cipher: {probe.cipher_suite_supported})")
        report_protocols(scan, lines)
        report_certificate(scan, lines)
        report_vulnerabilities(scan, lines)

    if lines:
        record(lines)
    kit.good("SSL/TLS scan completed!")
    return lines


def attack(web):
    ssltlsscan(web)
