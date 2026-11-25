#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTTP security header analysis shared by the misconfiguration modules
(headers, hsts, clickjack, cookiecheck).

Everything here is pure: functions take header values / responses and
return Issue lists, so the modules only fetch, print and record.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from urllib.parse import urlsplit

from core.methods import modkit as kit

HIGH, MEDIUM, LOW, INFO = "HIGH", "MEDIUM", "LOW", "INFO"
SEVERITIES = (HIGH, MEDIUM, LOW, INFO)

HSTS_MIN = 15768000        # 6 months: below this HSTS gives little protection
HSTS_PRELOAD = 31536000    # 1 year: required for the preload list


@dataclass
class Issue:
    severity: str
    header: str
    message: str

    def __str__(self) -> str:
        return f"[{self.severity}] {self.header}: {self.message}"


# --------------------------------------------------------------------------
# fetching helpers
# --------------------------------------------------------------------------

def raw_values(resp, name: str) -> list[str]:
    """Every value of a (possibly repeated) header, unmerged.

    requests folds repeated headers into one comma-joined string, which
    breaks Set-Cookie (dates contain commas) and hides duplicates.
    """
    raw = getattr(resp, "raw", None)
    headers = getattr(raw, "headers", None)
    if headers is not None and hasattr(headers, "getlist"):
        return [v for v in headers.getlist(name)]
    value = resp.headers.get(name)
    return [value] if value is not None else []


def is_html(resp) -> bool:
    ctype = resp.headers.get("Content-Type", "").lower()
    return "html" in ctype or (not ctype and "<html" in resp.text[:2000].lower())


# --------------------------------------------------------------------------
# HSTS
# --------------------------------------------------------------------------

def parse_directives(value: str) -> dict[str, str]:
    """`max-age=31536000; includeSubDomains` -> {'max-age': '31536000', 'includesubdomains': ''}."""
    out = {}
    for part in value.split(";"):
        part = part.strip()
        if not part:
            continue
        key, _, val = part.partition("=")
        out.setdefault(key.strip().lower(), val.strip().strip('"'))
    return out


def analyze_hsts(values: list[str], https: bool = True) -> list[Issue]:
    """Issues of the Strict-Transport-Security header(s) of an HTTPS response."""
    h = "Strict-Transport-Security"
    if not https:
        if values:
            return [Issue(INFO, h, "sent over plain HTTP, where browsers ignore it")]
        return []
    if not values:
        return [Issue(MEDIUM, h, "missing: first visits and typed URLs can be SSL-stripped")]
    issues = []
    if len(values) > 1:
        issues.append(Issue(LOW, h, f"sent {len(values)} times; browsers only honour the first"))
    d = parse_directives(values[0])
    age = d.get("max-age")
    if age is None or not age.isdigit():
        return issues + [Issue(MEDIUM, h, f"invalid: no numeric max-age ('{values[0]}'), browsers ignore it")]
    age = int(age)
    if age == 0:
        issues.append(Issue(MEDIUM, h, "max-age=0 disables HSTS (deletes the browser's policy)"))
    elif age < HSTS_MIN:
        issues.append(Issue(LOW, h, f"max-age={age} is short (< 6 months; 1 year recommended)"))
    if age and "includesubdomains" not in d:
        issues.append(Issue(LOW, h, "no includeSubDomains: subdomains (and cookies scoped to them) "
                                    "can still be reached over HTTP"))
    if "preload" in d and (age < HSTS_PRELOAD or "includesubdomains" not in d):
        issues.append(Issue(INFO, h, "'preload' set but not eligible (needs max-age>=31536000 "
                                     "and includeSubDomains)"))
    return issues


# --------------------------------------------------------------------------
# CSP
# --------------------------------------------------------------------------

def parse_csp(value: str) -> list[dict[str, list[str]]]:
    """A CSP header value -> list of policies (comma separates policies)."""
    policies = []
    for policy in value.split(","):
        directives: dict[str, list[str]] = {}
        for part in policy.split(";"):
            tokens = part.strip().split()
            if tokens:
                directives.setdefault(tokens[0].lower(), [t for t in tokens[1:]])
        if directives:
            policies.append(directives)
    return policies


