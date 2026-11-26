#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Non-interactive command line for TIDoS.

Modules are addressed by a readable path, <phase>[/<subphase>]/<module>, e.g.

    tidos --list
    tidos --list osint
    tidos -u http://host -m osint/passiverecon/getgeoip
    tidos -u http://host -m osint/passiverecon        # a whole sub-phase
    tidos -u http://host -m osint/all                 # a whole phase
    tidos -u http://host -m all --tor
    tidos -u http://host -m sqli --set PARAM=/p.php?id=1 --set COOKIE=sid=abc
    tidos --info osint/passiverecon/getgeoip

Running with no arguments starts the interactive console instead.
"""

from __future__ import annotations

import argparse
import importlib
import os
import socket
import sys
from dataclasses import dataclass
from pathlib import Path

import core.variables as variables
from core.methods import modkit as kit

# Directory name -> friendly phase / sub-phase alias.
PHASE_ALIAS = {
    "OSINTFootprinting": "osint",
    "ScanningEnumeration": "scan",
    "VlnAnalysis": "vuln",
    "SploitLoot": "sploit",
    "PostSploit": "post",
    "Aid": "aid",
}
SUB_ALIAS = {
    "PassiveRecon": "passiverecon",
    "ActiveRecon": "activerecon",
    "InfoDisclose": "infodisc",
    "Misconfig": "misconfig",
    "Severe": "severe",
    "Other": "other",
    "PortScanning": "portscanning",
    "WebCrawling": "webcrawling",
}
PHASE_ORDER = ["osint", "scan", "vuln", "sploit", "post", "aid"]


@dataclass(frozen=True)
class Mod:
    path: str      # osint/passiverecon/getgeoip
    dotted: str    # modules.OSINTFootprinting.PassiveRecon.getgeoip
    info: str      # searchinfo


def _sub_alias(part: str) -> str:
    import re
    part = re.sub(r"^0x[0-9a-fA-F]+-", "", part)   # strip the 0x01- ordering prefix
    return SUB_ALIAS.get(part, part.lower())


def discover() -> list[Mod]:
    """Every runnable module (has `searchinfo` and `attack`), by friendly path.

    The `*-all` launchers are left out: whole phases/sub-phases are selected
    with the `all` path instead.
    """
    root = Path(variables.modir).resolve()
    mods: list[Mod] = []
    for f in sorted(root.glob("**/*.py")):
        stem = f.stem
        if stem.startswith("__") or "-" in stem:       # dunder files and *-all launchers
            continue
        rel = f.relative_to(root)
        if "files" in rel.parts or "__pycache__" in rel.parts:
            continue
        parts = rel.with_suffix("").parts
        dotted = "modules." + ".".join(parts)
        try:
            m = importlib.import_module(dotted)
        except Exception:
            continue
        if not (hasattr(m, "searchinfo") and callable(getattr(m, "attack", None))):
            continue
        phase = PHASE_ALIAS.get(parts[0], parts[0].lower())
        subs = [_sub_alias(p) for p in parts[1:-1]]
        path = "/".join([phase, *subs, parts[-1]])
        mods.append(Mod(path, dotted, str(getattr(m, "searchinfo", "")).strip()))
    return mods


def resolve(selector: str, registry: list[Mod]) -> list[Mod]:
    """Modules matching a selector: `all`, a phase/sub-phase prefix, a full path,
    `.../all`, or a bare module name."""
    sel = selector.strip().strip("/").lower()
    if sel in ("all", "*", ""):
        return list(registry)
    if sel.endswith("/all"):
        prefix = sel[:-4]
        return [m for m in registry if m.path == prefix or m.path.startswith(prefix + "/")]
    exact = [m for m in registry if m.path == sel]
    if exact:
        return exact
    prefix = [m for m in registry if m.path.startswith(sel + "/")]
    if prefix:
        return prefix
    return [m for m in registry if m.path.rsplit("/", 1)[-1] == sel]


# --------------------------------------------------------------------------
# targets
# --------------------------------------------------------------------------

def build_target(url: str):
    """A Target built from a URL without any prompts (CLI use)."""
    from core.methods.threat import Target
    raw = url.strip()
    if "://" not in raw:
        raw = "http://" + raw
    scheme, rest = raw.split("://", 1)
    authority = rest.split("/", 1)[0]
    host = authority.split(":")[0]
    port = 443 if scheme == "https" else 80
    if ":" in authority:
        try:
            port = int(authority.split(":")[1])
        except ValueError:
            pass
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        kit.warn(f"Could not resolve {host}; continuing with the hostname.")
        ip = host
    t = Target(host, ip)
    t.port = port
    t.urluser = ""
    t.urlpasswd = ""
    full = f"{scheme}://{host}"
    if port not in (80, 443):
        full += f":{port}"
    t.fullurl = full
    return t


def apply_options(mod, sets: dict) -> None:
    """Set module options copy-on-write (shared option dicts must not leak)."""
    props = getattr(mod, "properties", {})
    for key, val in sets.items():
        if key in props:
            props[key] = [props[key][0], val]


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------

def cmd_list(category: str | None) -> int:
    registry = discover()
    if category:
        registry = resolve(category, registry)
        if not registry:
            kit.bad(f"No modules under '{category}'. Try: tidos --list")
            return 1
    groups: dict[str, list[Mod]] = {}
    for m in registry:
        groups.setdefault(m.path.split("/")[0], []).append(m)
    order = [p for p in PHASE_ORDER if p in groups] + [p for p in groups if p not in PHASE_ORDER]
    total = 0
    for phase in order:
        print(f"\n  {phase}")
        for m in sorted(groups[phase], key=lambda x: x.path):
            total += 1
            print(f"    {m.path:<42} {m.info}")
    print(f"\n  {total} module(s). Address one with -m <path>, a group with -m <phase>[/<sub>] or -m <phase>/all.")
    return 0


def cmd_info(path: str) -> int:
    registry = discover()
    found = resolve(path, registry)
    if not found:
        kit.bad(f"No modules match '{path}'. Try: tidos --list")
        return 1
    for m in found:
        mod = importlib.import_module(m.dotted)
        print(f"\n  {m.path}  --  {m.info}")
        doc = (getattr(mod, "info", "") or "").strip()
        if doc:
            print("  " + doc)
        props = getattr(mod, "properties", {})
        if props:
            print("  options:")
            width = max(len(k) for k in props)
            for k, meta in props.items():
                desc = meta[0] if isinstance(meta, (list, tuple)) and meta else ""
                print(f"    {k.ljust(width)}  {desc}")
    return 0


def cmd_run(urls: list[str], selectors: list[str], sets: dict,
            use_tor: bool, processes: int | None) -> int:
    registry = discover()
    chosen: list[Mod] = []
    for sel in selectors:
        matches = resolve(sel, registry)
        if not matches:
            kit.bad(f"No modules match '{sel}'. Try: tidos --list")
            return 1
        for m in matches:
            if m not in chosen:
                chosen.append(m)

    if processes:
        variables.processes = max(1, processes)
    if use_tor:
        from core.methods import tor
        if not tor.torpipe(True):
            return 1

    targets = [build_target(u) for u in urls]
    for t in targets:
        kit.info(f"Target {t.fullurl} -- {len(chosen)} module(s)")
        for m in chosen:
            try:
                mod = importlib.import_module(m.dotted)
            except Exception as e:  # noqa: BLE001
                kit.bad(f"{m.path}: import failed ({type(e).__name__}: {e})")
                continue
            apply_options(mod, sets)
            print()
            kit.info(f">> {m.path}")
            try:
                mod.attack(t)
            except KeyboardInterrupt:
                kit.warn(f"{m.path} interrupted; moving on (Ctrl+C again to abort).")
            except SystemExit:
                pass
            except Exception as e:  # noqa: BLE001
                kit.bad(f"{m.path} failed on {t.fullurl}: {type(e).__name__}: {e}")
    kit.good("Done.")
    return 0


# --------------------------------------------------------------------------
# argument parsing
# --------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="tidos",
        description="TIDoS -- offensive web application pentest framework (CLI). "
                    "Run with no arguments for the interactive console.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="examples:\n"
               "  tidos --list\n"
               "  tidos --list osint\n"
               "  tidos -u http://host -m osint/passiverecon/getgeoip\n"
               "  tidos -u http://host -m osint/passiverecon\n"
               "  tidos -u http://host -m osint/all --tor\n"
               "  tidos -u http://host -m sqli --set PARAM=/p.php?id=1 --set COOKIE=sid=abc\n"
               "  tidos --info osint/passiverecon/getgeoip\n",
    )
    p.add_argument("-u", "--url", action="append", metavar="URL", default=[],
                   help="target URL (repeatable; comma-separated values accepted)")
    p.add_argument("-m", "--module", action="append", metavar="PATH", default=[],
                   help="module path to run: all | <phase> | <phase>/<sub> | <phase>/<sub>/<module> "
                        "| <phase>/all | <module> (repeatable)")
    p.add_argument("--set", action="append", metavar="OPT=VALUE", default=[],
                   help="set a module option (repeatable), e.g. --set PARAM=/p.php?id=1")
    p.add_argument("--list", nargs="?", const="", metavar="CATEGORY",
                   help="list modules (optionally only a phase/sub-phase) and exit")
    p.add_argument("--info", metavar="PATH", help="show a module's description and options, then exit")
    p.add_argument("--tor", action="store_true", help="route HTTP through Tor (verified first)")
    p.add_argument("--processes", type=int, metavar="N", help="worker processes for parallel modules")
    p.add_argument("-q", "--quiet", action="store_true", help="do not print the banner")
    return p


def _split_commas(values: list[str]) -> list[str]:
    out: list[str] = []
    for v in values:
        out.extend(part.strip() for part in v.split(",") if part.strip())
    return out


def _parse_sets(pairs: list[str]) -> dict:
    sets: dict = {}
    for item in pairs:
        if "=" not in item:
            kit.warn(f"Ignoring --set '{item}' (expected OPT=VALUE).")
            continue
        key, val = item.split("=", 1)
        sets[key.strip()] = val
    return sets


def main(argv: list[str]) -> int:
    """Entry point for non-interactive use. Returns a process exit code."""
    from core.methods import print as prnt
    args = build_parser().parse_args(argv)

    if not args.quiet:
        prnt.banner()

    if args.list is not None:
        return cmd_list(args.list or None)
    if args.info:
        return cmd_info(args.info)

    urls = _split_commas(args.url)
    selectors = _split_commas(args.module)
    if not selectors:
        kit.bad("Nothing to do: pass -m/--module (and -u/--url), or --list. See tidos -h.")
        return 2
    if not urls:
        kit.bad("No target: pass at least one -u/--url.")
        return 2
    if os.name != "nt" and hasattr(os, "geteuid") and os.geteuid() != 0:
        kit.warn("Not running as root; raw-socket modules (port scans, ARP, traceroute) may fail.")
    return cmd_run(urls, selectors, _parse_sets(args.set), args.tor, args.processes)
