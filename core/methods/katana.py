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
Katana (github.com/projectdiscovery/katana) as TIDoS's crawling engine.

Katana is not bundled. The first time something needs to crawl, a pinned
release for this OS/CPU is downloaded from GitHub, checked against the
SHA-256 pinned below and unpacked into tools/bin/ (or ~/.cache/tidos/bin
when the checkout is read-only). Later runs reuse it.

    for item in katana.crawl("https://target/", depth=2, max_pages=200):
        item["request"]["endpoint"], item.get("response", {}).get("status_code")

Environment:
    TIDOS_KATANA=/path/to/katana   use this binary (no version check, no download)
    TIDOS_NO_DOWNLOAD=1            never download; fail with install instructions
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import zipfile
from typing import Iterator

import core.variables as variables
from core.methods import modkit as kit

VERSION = "1.8.0"
RELEASE = ("https://github.com/projectdiscovery/katana/releases/download/"
           "v{version}/katana_{version}_{os}_{arch}.zip")
# from katana-1.8.0-checksums.txt of the GitHub release
SHA256 = {
    ("linux", "amd64"): "cb027ae99d0757061b70c07a15c7a80f62c5a535ab52c4a329f80c4b0a7309d2",
    ("linux", "arm64"): "80e269210727a855511ffac8dfb01297b2344742acec71a35e8ba4a67a90f0f2",
    ("linux", "386"): "342adc440481a0b562121857d80bc5c8fbc8d1d21a57ddf593e6ba884078c8f6",
    ("macOS", "amd64"): "806256316dd45e0fe0e3985fd7283ddffc376c95cbaa3dcfd14cde6e1de61aaf",
    ("macOS", "arm64"): "52e9802e9f83012a089fe57fb1ac476b936f181ac033c71bfa55f913c07cede6",
}
ARCH = {"x86_64": "amd64", "amd64": "amd64", "aarch64": "arm64", "arm64": "arm64",
        "i386": "386", "i686": "386", "x86": "386"}
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INSTALL_DIRS = (os.path.join(ROOT, "tools", "bin"),
                os.path.join(os.path.expanduser("~"), ".cache", "tidos", "bin"))
TOR_PROXY = "socks5://127.0.0.1:9050"
MAX_BODY = 5 * 1024 * 1024

_lock = threading.Lock()
_binary: str | None = None


class KatanaError(Exception):
    """Katana is unavailable or failed to run; the message says what to do."""


# --------------------------------------------------------------------------
# locating / installing
# --------------------------------------------------------------------------

def platform_tag() -> tuple[str, str]:
    system = {"linux": "linux", "darwin": "macOS"}.get(sys.platform)
    arch = ARCH.get(platform.machine().lower())
    if not system or not arch or (system, arch) not in SHA256:
        raise KatanaError(f"No Katana build is pinned for {sys.platform}/{platform.machine()}. "
                          "Install it yourself (go install github.com/projectdiscovery/katana/cmd/katana@latest) "
                          "and set TIDOS_KATANA=/path/to/katana.")
    return system, arch