# hosts serving JSONP endpoints / script gadgets usable to bypass a host allowlist
CSP_BYPASS_HOSTS = ("www.google.com", "ajax.googleapis.com", "*.googleapis.com",
                    "cdnjs.cloudflare.com", "cdn.jsdelivr.net", "unpkg.com",
                    "*.googleusercontent.com", "accounts.google.com", "*.google.com",
                    "www.gstatic.com", "*.gstatic.com", "*.cloudfront.net",
                    "*.amazonaws.com", "*.herokuapp.com", "*.firebaseapp.com",
                    "raw.githubusercontent.com", "*.github.io")

_WIDE = {"*", "http:", "https:", "data:", "blob:", "filesystem:", "http://*", "https://*"}


def _effective(directives: dict[str, list[str]], name: str) -> list[str] | None:
    if name in directives:
        return directives[name]
    return directives.get("default-src")


def analyze_csp_policy(d: dict[str, list[str]], header: str) -> list[Issue]:
    issues = []
    script = _effective(d, "script-src")
    if script is None:
        issues.append(Issue(MEDIUM, header, "no script-src/default-src: scripts are not restricted"))
    else:
        low = [s.lower() for s in script]
        nonce_or_hash = any(s.startswith(("'nonce-", "'sha256-", "'sha384-", "'sha512-")) for s in low)
        strict_dynamic = "'strict-dynamic'" in low
        if "'unsafe-inline'" in low and not nonce_or_hash:
            issues.append(Issue(MEDIUM, header, "script-src allows 'unsafe-inline' (inline XSS "
                                                "payloads execute)"))
        if "'unsafe-eval'" in low:
            issues.append(Issue(LOW, header, "script-src allows 'unsafe-eval'"))
        if not strict_dynamic:
            wide = sorted({s for s in low if s in _WIDE})
            if wide:
                issues.append(Issue(MEDIUM, header, "script-src allows any source: " + " ".join(wide)))
            gadgets = sorted({s for s in low
                              if re.sub(r"^https?://", "", s).rstrip("/") in CSP_BYPASS_HOSTS})
            if gadgets:
                issues.append(Issue(LOW, header, "script-src allowlists hosts with known JSONP/"
                                                 "script gadgets: " + " ".join(gadgets)))
    obj = _effective(d, "object-src")
    if obj is None or (obj and any(s.lower() in _WIDE for s in obj)):
        issues.append(Issue(LOW, header, "object-src not restricted (set object-src 'none')"))
    if "base-uri" not in d:
        issues.append(Issue(INFO, header, "no base-uri: injected <base> tags can redirect relative "
                                          "script URLs"))
    return issues


def analyze_csp(enforced: list[str], report_only: list[str]) -> list[Issue]:
    h = "Content-Security-Policy"
    if not enforced:
        issues = [Issue(MEDIUM, h, "missing: no mitigation against XSS / data injection")]
        if report_only:
            issues.append(Issue(INFO, h + "-Report-Only", "present but only reports, nothing is enforced"))
        return issues
    issues = []
    policies = [p for v in enforced for p in parse_csp(v)]
    # with several policies a source must pass all of them: judge the strictest
    # by only reporting issues that every policy shares
    per_policy = [analyze_csp_policy(p, h) for p in policies]
    if per_policy:
        common = {i.message for i in per_policy[0]}
        for other in per_policy[1:]:
            common &= {i.message for i in other}
        issues = [i for i in per_policy[0] if i.message in common]
    return issues


# --------------------------------------------------------------------------
# framing (clickjacking)
# --------------------------------------------------------------------------

@dataclass
class Framing:
    frameable: bool
    reason: str
    issues: list = field(default_factory=list)


def frame_ancestors(enforced_csp: list[str]) -> list[list[str]]:
    return [p["frame-ancestors"] for v in enforced_csp for p in parse_csp(v) if "frame-ancestors" in p]


