# TIDoS test suite

A deliberately-vulnerable local site plus a runner that points the TIDoS
modules at it and checks they detect what they should.

```bash
pip install -r requirements.txt     # the suite uses the framework's own deps
python3 tests/run.py                 # deep detection tests + contract smoke
python3 tests/run.py --run-smoke     # also run every other module once
python3 tests/run.py -k sqli         # only cases/modules matching a substring
```

The runner exits non-zero if any deep case fails, any module breaks the module
contract, or (with `--run-smoke`) any module raises an unhandled exception.

## What runs

**Deep detection cases** — the core of the suite. Each case points one module
at a crafted endpoint on the vulnerable site and asserts it reports the bug;
several also point the module at a safe twin and assert it stays quiet (no
false positive). Covered: `sqli`, `xss`, `lfi`, `rfi`, `phpi`, `rce`, `htmli`,
`crlf`, `openredirect`, `ldap`, `xpathi`, `clickjack`, `headers`,
`cookiecheck`, `icors`, `hhi`, `sessionfix`, `hsts` (HTTPS), the
information-disclosure modules (`emailext`, `creditcards`, `ssn`, `phone`,
`internalip`, `secrets`, `errors`), `commentssrc`, and `shellshock`.

**Contract smoke** — imports every module under `modules/` and checks it
exposes the `info` / `searchinfo` / `properties` / `attack` contract the
console, CLI and GUI rely on. Helper files placed in module directories (e.g.
`wafimpo`) are skipped, as discovery doesn't list them.

**Run smoke** (`--run-smoke`) — runs each remaining module once against the
site, bounded by a per-module timeout, failing only on an unhandled exception.
External-OSINT modules (Shodan, Google, whois, DNS, ...) simply error out
without network access or an API key; that is expected and not a failure.

## The vulnerable site (`tests/vulnsite/`)

A cluster of `127.0.0.1` servers started together by `VulnSite`:

| Server (port)        | Covers |
|----------------------|--------|
| sqli (8771)          | SQLi (error/boolean/time) and XSS, backed by a real in-memory SQLite oracle |
| fileinj (8772)       | LFI, RFI, path traversal, PHP injection, command injection, Shellshock, Struts (all emulated — nothing is executed) |
| webinj (8773)        | HTML injection, CRLF, open redirect, LDAP, XPath, CSRF |
| misconf (8774 / 18774 TLS) | security headers, clickjacking, cookies, CORS, host-header injection, session fixation, TRACE, HSTS |
| recon (8775)         | leaked emails / cards / SSNs / phones / internal IPs / secrets / stack traces, HTML comments, robots.txt, phpinfo, WebDAV |

Every endpoint serves fabricated data over loopback only. "Vulnerable"
behaviour (shell, PHP, SQL, OGNL) is emulated with pattern matching — the site
never runs anything. The HTTPS server needs `openssl` on `PATH` to mint a
throwaway certificate; without it the HSTS case is skipped.

```python
from tests.vulnsite import VulnSite
with VulnSite() as site:
    print(site.url("sqli"))   # http://127.0.0.1:8771
```

## Scope

The suite targets the web-facing modules that can be driven against a local
site. Brute-force modules (which need live FTP/SSH/SMTP/… services) and the
external-OSINT modules (which query the real internet) are covered only by the
contract smoke, not by deep detection cases.
