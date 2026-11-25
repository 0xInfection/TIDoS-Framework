#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shodan host intel -- what Shodan knows about the target's IP (banners, CVEs, tags...)."""

from __future__ import annotations

from core.methods import modkit as kit
from core.methods.print import pscan

info = ("Host intelligence from Shodan. With SHODAN_API_KEY the full host record is used: "
        "service banners, known CVEs, tags, geolocation/ASN, CPEs and SSL/HTTP details. "
        "Without a key the free Shodan InternetDB is used: open ports, CPEs, hostnames, "
        "tags and known CVEs (no banners or per-service detail).")
searchinfo = "Shodan Host Intel"
properties = {}

SHODAN = "https://api.shodan.io/shodan/host/"
INTERNETDB = "https://internetdb.shodan.io/"

# tags worth flagging rather than just listing
RISKY_TAGS = {"honeypot", "compromised", "malware", "self-signed", "tor", "vpn", "c2"}


def api_error(resp) -> str:
    try:
        return str(resp.json().get("error") or resp.reason)
    except ValueError:
        return resp.reason or f"HTTP {resp.status_code}"


def fetch(url: str, params: dict | None = None):
    """(status, json) of a Shodan request; (None, None) after reporting
    network errors. Never echoes the URL: it may carry the API key."""
    try:
        resp = kit.http(timeout=30).get(url, params=params)
    except Exception as e:
        kit.bad(f"Shodan unreachable: {type(e).__name__}")
        return None, None
    try:
        data = resp.json() if resp.status_code == 200 else None
    except ValueError:
        kit.bad("Shodan returned an unreadable answer.")
        return None, None
    if resp.status_code not in (200, 404):
        kit.bad(f"Shodan refused the request (HTTP {resp.status_code}): {api_error(resp)}")
        return None, None
    return resp.status_code, data


# --------------------------------------------------------------------------
# field extraction (defensive: Shodan omits most keys on most hosts)
# --------------------------------------------------------------------------

def cve_list(vulns) -> list[str]:
    """CVE ids from a top-level list or a per-service {CVE: {...}} dict.
    Shodan prefixes verified vulns with '!' and may carry a CVSS score."""
    out = []
    if isinstance(vulns, dict):
        for cve, meta in vulns.items():
            label = cve.lstrip("!")
            if isinstance(meta, dict):
                cvss = meta.get("cvss")
                if cvss not in (None, "", []):
                    label += f" (CVSS {cvss})"
                if meta.get("verified") or cve.startswith("!"):
                    label += " [verified]"
            out.append(label)
    elif isinstance(vulns, (list, tuple, set)):
        out = [str(c).lstrip("!") for c in vulns]
    return sorted(set(out))


def location(data: dict) -> str:
    loc = data.get("location") or {}
    city = data.get("city") or loc.get("city")
    country = (data.get("country_name") or loc.get("country_name")
               or data.get("country_code") or loc.get("country_code"))
    return ", ".join(p for p in (city, country) if p)


def ssl_summary(ssl: dict) -> list[str]:
    cert = ssl.get("cert") or {}
    rows = []
    cn = (cert.get("subject") or {}).get("CN")
    issuer = (cert.get("issuer") or {}).get("CN")
    if cn:
        rows.append(f"cert CN={cn}")
    if issuer:
        rows.append(f"issuer={issuer}")
    if cert.get("expires"):
        rows.append(f"expires {cert['expires']}" + (" (EXPIRED)" if cert.get("expired") else ""))
    supported = [v for v in (ssl.get("versions") or []) if not str(v).startswith("-")]
    if supported:
        rows.append("TLS: " + ", ".join(supported))
    if ssl.get("jarm"):
        rows.append(f"JARM {ssl['jarm']}")
    return rows


def http_summary(http: dict) -> list[str]:
    rows = []
    if http.get("server"):
        rows.append(f"server={http['server']}")
    if http.get("title"):
        rows.append(f"title={str(http['title']).strip()!r}")
    if http.get("waf"):
        rows.append(f"WAF={http['waf']}")
    components = http.get("components") or {}
    if components:
        rows.append("tech: " + ", ".join(sorted(components)))
    return rows


def cpes(item: dict) -> list[str]:
    value = item.get("cpe23") or item.get("cpe") or []
    return value if isinstance(value, list) else [value]


# --------------------------------------------------------------------------
# premium (keyed) host record
# --------------------------------------------------------------------------