def analyze_framing(xfo_values: list[str], enforced_csp: list[str]) -> Framing:
    """Can a cross-origin page frame this response?

    Follows the HTML spec: CSP frame-ancestors (enforced, header only) takes
    precedence over X-Frame-Options; conflicting XFO values block framing;
    unknown XFO values (ALLOW-FROM included) are ignored by browsers.
    """
    issues = []
    fa = frame_ancestors(enforced_csp)
    if fa:
        # every policy must allow the embedder; one restrictive policy is enough
        for sources in fa:
            low = [s.lower() for s in sources]
            if not any(s in ("*", "http:", "https:", "http://*", "https://*") for s in low):
                return Framing(False, "CSP frame-ancestors " + (" ".join(sources) or "(empty = 'none')"))
        issues.append(Issue(MEDIUM, "Content-Security-Policy",
                            "frame-ancestors allows any origin: " + " ".join(fa[0])))
        return Framing(True, "CSP frame-ancestors allows any origin", issues)

    values = {v.strip().lower() for raw in xfo_values for v in raw.split(",") if v.strip()}
    if len(values) > 1:
        if values & {"deny", "sameorigin"}:
            issues.append(Issue(INFO, "X-Frame-Options", "conflicting values "
                                f"{sorted(values)}; browsers fall back to DENY"))
            return Framing(False, "X-Frame-Options (conflicting values, treated as DENY)", issues)
        return Framing(True, f"X-Frame-Options has only invalid values {sorted(values)}", issues)
    if values & {"deny", "sameorigin"}:
        return Framing(False, "X-Frame-Options " + next(iter(values)).upper())
    if values:
        value = next(iter(values))
        note = "ALLOW-FROM is not supported by modern browsers" if value.startswith("allow-from") \
            else f"invalid value '{value}'"
        issues.append(Issue(MEDIUM, "X-Frame-Options", f"{note}: the header is ignored"))
        return Framing(True, f"X-Frame-Options ignored ({note})", issues)
    issues.append(Issue(MEDIUM, "X-Frame-Options", "neither X-Frame-Options nor CSP frame-ancestors "
                                                   "is set: the page can be framed (clickjacking)"))
    return Framing(True, "no X-Frame-Options or CSP frame-ancestors", issues)


# --------------------------------------------------------------------------
# cookies
# --------------------------------------------------------------------------

SESSION_NAME = re.compile(r"sess|sid\b|^sid|token|auth|jwt|login|remember|^id$|_id$|user|"
                          r"jsessionid|phpsessid|asp\.net|connect\.sid|laravel|csrf|xsrf", re.I)
CSRF_NAME = re.compile(r"csrf|xsrf", re.I)


@dataclass
class Cookie:
    name: str
    value: str
    attrs: dict
    raw: str

    @property
    def secure(self) -> bool:
        return "secure" in self.attrs

    @property
    def httponly(self) -> bool:
        return "httponly" in self.attrs

    @property
    def samesite(self) -> str:
        return self.attrs.get("samesite", "")

    @property
    def deleted(self) -> bool:
        """Set-Cookie that only clears a cookie (expired / max-age<=0)."""
        age = self.attrs.get("max-age", "")
        if age.lstrip("-").isdigit() and int(age) <= 0:
            return True
        m = re.search(r"\b(19[0-9]{2}|200[0-9])\b", self.attrs.get("expires", ""))
        return bool(m)


def parse_set_cookie(raw: str) -> Cookie | None:
    parts = raw.split(";")
    name, sep, value = parts[0].partition("=")
    if not sep or not name.strip():
        return None
    attrs = {}
    for p in parts[1:]:
        k, _, v = p.strip().partition("=")
        if k:
            attrs[k.strip().lower()] = v.strip()
    return Cookie(name.strip(), value.strip(), attrs, raw.strip())


