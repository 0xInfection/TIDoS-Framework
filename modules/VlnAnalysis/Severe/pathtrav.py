#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Path traversal scanning with the external Vailyn tool."""

from __future__ import annotations

import os
import re

import core.variables as variables
from core.methods import modkit as kit
from core.methods.print import pvln

info = ("Path traversal scanning with Vailyn (https://github.com/VainlyStrain/Vailyn, an optional "
        "external tool; see docs/install.md). Supports query, path, cookie, POST (plain/JSON) and "
        "crawl-all attack vectors, cookies, a target file and depth. Vailyn's install directory is read "
        "from core/doc/vailyn. For a built-in scanner without external tools use pathtrav_legacy "
        "(URL path) or lfi (parameters).")
searchinfo = "Advanced Path Traversal Scanning"
properties = {
    "DIRECTORY": ["Sensitive directory appended to the target, e.g. /sensitive (empty: none)", ""],
    "ATTACK": ["Attack vector: 1 query, 2 path, 3 cookie, 4 POST plain, 5 POST JSON, A crawl-all (default A)", ""],
    "COOKIE": ["Authentication cookie in Cookie-header format, without 'Cookie:' (empty: none)", ""],
    "PARAM": ["Query parameter for ATTACK 1", ""],
    "POST": ["POST data for ATTACK 4/5 (mark the injection point with INJECT)", ""],
    "FILE": ["File to look for (default /etc/passwd)", ""],
    "DEPTH": ["Traversal depth (default 8)", ""],
    "TIMEOUT": ["Request timeout in seconds passed to Vailyn (empty: Vailyn's default)", ""],
    "PRECISE": ["Use exactly DEPTH instead of 1..DEPTH (y/n, default n)", ""],
    "MAXTIME": ["Seconds before Vailyn is stopped (default 3600)", ""],
}

VECTORS = ("1", "2", "3", "4", "5", "A")
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


def executable() -> str:
    """Path of the Vailyn script, '' (after saying why) when not installed."""
    vdir = (variables.vailyndir or "").strip()
    if not vdir:
        kit.bad("Vailyn's install directory is not set (core/doc/vailyn); see docs/install.md, "
                "or use pathtrav_legacy / lfi instead.")
        return ""
    path = os.path.join(os.path.abspath(os.path.expanduser(vdir)), "Vailyn")
    if not os.path.isfile(path):
        kit.bad(f"Vailyn not found at {path}; fix core/doc/vailyn or use pathtrav_legacy / lfi instead.")
        return ""
    return path


def build(web, script: str) -> list[str] | None:
    """Vailyn argv from the module options, None when an option is invalid."""
    victim = kit.url(web)
    directory = kit.option(properties, "DIRECTORY", "Directory to attack, e.g. /sensitive (enter for none)", "")
    if directory:
        victim += "/" + directory.strip().lstrip("/")

    attack = kit.option(properties, "ATTACK", "Attack vector (1 query, 2 path, 3 cookie, 4 POST, 5 JSON, A all)",
                        "A").strip().upper()
    if attack not in VECTORS:
        kit.bad(f"Invalid ATTACK '{attack}': use one of {', '.join(VECTORS)}.")
        return None
    argv = [script, "--victim", victim, "--attack", attack]

    cookie = kit.option(properties, "COOKIE", "Authentication cookie (enter for none)", "")
    if cookie:
        argv += ["--cookie", cookie]
    if attack == "1":
        param = kit.option(properties, "PARAM", "Query parameter to attack", "")
        if not param:
            kit.bad("ATTACK 1 needs PARAM (the query parameter).")
            return None
        argv += ["--param", param]
    elif attack in ("4", "5"):
        post = kit.option(properties, "POST", "POST data (mark the injection point with INJECT)", "")
        if "INJECT" not in post:
            kit.bad("ATTACK 4/5 needs POST data with an INJECT marker.")
            return None
        argv += ["--param", post]

    argv += ["--check", kit.option(properties, "FILE", "File to look for", "/etc/passwd") or "/etc/passwd"]
    depth = max(1, kit.integer(properties, "DEPTH", "Traversal depth", 8))
    argv += ["--depths", str(depth), "1", "1", "--nosploit", "--notmain"]
    if kit.flag(properties, "PRECISE", "Use exactly DEPTH", False):
        argv.append("--precise")
    timeout = kit.option(properties, "TIMEOUT", "Request timeout in seconds (enter for default)", "")
    if timeout:
        try:
            float(timeout)
            argv += ["--timeout", timeout.strip()]
        except ValueError:
            kit.warn(f"Invalid TIMEOUT '{timeout}', using Vailyn's default.")
    if variables.tor:
        argv.append("--tor")
    if kit.is_root() and (variables.username or "").strip():
        argv = ["sudo", "-u", variables.username.strip(), *argv]  # drop root, as before
    return argv


def pathtrav(web):
    pvln("path traversal")
    script = executable()
    if not script:
        return None
    argv = build(web, script)
    if argv is None:
        return None
    maxtime = max(30, kit.integer(properties, "MAXTIME", "Seconds before Vailyn is stopped", 3600))
    kit.info("Running Vailyn; output is shown when it finishes.")
    proc = kit.run_tool(argv, timeout=maxtime, cwd=os.path.dirname(script))
    if proc is None:
        kit.warn("Raise MAXTIME or lower DEPTH if Vailyn timed out.")
        return None
    out = ANSI.sub("", proc.stdout or "").strip()
    if out:
        print(out)
    if proc.returncode != 0:
        err = ANSI.sub("", proc.stderr or "").strip().splitlines()
        kit.bad(f"Vailyn exited with status {proc.returncode}: {err[-1] if err else 'no error output'}")
        kit.warn("Try upgrading Vailyn; report persistent errors at https://github.com/VainlyStrain/Vailyn")
    rec = kit.Recorder(web, kit.CRITICAL, "pathtrav")
    rec("\n".join(out.splitlines()[-300:]) if out else "Vailyn finished without output.")
    return proc


def attack(web):
    pathtrav(web)