def version(path: str) -> str:
    """'1.8.0' as reported by `katana -version`, '' if it does not run."""
    try:
        out = subprocess.run([path, "-version"], capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return ""
    m = re.search(r"version:?\s*v?(\d+\.\d+\.\d+)", out.stdout + out.stderr, re.I)
    return m.group(1) if m else ""


def _manual_hint() -> str:
    try:
        system, arch = platform_tag()
        url = RELEASE.format(version=VERSION, os=system, arch=arch)
    except KatanaError:
        url = f"https://github.com/projectdiscovery/katana/releases/tag/v{VERSION}"
    return (f"Download {url}, unzip it and put `katana` in {INSTALL_DIRS[0]} "
            "(or set TIDOS_KATANA=/path/to/katana).")


def find() -> str | None:
    """A usable katana: $TIDOS_KATANA, a managed copy, or one on PATH of the pinned version."""
    override = os.environ.get("TIDOS_KATANA", "").strip()
    if override:
        if os.path.isfile(override) and os.access(override, os.X_OK):
            return override
        raise KatanaError(f"TIDOS_KATANA={override} is not an executable file.")
    candidates = [os.path.join(d, "katana") for d in INSTALL_DIRS]
    on_path = shutil.which("katana")
    if on_path:
        candidates.append(on_path)
    for path in candidates:
        if os.path.isfile(path) and os.access(path, os.X_OK) and version(path) == VERSION:
            return path
    return None


def _fetch() -> bytes:
    """The pinned katana binary for this platform, checksum-verified."""
    system, arch = platform_tag()
    url = RELEASE.format(version=VERSION, os=system, arch=arch)
    kit.info(f"Katana (the crawling engine) is not installed; downloading v{VERSION} for {system}/{arch}...")
    try:
        resp = kit.http(timeout=120).get(url, stream=True)
        if resp.status_code != 200:
            raise KatanaError(f"Download failed: HTTP {resp.status_code} for {url}. {_manual_hint()}")
        blob = io.BytesIO()
        for chunk in resp.iter_content(1 << 20):
            blob.write(chunk)
    except KatanaError:
        raise
    except Exception as e:  # connection errors, timeouts, Tor failures
        raise KatanaError(f"Could not download Katana ({type(e).__name__}: {e}). {_manual_hint()}") from None
    digest = hashlib.sha256(blob.getvalue()).hexdigest()
    if digest != SHA256[(system, arch)]:
        raise KatanaError(f"Checksum mismatch for {url} (got {digest}); refusing to install it.")
    try:
        with zipfile.ZipFile(blob) as zf:
            return zf.read("katana")
    except (KeyError, zipfile.BadZipFile):
        raise KatanaError(f"{url} does not contain a katana binary. {_manual_hint()}") from None


def _install(data: bytes, dest_dir: str) -> str:
    """Write the binary atomically into dest_dir (OSError if not writable)."""
    os.makedirs(dest_dir, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=dest_dir, prefix=".katana-")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        os.chmod(tmp, 0o755)
        path = os.path.join(dest_dir, "katana")
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    kit.good(f"Katana v{VERSION} installed at {path}")
    return path


def ensure() -> str:
    """Path to a working katana, downloading it on first use."""
    global _binary
    with _lock:
        if _binary and os.path.isfile(_binary):
            return _binary
        path = find()
        if not path:
            if os.environ.get("TIDOS_NO_DOWNLOAD", "").strip() not in ("", "0"):
                raise KatanaError(f"Katana is required for crawling and TIDOS_NO_DOWNLOAD is set. {_manual_hint()}")
            data, errors = _fetch(), []
            for dest in INSTALL_DIRS:
                try:
                    path = _install(data, dest)
                    break
                except OSError as e:  # read-only checkout (e.g. /opt as a normal user): next location
                    errors.append(f"{dest}: {e.strerror or e}")
            if not path:
                raise KatanaError("Cannot write Katana anywhere (" + "; ".join(errors) + "). " + _manual_hint())
        _binary = path
        return path


# --------------------------------------------------------------------------
# crawling
# --------------------------------------------------------------------------

def command(binary: str, url: str, *, depth: int, max_pages: int, headers: dict[str, str] | None,
            out_scope: list[str], timeout: int, duration: int, js: bool) -> list[str]:
    args = [binary, "-u", url, "-d", str(max(1, depth)),
            "-jsonl", "-silent", "-nc", "-duc",
            "-or",              # no raw request/response dumps (bodies are kept: -ob also disables -jc)
            "-duf",             # keep same-content URLs: /api/users and /api/users?id=2 are both wanted
            "-fx",              # forms with their fields
            "-fs", "fqdn", "-do",
            "-mdp", str(max_pages),
            "-mrs", str(MAX_BODY),
            "-timeout", str(timeout),
            "-ct", f"{duration}s",
            "-c", str(max(1, min(variables.processes, 16))), "-p", "1"]
    if js:
        args.append("-jc")
    if depth >= 3:
        args += ["-kf", "robotstxt,sitemapxml"]
    for regex in out_scope:
        args += ["-cos", regex]
    for name, value in (headers or {}).items():
        args += ["-H", f"{name}: {value}"]
    if variables.tor:
        args += ["-proxy", TOR_PROXY]
    return args


def crawl(url: str, *, depth: int, max_pages: int = 200, headers: dict[str, str] | None = None,
          out_scope: list[str] | None = None, timeout: int = 6, duration: int = 600,
          js: bool = True) -> Iterator[dict]:
    """Stream Katana's JSONL results for `url` (one dict per discovered URL).

    Raises KatanaError when Katana is unavailable or exits with an error
    before producing anything. Stops Katana once the generator is closed.
    """
    binary = ensure()
    args = command(binary, url, depth=depth, max_pages=max_pages, headers=headers,
                   out_scope=out_scope or [], timeout=timeout, duration=duration, js=js)
    with tempfile.TemporaryFile(mode="w+") as errlog:
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=errlog, text=True,
                                encoding="utf-8", errors="replace", bufsize=1)
        killer = threading.Timer(duration + 60, proc.kill)  # -ct is the soft limit, this the hard one
        killer.daemon = True
        killer.start()
        produced = False
        try:
            for line in proc.stdout:
                line = line.strip()
                if not line.startswith("{"):
                    continue
                try:
                    item = json.loads(line)
                except ValueError:
                    continue
                produced = True
                yield item
            proc.wait()
        finally:
            killer.cancel()
            if proc.poll() is None:
                proc.kill()
                proc.wait()
            proc.stdout.close()
        if proc.returncode and not produced:
            errlog.seek(0)
            lines = [l.strip() for l in errlog.read().splitlines() if l.strip()]
            reason = lines[-1] if lines else f"exit status {proc.returncode}"
            raise KatanaError(f"Katana failed: {reason}")