def analyze_cookie(c: Cookie, https: bool, host: str = "") -> list[Issue]:
    issues = []
    sensitive = bool(SESSION_NAME.search(c.name))
    kind = "session-like cookie" if sensitive else "cookie"
    label = f"Set-Cookie {c.name}"
    if not c.secure:
        if https:
            issues.append(Issue(MEDIUM if sensitive else LOW, label,
                                f"{kind} without Secure: it is also sent over plain HTTP"))
        else:
            issues.append(Issue(LOW if sensitive else INFO, label,
                                f"{kind} without Secure, set over plain HTTP (site not using TLS)"))
    if not c.httponly:
        if CSRF_NAME.search(c.name):
            issues.append(Issue(INFO, label, "no HttpOnly (usually intended: double-submit CSRF "
                                             "tokens must be readable by JavaScript)"))
        else:
            issues.append(Issue(MEDIUM if sensitive else LOW, label,
                                f"{kind} without HttpOnly: readable by JavaScript (XSS can steal it)"))
    ss = c.samesite.lower()
    if not ss:
        issues.append(Issue(LOW if sensitive else INFO, label,
                            "no SameSite (browsers default to Lax, older ones send it cross-site)"))
    elif ss == "none":
        if not c.secure:
            issues.append(Issue(LOW, label, "SameSite=None without Secure: modern browsers reject the cookie"))
        elif sensitive:
            issues.append(Issue(LOW, label, "SameSite=None: sent on cross-site requests (CSRF exposure)"))
    elif ss not in ("lax", "strict"):
        issues.append(Issue(LOW, label, f"invalid SameSite value '{c.samesite}'"))
    if c.name.startswith("__Host-") and (not c.secure or c.attrs.get("path", "") != "/"
                                         or "domain" in c.attrs):
        issues.append(Issue(LOW, label, "__Host- prefix requires Secure, Path=/ and no Domain: "
                                        "browsers reject it"))
    elif c.name.startswith("__Secure-") and not c.secure:
        issues.append(Issue(LOW, label, "__Secure- prefix without Secure: browsers reject it"))
    dom = c.attrs.get("domain", "").lstrip(".").lower()
    if sensitive and dom and host and host.lower() != dom and host.lower().endswith("." + dom):
        issues.append(Issue(INFO, label, f"scoped to the parent domain .{dom}: every subdomain "
                                         "receives it"))
    return issues


# --------------------------------------------------------------------------
# full audit
# --------------------------------------------------------------------------

VERSION = re.compile(r"/\s*v?\d|\b\d+\.\d+")
LEAK_HEADERS = ("Server", "X-Powered-By", "X-AspNet-Version", "X-AspNetMvc-Version",
                "X-Generator", "X-Version", "X-Backend-Server", "X-Server",
                "X-Drupal-Cache", "X-Mod-Pagespeed", "X-Powered-CMS", "Liferay-Portal")
DEBUG_HEADERS = ("X-Debug-Token", "X-Debug-Token-Link", "X-Debug", "X-Debugkit",
                 "X-Laravel-Debugbar", "X-Clockwork-Id", "X-Rack-Mini-Profiler")


def _first(resp, name: str) -> str:
    return (resp.headers.get(name) or "").strip()


