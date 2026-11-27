#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Test suite for the TIDoS modules, driven against the local vulnerable site.

    python3 tests/run.py                # deep detection tests + contract smoke
    python3 tests/run.py --run-smoke    # also execute every other module once
    python3 tests/run.py -k sqli        # only cases/modules matching a substring

Deep tests point a module at a crafted endpoint and assert it reports the bug
(and, for a safe twin, that it stays quiet). The contract smoke imports every
module and checks it exposes info/searchinfo/properties/attack. --run-smoke
additionally runs each remaining module once against the site, failing only on
an unhandled exception (external-OSINT modules simply error out without a key).
"""
from __future__ import annotations

import argparse
import importlib
import io
import os
import re
import sys
import tempfile
import threading
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass, field

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# Route result storage to a throwaway DB before anything imports it.
_DBFD, _DBPATH = tempfile.mkstemp(prefix="tidos-test-", suffix=".db")
os.close(_DBFD)
import core.variables as variables  # noqa: E402
variables.database = _DBPATH
from core.methods import modkit as kit  # noqa: E402
kit.database = _DBPATH
from core.methods.threat import Target  # noqa: E402
from tests.vulnsite import VulnSite  # noqa: E402

GREEN, RED, YELLOW, DIM, RST = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"


def target(url: str) -> Target:
    host = re.sub(r"^https?://", "", url).split("/")[0].split(":")[0]
    t = Target(host, host)
    t.fullurl = url
    return t


def run_module(dotted: str, tgt: Target, opts: dict) -> str:
    """Run a module once with `opts` applied; return its captured output.
    Options are set copy-on-write so shared option dicts never leak."""
    mod = importlib.import_module(dotted)
    saved = dict(mod.properties)
    for key, value in opts.items():
        desc = mod.properties[key][0] if key in mod.properties else ""
        mod.properties[key] = [desc, value]
    buf = io.StringIO()
    try:
        with redirect_stdout(buf), redirect_stderr(buf):
            mod.attack(tgt)
    finally:
        mod.properties.clear()
        mod.properties.update(saved)
    return buf.getvalue()


# --------------------------------------------------------------------------
# deep detection cases
# --------------------------------------------------------------------------

@dataclass
class Case:
    name: str
    module: str
    server: str             # vulnsite server key, or "https"
    path: str               # endpoint, becomes PARAM or the target URL
    expect: list = field(default_factory=list)   # substrings that MUST appear
    forbid: list = field(default_factory=list)   # substrings that must NOT
    opts: dict = field(default_factory=dict)
    param: bool = True       # path goes in PARAM (injection) vs the target URL


V = "VlnAnalysis.Severe."
M = "VlnAnalysis.Misconfig."
I = "OSINTFootprinting.InfoDisclose."
A = "OSINTFootprinting.ActiveRecon."


def mod(short: str) -> str:
    return "modules." + short


CASES = [
    # ---- injection (PARAM-driven) ----
    Case("sqli/error", mod(V + "sqli"), "sqli", "/sql/err?id=1",
         expect=["finding"], opts={"TECHNIQUE": "error,boolean"}),
    Case("sqli/safe", mod(V + "sqli"), "sqli", "/sql/safe?id=1",
         expect=["No "], forbid=["finding"], opts={"TECHNIQUE": "error,boolean"}),
    Case("xss/reflected", mod(V + "xss"), "sqli", "/x/html?q=hello", expect=["finding"]),
    Case("xss/encoded-safe", mod(V + "xss"), "sqli", "/x/enc?q=hello",
         expect=["No "], forbid=["finding"]),
    Case("lfi", mod(V + "lfi"), "fileinj", "/lfi/read?file=about.php", expect=["finding"]),
    Case("lfi/safe", mod(V + "lfi"), "fileinj", "/lfi/whitelist?file=about.php",
         expect=["No "], forbid=["finding"]),
    Case("rfi", mod(V + "rfi"), "fileinj", "/rfi/inc?file=home", expect=["finding"],
         opts={"RFIMARK": "TIDREMOTE-q8z3"}),  # RFIURL filled in at runtime
    Case("pathtrav", mod(V + "pathtrav"), "fileinj", "/lfi/read?file=about.php", expect=["confirmed"]),
    Case("phpi", mod(V + "phpi"), "fileinj", "/phpi/eval?code=1", expect=["finding"]),
    Case("rce", mod(V + "rce"), "fileinj", "/rce/ping?host=127.0.0.1", expect=["finding"]),
    Case("htmli", mod(V + "htmli"), "webinj", "/htmli/vuln?q=a", expect=["finding"]),
    Case("crlf", mod(V + "crlf"), "webinj", "/crlf/vuln?r=x", expect=["finding"]),
    Case("openredirect", mod(V + "openredirect"), "webinj", "/redir/vuln?next=x", expect=["finding"]),
    Case("ldap", mod(V + "ldap"), "webinj", "/ldap/vuln?user=a", expect=["finding"]),
    Case("xpathi", mod(V + "xpathi"), "webinj", "/xpath/vuln?name=a", expect=["finding"]),

    # ---- misconfiguration (target-URL driven) ----
    Case("clickjack", mod(M + "clickjack"), "misconf", "/cj/none", expect=["Clickjackable"], param=False),
    Case("clickjack/safe", mod(M + "clickjack"), "misconf", "/cj/deny",
         expect=["Not clickjackable"], param=False),
    Case("headers", mod(M + "headers"), "misconf", "/hdr/bad", expect=["missing"], param=False),
    Case("cookiecheck", mod(M + "cookiecheck"), "misconf", "/ck/bad", expect=["Secure"], param=False),
    Case("icors", mod(M + "icors"), "misconf", "/cors/reflectcreds",
         expect=["CORS misconfiguration"], param=False),
    Case("hhi", mod(M + "hhi"), "misconf", "/hhi/redirect", expect=["Host header injection"], param=False),
    Case("sessionfix", mod(M + "sessionfix"), "misconf", "/sf/url", expect=["Session fixation"], param=False),

    # ---- information disclosure (target-URL driven, CRAWL off) ----
    Case("emailext", mod(I + "emailext"), "recon", "/leak/emails",
         expect=["corp-internal.net"], opts={"CRAWL": "n"}, param=False),
    Case("creditcards", mod(I + "creditcards"), "recon", "/leak/cards",
         expect=["4111"], opts={"CRAWL": "n"}, param=False),
    Case("ssn", mod(I + "ssn"), "recon", "/leak/ssn",
         expect=["123-45-6789"], opts={"CRAWL": "n"}, param=False),
    Case("phone", mod(I + "phone"), "recon", "/leak/phone",
         expect=["202-555-0143"], opts={"CRAWL": "n"}, param=False),
    Case("internalip", mod(I + "internalip"), "recon", "/leak/internalip",
         expect=["10.10.14.22"], opts={"CRAWL": "n"}, param=False),
    Case("secrets", mod(I + "secrets"), "recon", "/leak/secrets",
         expect=["AKIA"], opts={"CRAWL": "n"}, param=False),
    Case("errors", mod(I + "errors"), "recon", "/leak/error",
         expect=["PHP"], opts={"CRAWL": "n"}, param=False),
    Case("secrets/clean", mod(I + "secrets"), "recon", "/clean",
         expect=["No "], forbid=["AKIA"], opts={"CRAWL": "n"}, param=False),

    # ---- active recon ----
    Case("commentssrc", mod(A + "commentssrc"), "recon", "/comments", expect=["admin"], param=False),

    # ---- exploitation ----
    Case("shellshock", "modules.SploitLoot.shellshocksploit", "fileinj", "",
         expect=["Shellshock confirmed"], opts={"PATH": "/cgi-bin/vuln.cgi"}, param=False),
]

HTTPS_CASES = [
    Case("hsts", mod(M + "hsts"), "https", "/hsts/none", expect=["missing"], param=False),
]


def check(out: str, case: Case) -> tuple[bool, str]:
    low = out.lower()
    for want in case.expect:
        if want.lower() not in low:
            return False, f"expected {want!r}"
    for bad in case.forbid:
        if bad.lower() in low:
            return False, f"forbidden {bad!r}"
    return True, ""


def run_cases(site: VulnSite, cases: list, needle: str) -> tuple[int, int]:
    passed = failed = 0
    for case in cases:
        if needle and needle not in case.name and needle not in case.module:
            continue
        base = site.https_url if case.server == "https" else site.url(case.server)
        opts = dict(case.opts)
        if case.module.endswith(".rfi"):
            opts["RFIURL"] = site.url("fileinj") + "/rfi/remote.txt"
        if case.param:
            opts["PARAM"] = case.path
            tgt = target(base)
        else:
            tgt = target(base + case.path)
        try:
            out = run_module(case.module, tgt, opts)
            ok, why = check(out, case)
        except Exception as e:  # noqa: BLE001
            ok, why, out = False, f"{type(e).__name__}: {e}", ""
        if ok:
            passed += 1
            print(f"  {GREEN}PASS{RST} {case.name}")
        else:
            failed += 1
            print(f"  {RED}FAIL{RST} {case.name}  ({why})")
            snippet = " | ".join(l.strip() for l in out.splitlines() if l.strip())[:300]
            if snippet:
                print(f"       {DIM}{snippet}{RST}")
    return passed, failed


# --------------------------------------------------------------------------
# contract smoke: every module imports and exposes the contract
# --------------------------------------------------------------------------

def iter_modules():
    skip = os.sep + "files" + os.sep  # data/helper dirs, not modules
    for dp, dn, fns in os.walk(os.path.join(ROOT, "modules")):
        if "__pycache__" in dp or skip in dp + os.sep:
            continue
        for fn in sorted(fns):
            if fn.endswith(".py") and fn != "__init__.py" and "-" not in fn:
                rel = os.path.relpath(os.path.join(dp, fn), ROOT)
                yield rel[:-3].replace(os.sep, ".")


def contract_smoke(needle: str) -> tuple[int, int, int]:
    passed = failed = helpers = 0
    for dotted in iter_modules():
        if needle and needle not in dotted:
            continue
        try:
            m = importlib.import_module(dotted)
            # files placed in module dirs without the module contract are helpers
            # (e.g. DNSDumpsterAPI, a helper of dnsdump); not listed by discovery.
            if not any(hasattr(m, a) for a in ("searchinfo", "attack")):
                helpers += 1
                continue
            for attr in ("info", "searchinfo", "properties", "attack"):
                assert hasattr(m, attr), f"missing {attr}"
            assert callable(m.attack)
            passed += 1
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  {RED}FAIL{RST} {dotted}  ({type(e).__name__}: {e})")
    return passed, failed, helpers


# --------------------------------------------------------------------------
# optional run smoke: execute every other module once against the site
# --------------------------------------------------------------------------

def run_smoke(site: VulnSite, needle: str, covered: set) -> tuple[int, int, int]:
    ok = errored = skipped = 0
    tgt = target(site.url("recon"))
    for dotted in iter_modules():
        if dotted in covered or (needle and needle not in dotted):
            continue
        try:
            m = importlib.import_module(dotted)
        except Exception:  # noqa: BLE001  (import failures are a contract-smoke concern)
            continue
        if not any(hasattr(m, a) for a in ("searchinfo", "attack")):
            continue  # helper, not a module
        result = {}

        def work():
            try:
                run_module(dotted, tgt, {})
                result["ok"] = True
            except Exception as e:  # noqa: BLE001
                result["err"] = f"{type(e).__name__}: {e}"

        th = threading.Thread(target=work, daemon=True)
        th.start()
        th.join(15)
        if th.is_alive():
            skipped += 1
            print(f"  {YELLOW}SKIP{RST} {dotted}  (timed out)")
        elif "err" in result:
            errored += 1
            print(f"  {RED}ERR {RST} {dotted}  ({result['err']})")
        else:
            ok += 1
    return ok, errored, skipped


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-smoke", action="store_true", help="also execute every other module once")
    ap.add_argument("-k", dest="needle", default="", help="only cases/modules matching this substring")
    args = ap.parse_args()

    print(f"{DIM}Starting the vulnerable site...{RST}")
    with VulnSite() as site:
        print(f"\n{DIM}== deep detection cases =={RST}")
        p1, f1 = run_cases(site, CASES, args.needle)
        if site.https_available:
            ph, fh = run_cases(site, HTTPS_CASES, args.needle)
            p1 += ph
            f1 += fh
        elif not args.needle:
            print(f"  {YELLOW}SKIP{RST} hsts (no openssl / HTTPS unavailable)")

        print(f"\n{DIM}== contract smoke (all modules import + expose the contract) =={RST}")
        p2, f2, helpers = contract_smoke(args.needle)
        print(f"  {p2} modules OK, {f2} failed, {helpers} helpers skipped")

        p3 = e3 = s3 = 0
        if args.run_smoke:
            print(f"\n{DIM}== run smoke (execute every other module once) =={RST}")
            covered = {c.module for c in CASES + HTTPS_CASES}
            p3, e3, s3 = run_smoke(site, args.needle, covered)
            print(f"  {p3} ran clean, {e3} raised, {s3} timed out")

    total_fail = f1 + f2 + e3
    print(f"\n{'-' * 56}")
    print(f"deep: {GREEN}{p1} passed{RST}, {RED if f1 else DIM}{f1} failed{RST}  |  "
          f"contract: {p2} ok, {f2} bad" + (f"  |  run-smoke: {p3} ok, {e3} err, {s3} skip" if args.run_smoke else ""))
    os.unlink(_DBPATH)
    return 1 if total_fail else 0


if __name__ == "__main__":
    sys.exit(main())
