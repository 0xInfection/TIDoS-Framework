#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""
Shared building blocks for TIDoS modules.

Every module exposes the same contract to the console / CLI / GUI:

    info       -- long description (shown by `info`)
    searchinfo -- short name (shown by `list` / `find`)
    properties -- {"OPT": ["description", "value"]} (edited with `set`)
    attack(target)

This kit keeps the boring parts out of the modules themselves:

    * target helpers   -- host(), url(), domain(), resolve()
    * options          -- option() / flag(): use the `set` value, else prompt
                          interactively, else fall back to a default (CLI/VAL)
    * HTTP             -- http(): Tor-aware session with sane timeouts
    * output           -- info(), good(), bad(), warn(), found(), bullet()
    * persistence      -- Recorder: thin wrapper around save_data()
    * files            -- wordlist(), logdir()
    * externals        -- apikey(), run_tool(), command(), hackertarget()
"""

from __future__ import annotations

import functools
import os
import re
import shutil
import socket
import subprocess
import sys
from typing import Iterable
from urllib.parse import urlsplit

import urllib3

from core.Core.colors import C, G, GR, O, R, color
from core.database.database_module import save_data
from core.methods.tor import session as _tor_session
from core.variables import database

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEFAULT_TIMEOUT = 10
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

# (module, lvl1) pairs used by the results database. Keep these strings
# stable: the GUI and older databases key on them.
PASSIVE = ("ReconANDOSINT", "Passive Reconnaissance & OSINT")
ACTIVE = ("ReconANDOSINT", "Active Reconnaissance")
INFODISC = ("ReconANDOSINT", "Information Disclosure")
SCAN = ("ScanANDEnum", "Scanning & Enumeration")
PORTSCAN = ("ScanANDEnum", "Port Scanning")
CRAWL = ("ScanANDEnum", "Crawling")
MISCONFIG = ("VulnAnalysis", "Basic Bugs & Misconfigurations")
CRITICAL = ("VulnAnalysis", "Critical Vulnerabilities")
BRUTE = ("VulnAnalysis", "Brute Force Tools")


# --------------------------------------------------------------------------
# targets
# --------------------------------------------------------------------------

def as_url(target) -> str:
    """Full URL of a target (credentials included), without trailing slash.

    Accepts a core.methods.threat.Target or a plain string. Bare hosts/IPs
    get an http:// scheme so they can be requested directly.
    """
    raw = getattr(target, "fullurl", None) or str(target)
    raw = raw.strip()
    if "://" not in raw:
        raw = "http://" + raw
    return raw.rstrip("/")


def url(target) -> str:
    """Alias of as_url(); reads better at call sites: requests.get(url(t))."""
    return as_url(target)


def host(target) -> str:
    """Bare hostname (or IP) of a target: no scheme, credentials or port."""
    name = getattr(target, "name", "")
    if name:
        return name
    return urlsplit(as_url(target)).hostname or ""


def domain(target) -> str:
    """Registrable domain of the target (example.co.uk for a.b.example.co.uk)."""
    h = host(target)
    try:
        import tldextract
        ext = tldextract.extract(h)
        if ext.domain and ext.suffix:
            return f"{ext.domain}.{ext.suffix}"
    except Exception:
        pass
    return h


def resolve(target) -> str:
    """IPv4 address of the target ('' if it does not resolve)."""
    h = host(target)
    if is_ip(h):
        return h
    try:
        return socket.gethostbyname(h)
    except (OSError, UnicodeError):
        return getattr(target, "ip", "") or ""


def is_ip(value: str) -> bool:
    return bool(re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", value or ""))


# --------------------------------------------------------------------------
# options
# --------------------------------------------------------------------------

def is_root() -> bool:
    """True when running with root privileges (needed for raw-packet scans)."""
    return hasattr(os, "geteuid") and os.geteuid() == 0


def interactive() -> bool:
    """True when we may prompt the user (console session on a TTY)."""
    try:
        return sys.stdin.isatty()
    except (AttributeError, ValueError):
        return False


def option(properties: dict, key: str, prompt: str, default: str = "") -> str:
    """Resolve a module option.

    1. value configured with `set KEY VAL` (or a VAL session file)
    2. interactive prompt (enter keeps the default)
    3. the default
    `none` is treated as an explicitly empty value.
    """
    value = ""
    if key in properties:
        value = str(properties[key][1]).strip()
    if value.lower() == "none":
        return ""
    if value:
        return value
    if interactive():
        hint = f" [{default}]" if default else ""
        try:
            answer = input(f"{O} [§] {prompt}{hint} :> {color.END}").strip()
        except EOFError:
            answer = ""
        return answer or default
    return default


def flag(properties: dict, key: str, prompt: str, default: bool = False) -> bool:
    """Boolean option: y/yes/true/1/on → True."""
    value = option(properties, key, prompt + " (y/n)", "y" if default else "n")
    return value.strip().lower() in ("y", "yes", "true", "1", "on")


def number(properties: dict, key: str, prompt: str, default: float) -> float:
    """Float option (timeouts, delays)."""
    value = option(properties, key, prompt, str(default))
    try:
        return float(value)
    except ValueError:
        warn(f"Invalid number '{value}' for {key}, using {default}.")
        return default


# Optional request extras shared by every module that talks HTTP to the target:
#     properties = {**kit.AUTH_OPTIONS, ...}
#     session = kit.http(headers=kit.request_headers(properties))
AUTH_OPTIONS = {
    "COOKIE": ["Cookie header sent with every request, e.g. 'PHPSESSID=abc; role=admin'", ""],
    "HEADERS": ["Extra request headers 'Name: value'; separate several with '||'", ""],
}


def setting(properties: dict, key: str, default: str = "") -> str:
    """A value configured with `set`, never prompted for (optional extras)."""
    value = str(properties[key][1]).strip() if key in properties else ""
    if value.lower() == "none":
        return ""
    return value or default


def parse_headers(spec: str) -> dict[str, str]:
    """'A: 1 || B: 2' (or one per line) -> {'A': '1', 'B': '2'}; bad entries are skipped."""
    headers: dict[str, str] = {}
    for item in re.split(r"\|\||[\r\n]+", spec):
        item = item.strip()
        if not item:
            continue
        name, sep, value = item.partition(":")
        name, value = name.strip(), value.strip()
        if not sep or not re.fullmatch(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+", name):
            warn(f"Ignoring malformed header '{item}' (expected 'Name: value').")
            continue
        headers[name] = value
    return headers


def request_headers(properties: dict) -> dict[str, str]:
    """Headers from the HEADERS and COOKIE options (COOKIE is merged into any Cookie header)."""
    headers = parse_headers(setting(properties, "HEADERS"))
    cookie = setting(properties, "COOKIE")
    if cookie:
        existing = {k.lower(): k for k in headers}.get("cookie")
        if existing:
            cookie = f"{headers.pop(existing)}; {cookie}"
        headers["Cookie"] = cookie
    return headers


def integer(properties: dict, key: str, prompt: str, default: int) -> int:
    value = option(properties, key, prompt, str(default))
    try:
        return int(value)
    except ValueError:
        warn(f"Invalid number '{value}' for {key}, using {default}.")
        return default


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------

def http(timeout: float = DEFAULT_TIMEOUT, headers: dict | None = None):
    """A requests session that honours `tor on`, skips TLS verification
    (we're pentesting, self-signed certs are the norm) and never hangs."""
    s = _tor_session()
    s.verify = False
    s.headers["User-Agent"] = USER_AGENT
    if headers:
        s.headers.update(headers)
    # keyword passed at call time still wins over this default
    s.request = functools.partial(s.request, timeout=timeout)
    return s


# --------------------------------------------------------------------------
# output
# --------------------------------------------------------------------------

def info(msg: str) -> None:
    print(f"{GR} [*] {msg}{color.END}")


def good(msg: str) -> None:
    print(f"{G} [+] {msg}{C}{color.TR2}{color.END}")


def bad(msg: str) -> None:
    print(f"{R} [-] {msg}{color.END}")


def warn(msg: str) -> None:
    print(f"{O} [!] {msg}{color.END}")


def found(label: str, value) -> None:
    """`[+] Label :> value` in the framework's powerline style."""
    print(f"{O} [+] {label} :> {C}{color.TR3}{C}{G}{value}{C}{color.TR2}{color.END}")


def bullet(text, indent: int = 3) -> None:
    print(f"{C}{' ' * indent}- {text}{color.END}")


def kv_table(pairs: Iterable[tuple[str, object]], indent: int = 3) -> None:
    """Aligned key/value listing (skips empty values)."""
    pairs = [(str(k), str(v)) for k, v in pairs if v not in (None, "", [])]
    if not pairs:
        return
    width = max(len(k) for k, _ in pairs)
    for k, v in pairs:
        print(f"{' ' * indent}{O}{k.ljust(width)}{color.END} : {C}{v}{color.END}")


# --------------------------------------------------------------------------
# persistence
# --------------------------------------------------------------------------

class Recorder:
    """Store findings in the session database under a fixed module path.

        rec = Recorder(target, PASSIVE, "whois")
        rec("raw whois text")
    """

    def __init__(self, target, section: tuple[str, str], lvl2: str, lvl3: str = ""):
        self.module, self.lvl1 = section
        self.lvl2 = lvl2
        self.lvl3 = lvl3
        self.host = host(target)

    def __call__(self, data) -> None:
        if not isinstance(data, (str, bytes, dict)) and hasattr(data, "__iter__"):
            data = "\n".join(str(d) for d in data)  # lists, sets, generators...
        try:
            save_data(database, self.module, self.lvl1, self.lvl2, self.lvl3, self.host, str(data))
        except Exception as e:  # never let bookkeeping kill a scan
            bad(f"Could not store result: {e}")


# --------------------------------------------------------------------------
# files
# --------------------------------------------------------------------------

def wordlist(path: str) -> list[str]:
    """Non-empty, non-comment lines of a wordlist (deduplicated, ordered)."""
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            lines = (line.strip() for line in fh)
            return list(dict.fromkeys(l for l in lines if l and not l.startswith("#")))
    except OSError as e:
        bad(f"Cannot read wordlist {path}: {e.strerror or e}")
        return []


def logdir(target) -> str:
    """tmp/logs/<host>-logs/, created on demand."""
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", host(target)) or "target"
    path = os.path.join("tmp", "logs", f"{safe}-logs")
    os.makedirs(path, exist_ok=True)
    return path


# --------------------------------------------------------------------------
# externals
# --------------------------------------------------------------------------

def apikey(name: str, quiet: bool = False) -> str:
    """API credential from the environment: $TIDOS_<NAME>, then $<NAME>.

    Returns "" when the key is not configured, and says so unless `quiet`
    (for optional keys whose absence the caller reports itself).
    Keys are never stored in the repository; see docs/setup.md.
    """
    value = (os.environ.get(f"TIDOS_{name}") or os.environ.get(name) or "").strip()
    if not value and not quiet:
        bad(f"{name} is not set: export TIDOS_{name}=... (see docs/setup.md)")
    return value


def run_tool(args: list[str], timeout: float = 120, cwd: str | None = None):
    """Run an external tool without a shell.

    Returns the subprocess.CompletedProcess (stdout, stderr, returncode) or
    None, after saying why, when the tool is missing or times out.
    """
    if not shutil.which(args[0]):
        bad(f"'{args[0]}' is not installed or not in PATH.")
        return None
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=timeout, cwd=cwd)
    except subprocess.TimeoutExpired:
        bad(f"'{os.path.basename(args[0])}' timed out after {timeout:.0f}s.")
        return None