def audit(resp) -> list[Issue]:
    """Every header issue of a response (the page the browser ends up on)."""
    https = urlsplit(resp.url).scheme == "https"
    issues: list[Issue] = []

    issues += analyze_hsts(raw_values(resp, "Strict-Transport-Security"), https)

    csp = raw_values(resp, "Content-Security-Policy")
    csp_ro = raw_values(resp, "Content-Security-Policy-Report-Only")
    html = is_html(resp)
    if html:
        issues += analyze_csp(csp, csp_ro)
        issues += analyze_framing(raw_values(resp, "X-Frame-Options"), csp).issues
    elif not csp:
        issues.append(Issue(INFO, "Content-Security-Policy", "missing (response is not HTML)"))
    for legacy in ("X-Content-Security-Policy", "X-WebKit-CSP"):
        if resp.headers.get(legacy):
            issues.append(Issue(INFO, legacy, "obsolete prefixed CSP header, use Content-Security-Policy"))

    xcto = _first(resp, "X-Content-Type-Options")
    if xcto.lower() != "nosniff":
        msg = "missing" if not xcto else f"invalid value '{xcto}' (only 'nosniff' is valid)"
        issues.append(Issue(LOW, "X-Content-Type-Options", msg + ": MIME sniffing allowed"))

    rp = _first(resp, "Referrer-Policy")
    last = [v.strip().lower() for v in rp.split(",") if v.strip()][-1:] or [""]
    if not rp:
        issues.append(Issue(INFO, "Referrer-Policy", "missing (browsers default to "
                                                     "strict-origin-when-cross-origin)"))
    elif last[0] in ("unsafe-url", "no-referrer-when-downgrade"):
        issues.append(Issue(LOW, "Referrer-Policy", f"'{last[0]}' leaks full URLs (paths, query "
                                                    "tokens) to other sites"))
    elif last[0] == "origin-when-cross-origin" and not https:
        issues.append(Issue(INFO, "Referrer-Policy", f"'{last[0]}'"))

    if html:
        if not resp.headers.get("Permissions-Policy"):
            issues.append(Issue(INFO, "Permissions-Policy", "missing: browser features "
                                                            "(camera, geolocation...) not restricted"))
        if resp.headers.get("Feature-Policy"):
            issues.append(Issue(INFO, "Feature-Policy", "deprecated, replaced by Permissions-Policy"))
        if not resp.headers.get("Cross-Origin-Opener-Policy"):
            issues.append(Issue(INFO, "Cross-Origin-Opener-Policy", "missing: cross-origin windows "
                                                                    "keep a handle (XS-Leaks)"))
    if not resp.headers.get("Cross-Origin-Resource-Policy"):
        issues.append(Issue(INFO, "Cross-Origin-Resource-Policy", "missing: other sites may embed "
                                                                  "this resource (Spectre-style leaks)"))

    xxss = _first(resp, "X-XSS-Protection")
    if xxss and not xxss.startswith("0"):
        issues.append(Issue(INFO, "X-XSS-Protection", f"'{xxss}': deprecated XSS auditor setting "
                                                      "(can enable XS-Leaks in old browsers); set 0 or "
                                                      "rely on CSP"))
    for dep in ("Public-Key-Pins", "Expect-CT"):
        if resp.headers.get(dep):
            issues.append(Issue(INFO, dep, "deprecated header, ignored by modern browsers"))

    for name in LEAK_HEADERS:
        val = _first(resp, name)
        if not val:
            continue
        if VERSION.search(val) or name.startswith("X-AspNet"):
            issues.append(Issue(LOW, name, f"'{val}' discloses software version"))
        elif name != "Server":
            issues.append(Issue(INFO, name, f"'{val}' discloses technology"))
    for name in DEBUG_HEADERS:
        if resp.headers.get(name):
            issues.append(Issue(MEDIUM, name, f"'{_first(resp, name)}': debug/profiler header "
                                              "exposed in production"))

    acao = _first(resp, "Access-Control-Allow-Origin")
    if acao == "*" and _first(resp, "Access-Control-Allow-Credentials").lower() != "true":
        issues.append(Issue(INFO, "Access-Control-Allow-Origin", "'*': any site can read this "
                                                                 "response (fine for public data)"))
    return issues


def by_severity(issues: list[Issue]) -> list[Issue]:
    return sorted(issues, key=lambda i: SEVERITIES.index(i.severity))


def fetch(target, session=None, url: str = ""):
    """GET the target (following redirects); None after saying why it failed."""
    session = session or kit.http()
    url = url or kit.url(target)
    try:
        return session.get(url, allow_redirects=True)
    except Exception as e:
        kit.bad(f"Could not reach {url}: {type(e).__name__}")
        return None


def show(issues: list[Issue], record=None) -> None:
    """Print issues (worst first) and store them, one DB entry per issue."""
    for i in by_severity(issues):
        line = f"{i.header}: {i.message}"
        if i.severity in (HIGH, MEDIUM):
            kit.found(i.severity, line)
        elif i.severity == LOW:
            kit.warn(f"{i.severity} {line}")
        else:
            kit.bullet(f"{i.severity} {line}", indent=1)
        if record:
            record(str(i))
