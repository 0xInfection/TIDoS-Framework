#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Cloudflare misconfiguration -- is the origin server reachable around Cloudflare?"""

from __future__ import annotations

import ipaddress
import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlsplit

import requests
from requests.adapters import HTTPAdapter

import core.variables as variables
from core.methods import dnsmisc
from core.methods import modkit as kit
from core.methods.inject import ratio
from core.methods.print import pvln
from core.methods.mailauth import parse_spf, spf_records
from modules.OSINTFootprinting.ActiveRecon.serverdetect import serverdetect

info = ("This module searches for Cloudflare misconfigurations. It confirms the target is "
        "behind Cloudflare (Server/CF-RAY headers, Cloudflare IP ranges), then (BYPASS) "
        "collects non-Cloudflare IPs of the domain -- common unproxied subdomains (direct, "
        "origin, mail, ftp, cpanel, dev...), MX hosts, SPF ip4/a/mx entries and, with PASSIVE, "
        "HackerTarget host records -- and requests the site from each IP with the right Host "
        "header/SNI. An IP serving the same page is an exposed origin: attackers can bypass "
        "the Cloudflare WAF and DDoS protection by connecting to it directly.")
searchinfo = "Cloudflare Misconfig & Bypass"
properties = {
    "BYPASS": ["Hunt for the origin IP behind Cloudflare (y/n or 1/0)", ""],
    "PASSIVE": ["Also use HackerTarget host records as candidates (y/n)", ""],
}

# https://www.cloudflare.com/ips/ (stable for years)
CF_RANGES = [ipaddress.ip_network(n) for n in (
    "173.245.48.0/20", "103.21.244.0/22", "103.22.200.0/22", "103.31.4.0/22",
    "141.101.64.0/18", "108.162.192.0/18", "190.93.240.0/20", "188.114.96.0/20",
    "197.234.240.0/22", "198.41.128.0/17", "162.158.0.0/15", "104.16.0.0/13",
    "104.24.0.0/14", "172.64.0.0/13", "131.0.72.0/22",
    "2400:cb00::/32", "2606:4700::/32", "2803:f800::/32", "2405:b500::/32",
    "2405:8100::/32", "2a06:98c0::/29", "2c0f:f248::/32")]

LABELS = ("direct", "direct-connect", "origin", "origin-www", "www-origin", "backend", "server",
          "cpanel", "whm", "webmail", "mail", "smtp", "pop", "imap", "ftp", "sftp", "dev",
          "staging", "stage", "test", "beta", "old", "admin", "vpn", "remote", "ns1", "ns2",
          "autodiscover", "api", "app", "portal", "blog", "shop")
MAX_CANDIDATES = 40
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)


def is_cloudflare(ip: str) -> bool:
    try:
        a = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return any(a in net for net in CF_RANGES if net.version == a.version)


def routable(ip: str) -> bool:
    try:
        return ipaddress.ip_address(ip).is_global
    except ValueError:
        return False


class SNIAdapter(HTTPAdapter):
    """Connect to an IP while sending the site's name as TLS SNI."""

    def __init__(self, server_hostname: str, **kw):
        self.server_hostname = server_hostname
        super().__init__(**kw)

    def init_poolmanager(self, *args, **kw):
        kw["server_hostname"] = self.server_hostname
        super().init_poolmanager(*args, **kw)

    def proxy_manager_for(self, proxy, **kw):
        kw["server_hostname"] = self.server_hostname
        return super().proxy_manager_for(proxy, **kw)


def title(text: str) -> str:
    m = TITLE.search(text or "")
    return " ".join(m.group(1).split())[:120] if m else ""


def same_site(ref, resp) -> str:
    """Why `resp` (from a candidate IP) is the same page as `ref`, or ''."""
    if "cf-ray" in {k.lower() for k in resp.headers}:
        return ""
    if ref.status_code != resp.status_code:
        return ""
    if ref.is_redirect:
        a = ref.headers.get("Location", "")
        return f"same redirect ({a})" if a and a == resp.headers.get("Location", "") else ""
    t = title(ref.text)
    if t and t == title(resp.text):
        return f"same title '{t}'"
    r = ratio(ref.text, resp.text)
    return f"{r:.0%} identical body" if r >= 0.9 and len(ref.text) > 200 else ""


def candidates(host: str, domain: str, passive: bool) -> dict[str, set]:
    """ip -> sources, for non-Cloudflare public IPs related to the domain."""
    found: dict[str, set] = {}

    def add(ip, source):
        if routable(ip) and not is_cloudflare(ip):
            found.setdefault(ip, set()).add(source)

    names = {domain, host} | {f"{label}.{domain}" for label in LABELS}
    mx = dnsmisc.mx(domain)
    names |= set(mx)
    spf = spf_records(dnsmisc.txt(domain))
    if spf:
        for term in spf[0].split()[1:]:
            mech = term.lstrip("+~?-").lower()
            kind, _, val = mech.partition(":")
            if kind == "ip4" and (val.endswith("/32") or "/" not in val):
                add(val.split("/")[0], "SPF ip4")
            elif kind in ("a", "mx") and val:
                names.add(val.split("/")[0])
        parsed = parse_spf(spf[0])
        names |= {i for i in parsed.includes if i.endswith(domain)}

    with ThreadPoolExecutor(max_workers=max(1, min(variables.processes, 16))) as pool:
        for name, ips in zip(names, pool.map(lambda n: dnsmisc.addresses(n, ipv6=False), names)):
            for ip in ips:
                add(ip, f"{'MX ' if name in mx else ''}{name}")

    if passive:
        text = kit.hackertarget("hostsearch", domain, timeout=40)
        for line in (text or "").splitlines():
            name, _, ip = line.partition(",")
            if ip:
                add(ip.strip(), f"HackerTarget {name.strip()}")
    return found


