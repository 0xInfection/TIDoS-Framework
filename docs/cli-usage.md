# TIDoS command line

Besides the interactive console, every TIDoS module runs non-interactively from
the command line. Modules are addressed by a readable path and selected with the
same `-u`/`-m` flags whether you run one module, a whole sub-phase, or everything.

Running `tidos` with **no arguments** opens the interactive console instead.

- [Invocation](#invocation)
- [Module paths](#module-paths)
- [Selecting what to run](#selecting-what-to-run)
- [Running modules](#running-modules)
- [Setting module options](#setting-module-options)
- [Discovering modules: `--list` and `--info`](#discovering-modules---list-and---info)
- [Checking dependencies: `--check`](#checking-dependencies---check)
- [Reading findings back: `--results`](#reading-findings-back---results)
- [Full option reference](#full-option-reference)
- [Notes](#notes)

---

## Invocation

How you invoke `tidos` depends on how it was installed (see
[install.md](install.md)):

```bash
# local checkout -- run as root so raw-socket modules work; -E keeps TIDOS_* keys
sudo -E .venv/bin/python3 tidos.py -u http://target -m osint/activerecon/dotbrute

# global /opt install -- the launcher calls sudo itself
tidos -u http://target -m osint/activerecon/dotbrute

# Docker
docker run -it --rm tidos -u http://target -m osint/activerecon/dotbrute
```

The rest of this guide writes `tidos` for brevity.

## Module paths

Every module has a path of the form `<phase>[/<sub-phase>]/<module>`, for
example `osint/passiverecon/getgeoip`. The path mirrors the module tree on disk,
but with short, lowercase aliases:

| Phase directory | Path alias |
|---|---|
| `OSINTFootprinting` | `osint` |
| `ScanningEnumeration` | `scan` |
| `VlnAnalysis` | `vuln` |
| `SploitLoot` | `sploit` |
| `PostSploit` | `post` |
| `Aid` | `aid` |

| Sub-phase directory | Path alias |
|---|---|
| `PassiveRecon` | `passiverecon` |
| `ActiveRecon` | `activerecon` |
| `InfoDisclose` | `infodisc` |
| `Misconfig` | `misconfig` |
| `Severe` | `severe` |
| `Other` | `other` |
| `PortScanning` | `portscanning` |
| `WebCrawling` | `webcrawling` |

Use [`--list`](#discovering-modules---list-and---info) to print every path.

## Selecting what to run

`-m/--module` accepts several shapes, from one module up to the whole framework:

| Selector | Runs |
|---|---|
| `osint/passiverecon/getgeoip` | one module (full path) |
| `osint/passiverecon` | every module in a sub-phase |
| `osint/all` or `osint` | every module in a phase |
| `all` | every module, every phase |
| `getgeoip` | a bare module name (matched across all phases) |

`-m` is repeatable and also accepts comma-separated values, so these are
equivalent:

```bash
tidos -u http://target -m osint/activerecon/dotbrute -m vuln/misconfig/headers
tidos -u http://target -m osint/activerecon/dotbrute,vuln/misconfig/headers
```

## Running modules

A single module against one target:

```bash
tidos -u http://target -m osint/activerecon/dotbrute
```

```text
 [*] Target http://target -- 1 module(s)

 [*] >> osint/activerecon/dotbrute

 O S I N T · A C T I V E
 D O T   F I L E   B R U T E

 [*] Hunting dot files on http://target (39 paths)
 [+] Found (200) :> http://target/.bash_history   44B
 [+] Found (200) :> http://target/.htaccess   34B
 [+] 2 possible dot files found
 [+] Done.
```

`-u/--url` is repeatable too; every selected module runs against every target.
`--tor` routes HTTP through Tor (the connection is verified first), `--processes
N` sets the worker count for parallel modules, and `-q/--quiet` suppresses the
start-up banner.

```bash
tidos -u http://a.example -u http://b.example -m scan/all --tor --processes 8 -q
```

## Setting module options

Modules expose options (shown by [`--info`](#discovering-modules---list-and---info)).
Set them with `--set OPT=VALUE`, repeatable:

```bash
tidos -u http://target -m vuln/severe/sqli \
      --set PARAM=/product.php?id=1 \
      --set COOKIE=session=abc123
```

The path-hunting and injection modules take a `PARAM` option pointing at the
endpoint to test; when it is empty they crawl the site to find endpoints (which
needs [Katana](install.md#3-optional-external-tools)).

## Discovering modules: `--list` and `--info`

List every module and its path, or narrow to a phase / sub-phase:

```bash
tidos --list                 # everything
tidos --list osint           # one phase
tidos --list osint/passiverecon
```

```text
  osint
    osint/passiverecon/censysdom               CENSYS Domain Recon
    osint/passiverecon/checkuser               Alias Check
    osint/passiverecon/dig                     Dig DNS lookup
    osint/passiverecon/dnschk                  DNS Lookup Module
    osint/passiverecon/getgeoip                GeoIP Lookup
    ...
```

Show one module's description and its options:

```bash
tidos --info osint/activerecon/dotbrute
```

```text
  osint/activerecon/dotbrute  --  Hidden File Enumeration
  Looks for exposed dot files (.htaccess, .git, .env, ...) on the target's webserver.
  options:
    WORDLIST  Wordlist of paths to request
```

## Checking dependencies: `--check`

Report which Python libraries and external tools TIDoS can find on this host,
and what each one powers. Missing **required** packages make it exit non-zero;
optional ones are listed as warnings with install hints.

```bash
tidos --check
```

```text
 [*] TIDoS environment check

 Python libraries
 [+] requests     present   (HTTP engine (every web module))
 [+] bs4          present   (HTML parsing (crawlers, scrapers))
 [!] scapy        missing   [optional] raw-socket scanners, arpscan  ->  pip install scapy
 [!] wafw00f      missing   [optional] WAF detection  ->  pip install wafw00f
 ...
 External tools
 [+] nmap         present   (/usr/bin/nmap)
 [!] tor          missing   (Tor routing (tor on))
 ...
 Crawler
 [+] katana       present   (tools/bin/katana)

 [+] All required packages present.
```

## Reading findings back: `--results`

As modules run they record findings in the session database
(`core/database/tidos.db`). Read them back, grouped by target.

List the targets that have stored findings:

```bash
tidos --results
```

```text
 [*] Stored findings by target:
 [+] 127.0.0.1  (1 record(s))
 [*] View one with: tidos --results <target>
```

Dump the findings for one target (the argument is a case-insensitive substring):

```bash
tidos --results 127.0.0.1
```

```text
 [*] Findings for 127.0.0.1

 [+] Reconnaissance & OSINT / Active Reconnaissance / filebrute / dotbrute  #1
   - http://127.0.0.1:8781/.bash_history (200,  44B )
   - http://127.0.0.1:8781/.htaccess (200,  34B )
```

Each record is labelled with its phase and module path and numbered per target.
The database is git-ignored and rebuilds itself on first write.

## JSON output

`--list` and `--results` emit machine-readable JSON with `--json` (the banner is
suppressed automatically, so the output is a clean document you can pipe to
`jq`):

```bash
tidos --list osint --json
tidos --results example.com --json
```

```json
[
  {
    "path": "osint/passiverecon/getgeoip",
    "name": "GeoIP Lookup",
    "module": "modules.OSINTFootprinting.PassiveRecon.getgeoip"
  }
]
```

## Full option reference

```text
usage: tidos [-h] [-u URL] [-m PATH] [--set OPT=VALUE] [--list [CATEGORY]]
             [--info PATH] [--check] [--results [TARGET]] [--tor]
             [--processes N] [-q]

  -h, --help          show this help message and exit
  -u, --url URL       target URL (repeatable; comma-separated values accepted)
  -m, --module PATH   module path to run: all | <phase> | <phase>/<sub> |
                      <phase>/<sub>/<module> | <phase>/all | <module>
                      (repeatable)
  --set OPT=VALUE     set a module option (repeatable), e.g. --set PARAM=/p.php?id=1
  --list [CATEGORY]   list modules (optionally only a phase/sub-phase) and exit
  --info PATH         show a module's description and options, then exit
  --check             report which Python libraries and external tools are
                      available, then exit
  --results [TARGET]  show findings recorded in the database (optionally for
                      one target), then exit
  --json              machine-readable JSON output (with --list or --results)
  --tor               route HTTP through Tor (verified first)
  --processes N       worker processes for parallel modules
  -q, --quiet         do not print the banner
```

## Notes

- **Root.** Raw-socket modules (port scans, ARP, traceroute) need root; the CLI
  warns `[!] Not running as root...` and keeps going for everything else.
- **Missing tools degrade gracefully.** If a module needs an external tool or
  optional library that isn't installed, that module says so and stops; the rest
  of the run continues. Use `--check` to see what's available up front.
- **Exit codes.** `0` on success, `1` for a bad selector / missing dependency,
  `2` for a usage error (e.g. `-m` without `-u`).
- **Run from the repository root.** TIDoS reads `core/doc/*` and writes
  `tmp/logs/` relative to the current directory.
- **API keys** come only from the environment (`TIDOS_<NAME>`); see
  [setup.md](setup.md).
