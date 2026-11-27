#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""
Concurrent path discovery shared by the *brute recon modules.

Requests every path of a wordlist against the target and reports the ones
that exist. A random, certainly-missing path is requested first so servers
answering 200 to everything (soft 404s) don't flood the results.
"""

from __future__ import annotations

import sys
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

import core.variables as variables
from core.lib.FileUtils import FileUtils
from core.methods import modkit as kit

CLEAR_LINE = "\r\033[K"
HIT_CODES = {200, 204, 301, 302, 307, 308, 401, 403}


@dataclass(frozen=True)
class Hit:
    url: str
    status: int
    size: int

    def __str__(self) -> str:
        return f"{self.url} ({self.status}, {FileUtils.sizeHuman(self.size)})"


def _probe(session, url: str) -> tuple[int, int] | None:
    try:
        r = session.get(url, allow_redirects=False)
    except Exception:
        return None
    try:
        size = int(r.headers.get("content-length", ""))
    except ValueError:
        size = len(r.content)
    return r.status_code, size


def scan(target, paths: list[str], workers: int | None = None,
         codes: set[int] = HIT_CODES, quiet: bool = False) -> list[Hit]:
    """Return the paths that exist on `target`, sorted by URL.

    `quiet` suppresses the per-hit lines, for callers that confirm hits
    themselves before reporting them.
    """
    base = kit.url(target)
    session = kit.http(timeout=7)
    workers = max(1, min(workers or variables.processes, 32))

    baseline = _probe(session, f"{base}/{uuid.uuid4().hex}")

    def is_hit(status: int, size: int) -> bool:
        if status not in codes:
            return False
        if baseline and status == baseline[0] and size == baseline[1]:
            return False  # looks exactly like a 404 page
        return True

    hits: list[Hit] = []
    urls = [f"{base}/{p.lstrip('/')}" for p in paths]
    progress = sys.stdout.isatty()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_probe, session, u): u for u in urls}
        for done, fut in enumerate(as_completed(futures), 1):
            res = fut.result()
            if res and is_hit(*res):
                hit = Hit(futures[fut], *res)
                hits.append(hit)
                if not quiet:
                    if progress:
                        print(CLEAR_LINE, end="")
                    kit.found(f"Found ({hit.status})", f"{hit.url}  {FileUtils.sizeHuman(hit.size)}")
            if progress:
                print(f"{CLEAR_LINE} [*] {done}/{len(urls)} paths checked", end="", flush=True)
    if progress:
        print(CLEAR_LINE, end="")
    return sorted(hits, key=lambda h: h.url)


def run(target, properties: dict, *, noun: str, wordlist: str, lvl3: str,
        lvl2: str = "filebrute") -> list[Hit]:
    """Full module flow: resolve wordlist option, scan, print, record."""
    path = kit.option(properties, "WORDLIST", f"Wordlist for {noun}", wordlist)
    paths = kit.wordlist(path)
    if not paths:
        return []

    kit.info(f"Hunting {noun} on {kit.url(target)} ({len(paths)} paths)")
    hits = scan(target, paths)
    record = kit.Recorder(target, kit.ACTIVE, lvl2, lvl3)
    if hits:
        kit.good(f"{len(hits)} possible {noun} found")
        record([str(h) for h in hits])
    else:
        kit.bad(f"No {noun} found.")
        record(f"No {noun} found.")
    return hits