def check_ip(ip: str, host: str, ref, path: str):
    """(ip, scheme, reason) when the IP serves the site, else None."""
    for scheme in ("https", "http"):
        s = kit.http(timeout=8)
        if scheme == "https":
            s.mount("https://", SNIAdapter(host))
        netloc = f"[{ip}]" if ":" in ip else ip
        try:
            r = s.get(f"{scheme}://{netloc}{path}", headers={"Host": host}, allow_redirects=False)
        except requests.RequestException:
            continue
        why = same_site(ref, r)
        if why:
            return ip, scheme, why
    return None


def bypass(web, ref, host: str, domain: str, record) -> list[str]:
    kit.info("Collecting origin IP candidates (subdomains, MX, SPF)...")
    passive = kit.flag(properties, "PASSIVE", "Use HackerTarget host records", True)
    found = candidates(host, domain, passive)
    if not found:
        kit.bad("No non-Cloudflare IPs found for the domain.")
        record("Behind Cloudflare; no origin IP candidates found.")
        return []
    ips = sorted(found, key=lambda i: (-len(found[i]), i))[:MAX_CANDIDATES]
    kit.info(f"Requesting the site from {len(ips)} candidate IP(s) with Host: {host}...")
    parts = urlsplit(ref.url)
    path = (parts.path or "/") + (f"?{parts.query}" if parts.query else "")
    with ThreadPoolExecutor(max_workers=max(1, min(variables.processes, 16))) as pool:
        results = [r for r in pool.map(lambda ip: check_ip(ip, host, ref, path), ips) if r]

    origins = []
    for ip, scheme, why in results:
        src = ", ".join(sorted(found[ip]))
        kit.found("Origin server exposed", f"{ip} via {scheme} ({why}; found in: {src})")
        record(f"[HIGH] Cloudflare bypass: origin {ip} serves the site directly over {scheme} "
               f"({why}; found in: {src})")
        origins.append(ip)
    others = [ip for ip in ips if ip not in origins]
    if others:
        kit.info("Other non-Cloudflare IPs of the domain (not serving this site):")
        for ip in others[:15]:
            kit.bullet(f"{ip}  ({', '.join(sorted(found[ip]))})")
    if not origins:
        kit.good("No candidate IP serves the site: origin not exposed (as far as we can tell).")
        record("Behind Cloudflare; origin not found among "
               f"{len(ips)} candidate IPs: {', '.join(others[:15])}")
    else:
        kit.info("Restrict the origin firewall to Cloudflare IP ranges (or use Cloudflare Tunnel).")
    return origins


def cloudflaremisc(web):
    pvln("cloudflare misconfig.")
    record = kit.Recorder(web, kit.MISCONFIG, "cloudflaremisc")
    host = kit.host(web)
    domain = kit.domain(web)
    dnsmisc.warn_tor()
    ips = dnsmisc.addresses(host) if not kit.is_ip(host) else [host]
    if ips:
        kit.found("Server IP", ", ".join(ips))
    try:
        ref = kit.http().get(kit.url(web) + "/", allow_redirects=False)
    except requests.RequestException as e:
        kit.bad(f"Could not reach {kit.url(web)}: {type(e).__name__}")
        return []

    evidence = []
    if "cloudflare" in ref.headers.get("Server", "").lower():
        evidence.append("Server: cloudflare")
    if "CF-RAY" in ref.headers:
        evidence.append(f"CF-RAY: {ref.headers['CF-RAY']}")
    cf_ips = [ip for ip in ips if is_cloudflare(ip)]
    if cf_ips:
        evidence.append("IP in Cloudflare ranges: " + ", ".join(cf_ips))
    if not evidence:
        kit.bad("The website does not seem to be behind Cloudflare.")
        record("Not behind Cloudflare.")
        return []
    kit.warn("The website is behind Cloudflare: " + "; ".join(evidence))
    direct = [ip for ip in ips if not is_cloudflare(ip) and routable(ip)]
    if cf_ips and direct:
        kit.found("Partly unproxied", "the host also resolves to " + ", ".join(direct))
        record("[MEDIUM] Host also resolves to non-Cloudflare IPs: " + ", ".join(direct))

    if not kit.flag(properties, "BYPASS", "Try to find the origin IP behind Cloudflare", True):
        record("Behind Cloudflare (" + "; ".join(evidence) + ")")
        serverdetect(web)
        return []
    return bypass(web, ref, host, domain, record)


def attack(web):
    cloudflaremisc(web)