def show_service(item: dict) -> str:
    """Print one service entry with its enrichment; return the line to store."""
    port = item.get("port")
    transport = item.get("transport") or "tcp"
    product = " ".join(str(item[k]) for k in ("product", "version") if item.get(k))
    print()
    kit.found(f"Port {port}/{transport}", product or (item.get("_shodan") or {}).get("module", "?"))
    stored = [f"Port {port}/{transport} {product}".strip()]

    cpe = cpes(item)
    if cpe:
        kit.bullet("CPE: " + ", ".join(cpe))
        stored.append("CPE: " + ", ".join(cpe))

    banner = str(item.get("data") or "").strip()
    shown = [ln.rstrip() for ln in banner.splitlines() if ln.strip()]
    for line in shown[:15]:
        print(f"    {line}")
    if len(shown) > 15:
        print(f"    ... ({len(shown) - 15} more lines)")
    if banner:
        stored.append(banner)

    for row in ssl_summary(item.get("ssl") or {}) + http_summary(item.get("http") or {}):
        kit.bullet(row)
        stored.append(row)

    cves = cve_list(item.get("vulns"))
    if cves:
        kit.warn(f"Known CVEs: {', '.join(cves)}")
        stored.append("CVEs: " + ", ".join(cves))
    return "\n".join(stored)


def shodan_host(ip: str, key: str) -> list[str] | None:
    status, data = fetch(SHODAN + ip, {"key": key})
    if status is None:
        return None
    if status == 404 or not data:
        kit.bad(f"Shodan has no information about {ip}.")
        return []

    summary = [("Organization", data.get("org")), ("ISP", data.get("isp")),
               ("ASN", data.get("asn")), ("OS", data.get("os")),
               ("Location", location(data)),
               ("Hostnames", ", ".join(data.get("hostnames") or [])),
               ("Domains", ", ".join(data.get("domains") or [])),
               ("Last update", data.get("last_update"))]
    kit.kv_table(summary)
    lines = [f"{k}: {v}" for k, v in summary if v not in (None, "", [])]

    tags = data.get("tags") or []
    if tags:
        flagged = sorted(set(tags) & RISKY_TAGS)
        kit.found("Tags", ", ".join(tags))
        if flagged:
            kit.warn(f"Noteworthy tags: {', '.join(flagged)}")
        lines.append("Tags: " + ", ".join(tags))

    cves = cve_list(data.get("vulns"))
    if cves:
        kit.warn(f"{len(cves)} known CVE(s) across all services: {', '.join(cves)}")
        lines.append("CVEs: " + ", ".join(cves))

    services = sorted(data.get("data") or [], key=lambda i: i.get("port") or 0)
    lines += [show_service(item) for item in services]
    return lines


# --------------------------------------------------------------------------
# free (keyless) InternetDB record
# --------------------------------------------------------------------------

def internetdb(ip: str) -> list[str] | None:
    kit.warn("No SHODAN_API_KEY: using the free InternetDB (ports, CPEs, tags and CVEs; no banners).")
    status, data = fetch(INTERNETDB + ip)
    if status is None:
        return None
    if status == 404 or not data:
        kit.bad(f"InternetDB has no information about {ip}.")
        return []
    rows = [("Ports", ", ".join(map(str, data.get("ports") or []))),
            ("CPEs", ", ".join(data.get("cpes") or [])),
            ("Hostnames", ", ".join(data.get("hostnames") or [])),
            ("Tags", ", ".join(data.get("tags") or [])),
            ("Vulns", ", ".join(sorted(data.get("vulns") or [])))]
    kit.kv_table(rows)
    flagged = sorted(set(data.get("tags") or []) & RISKY_TAGS)
    if flagged:
        kit.warn(f"Noteworthy tags: {', '.join(flagged)}")
    if data.get("vulns"):
        kit.warn(f"{len(data['vulns'])} known CVE(s); set SHODAN_API_KEY for per-service detail.")
    return [f"{k} :> {v}" for k, v in rows if v]


def shodan_intel(web):
    pscan("shodan host intel")
    ip = kit.resolve(web)
    if not ip:
        kit.bad(f"Cannot resolve {kit.host(web)}.")
        return []
    kit.found("Target IP", ip)
    key = kit.apikey("SHODAN_API_KEY", quiet=True)
    kit.info("Querying Shodan..." if key else "Querying Shodan InternetDB (free)...")
    lines = shodan_host(ip, key) if key else internetdb(ip)
    if lines is None:
        return []

    record = kit.Recorder(web, kit.SCAN, "shodan")
    if lines:
        record(lines)
        kit.good("Shodan host intel done!")
    else:
        record(f"Shodan has no information about {ip}")
    return lines


def attack(web):
    shodan_intel(web)