def command(args: list[str], timeout: float = 120) -> str | None:
    """Run an external tool without a shell; stdout on success, None otherwise."""
    res = run_tool(args, timeout)
    if res is None:
        return None
    if res.returncode != 0 and not res.stdout:
        bad(f"'{args[0]}' failed: {res.stderr.strip() or res.returncode}")
        return None
    return res.stdout


HACKERTARGET = "https://api.hackertarget.com"
_HT_FAIL = ("error", "api count exceeded", "valid api key", "invalid")
_HT_EMPTY = ("no records", "no dns a records", "no results")


def hackertarget(endpoint: str, query: str, timeout: float = 30) -> str | None:
    """Plain-text answer of a HackerTarget API endpoint.

    Returns the text, "" when the API found nothing, or None (after saying
    why) on network errors, quota exhaustion or API errors. Uses
    HACKERTARGET_API_KEY when configured, the free tier otherwise.
    """
    params = {"q": query}
    key = apikey("HACKERTARGET_API_KEY", quiet=True)
    if key:
        params["apikey"] = key
    try:
        resp = http(timeout=timeout).get(f"{HACKERTARGET}/{endpoint}/", params=params)
    except Exception as e:
        bad(f"HackerTarget API unreachable: {type(e).__name__}")
        return None
    text = resp.text.strip()
    low = text.lower()
    if resp.status_code != 200 or low.startswith(_HT_FAIL):
        bad(f"HackerTarget API: {text.splitlines()[0] if text else resp.status_code}")
        return None
    return "" if low.startswith(_HT_EMPTY) else text
