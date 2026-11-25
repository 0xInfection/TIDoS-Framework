# Setting up TIDoS

This guide assumes TIDoS is already installed ([install.md](install.md)). It
covers:

- [API keys](#api-keys): which keys exist, what they unlock, and how to pass them in
- [Third-party services](#third-party-services): what each module talks to
- [Tor](#tor)
- [Module options](#module-options): `set`, defaults and unattended runs
- [Automation](#automation): CLI one-shots and VAL files
- [Output](#output): where results end up

---

## API keys

TIDoS ships **no** credentials. Keys are read from **environment variables
only**; never write them into the repository. Each key `NAME` is looked up as:

1. `TIDOS_<NAME>` (recommended; the `tidos` launcher forwards these through sudo)
2. `<NAME>`

Most modules need no key at all. A module whose key is missing prints the
variable it wants and stops; nothing else is affected.

### Key reference

| Environment variable | Modules | Required? | Get it from |
|---|---|---|---|
| `TIDOS_SHODAN_API_KEY` | `honeypot` (required), `shodan` (optional: without a key it falls back to the free Shodan InternetDB, which gives ports, CPEs, tags and CVEs but no banners or per-service detail) | See modules | [account.shodan.io](https://account.shodan.io/) → API Key |
| `TIDOS_CENSYS_API_TOKEN` | `censysdom`, `getcensys`, `webscan` (required); `osdetect` (optional extra evidence) | See modules | [Censys Platform](https://platform.censys.io/) → Personal Access Tokens |
| `TIDOS_VIEWDNS_API_KEY` | `mailtodom` (required), `iphistory` (fallback when the website blocks scraping) | See modules | [viewdns.info/api](https://viewdns.info/api/) |
| `TIDOS_WHATCMS_ACCESS_TOKEN` | `cms` | Optional: without it `cms` uses local fingerprinting only | [whatcms.org/API](https://whatcms.org/API) |
| `TIDOS_HACKERTARGET_API_KEY` | `revip`, `revdns`, `subnet`, `getgeoip`, `sharedns`, `subdom` (higher quota); `piwebenum` (needed only for its remote nping fallback) | Optional: the free tier allows a small number of requests per day | [hackertarget.com](https://hackertarget.com/scan-membership/) |
| `TIDOS_GOOGLE_API_TOKEN` | `googlenum` | Legacy | The Google+ API it queries was shut down in 2019; the module reports that no data is returned. |

### Setting keys for a session

```bash
export TIDOS_SHODAN_API_KEY='...'
export TIDOS_CENSYS_API_TOKEN='...'
```

Then start TIDoS the way you installed it:

| Install type | Command | Why |
|---|---|---|
| Global (`tidos` launcher) | `tidos` | The launcher forwards every `TIDOS_*` variable through sudo. |
| Local checkout | `sudo -E .venv/bin/python3 tidconsole.py` | `-E` keeps your environment; plain `sudo` drops it. |
| Local, with restrictive sudoers | `sudo --preserve-env=TIDOS_SHODAN_API_KEY,TIDOS_CENSYS_API_TOKEN .venv/bin/python3 tidconsole.py` | Use this if your sudo policy rejects `-E`. |
| Docker | `docker run -e TIDOS_SHODAN_API_KEY=... ...` or `--env-file` | |

> Keys exported without the prefix (e.g. `SHODAN_API_KEY`) still work, but only
> if you preserve them yourself. The launcher forwards `TIDOS_*` names only.

### Keeping keys in a file

Keep keys in one file that only you can read, and load it when needed:

```bash
mkdir -p ~/.config/tidos
cat > ~/.config/tidos/keys.env <<'EOF'
TIDOS_SHODAN_API_KEY=...
TIDOS_CENSYS_API_TOKEN=...
TIDOS_VIEWDNS_API_KEY=...
EOF
chmod 600 ~/.config/tidos/keys.env
```

```bash
set -a; . ~/.config/tidos/keys.env; set +a   # export everything in the file
tidos
```

The same file works with `docker run --env-file ~/.config/tidos/keys.env`.
Keep it out of the repository; `git status` should never show it.

### Checking which keys are visible

```bash
env | grep '^TIDOS_' | cut -d= -f1                 # names only, values stay hidden
sudo -E env | grep '^TIDOS_' | cut -d= -f1         # what a sudo'd console will see
```

---

## Third-party services

Passive modules send the **target's name or IP** to the services below. Treat
that as disclosure to a third party when scope or opsec matters. Active modules
only talk to the target itself, with the exceptions noted in the table.

| Module | Service(s) contacted | Key |
|---|---|---|
| `censysdom` | api.platform.censys.io | `CENSYS_API_TOKEN` |
| `checkuser` | GitHub, GitLab, PyPI, npm, Docker Hub, Reddit, HN, Steam, Wikipedia and ~10 more profile sites | none |
| `dnschk` | DNS-over-HTTPS resolver (default dns.google; option `RESOLVER`) | none |
| `getconinfo`, `whoischeckup` | rdap.org (follows on to the registry's RDAP server) | none |
| `getgeoip`, `revip`, `revdns`, `subnet`, `sharedns` | api.hackertarget.com | optional |
| `hackedmail` | api.xposedornot.com (sends the e-mail addresses) | none |
| `iphistory`, `mailtodom` | viewdns.info / api.viewdns.info | `VIEWDNS_API_KEY` |
| `piweb` | check-host.net (pings from its nodes) | none |
| `threatintel` | downloads public blocklists (abuse.ch Feodo, blocklist.de, OpenPhish, Phishing Army, Emerging Threats, Binary Defense, Project Honeypot); the target is only matched locally | none |
| `webarchive` | web.archive.org | none |
| `googleSearch`, `googledorker`, `googlegroups`, `linkedin`, `pastebin` | www.google.com | none |
| `googlenum` | www.googleapis.com | legacy |
| `cms` (active) | whatcms.org, in addition to the target | optional |
| Anything that crawls, first use only | github.com (downloads Katana; see [install.md](install.md#3-optional-external-tools)) | none |
| `subdom` (active) | crt.sh and api.hackertarget.com when `PASSIVE=y`, in addition to DNS queries | optional |
| `piwebenum` (active) | api.hackertarget.com, only when `nping` is not installed | `HACKERTARGET_API_KEY` |
| `getcensys`, `webscan` (scan) | api.platform.censys.io (looks up the target's IPs) | `CENSYS_API_TOKEN` |
| `osdetect` (scan) | api.platform.censys.io, only when a token is set, in addition to the target | optional |
| `shodan` (scan) | api.shodan.io with a key, otherwise internetdb.shodan.io | optional |
| `honeypot` (aid) | api.shodan.io (honeyscore) | `SHODAN_API_KEY` |
| `subdomover` (vlnysis) | crt.sh and api.hackertarget.com when `PASSIVE=y` (the default), plus DNS and HTTP to the subdomains | optional |
| `cloudflaremisc` (vlnysis) | api.hackertarget.com when `PASSIVE=y` (the default), plus requests to candidate origin IPs | optional |
| `rfi` (vlnysis) | none from TIDoS itself, but a vulnerable **target** fetches `RFIURL` (default `http://example.com/`) | none |

> Google now serves a JavaScript-only page to scripts. The Google-based modules
> detect this and stop with an explanation rather than returning bad data.

---

## Tor

Start a Tor client that listens on `127.0.0.1:9050`, then switch Tor mode on:

```bash
sudo systemctl start tor        # or run `tor` directly; in Docker start it in the container
```

```text
tid2 > tor on
 [+] Verified Tor exit (check.torproject.org). IP 203.0.113.7 > 185.220.101.1
 [+] Tor ON
tid2 > netinfo        # "Public IP (Tor exit)" now shows the exit address
```

How `tor on` works:

1. It checks that something accepts connections on `127.0.0.1:9050`. If nothing
   does, it offers to `systemctl start tor`; unattended runs try this without
   asking.
2. It asks [check.torproject.org](https://check.torproject.org/api/ip), *through
   that proxy*, whether the request arrived from a Tor exit. Tor mode is only
   enabled when the answer is yes. A proxy on 9050 that isn't Tor is refused
   with its real exit IP shown, and Tor mode stays **off**.

While Tor mode is on, **HTTP requests** made by modules go through
`socks5h://127.0.0.1:9050`, so DNS for those requests is resolved through Tor
too. If Tor stops working mid-session, requests fail instead of falling back to
your direct connection.

Raw-socket work does **not** go through Tor: port scans, DNS bruteforcing,
`dig`, ping, traceroute and TLS certificate grabs. The port scanners warn about
this when Tor is on; plan for it on engagements where your source IP matters.

Per-module behaviour with Tor on:

| Module | Behaviour |
|---|---|
| Crawling (`crawler1/2/3`, the scanners' parameter discovery, `csrf`, `pathtrav`, `CRAWL=y` in the info-disclosure modules) | Katana is given `-proxy socks5://127.0.0.1:9050` |
| `waf`, `webtech`, `getcensys`, `webscan`, `shodan` | HTTP through Tor |
| `getports`, `simpleport`, `tcpconnectscan`, `servicedetect`, raw scanners, `arpscan`, `ssltlsscan`, `osdetect` | Direct connections; a warning is printed |
| `nmapmain` | **Refused** unless you `set LEAK y`. nmap's `--proxies` only covers NSE and version probes; host discovery, the port scan itself and DNS go out directly (verified). With `LEAK=y` only TCP-connect profiles run, with `-sT -Pn --proxies`. |
| Vulnerability scanners (`sqli`, `xss`, `lfi`, ..., `headers`, `icors`, `hhi`, ...) | HTTP through Tor |
| `*brute` (FTP/POP/SMTP/MySQL/SSH/Telnet/XMPP), `netmisc` | Direct connections; a warning is printed |
| `zone`, `mailspoof`, `ssscript`, `subdomover` (DNS part), `cloudflaremisc` (origin probes) | Direct DNS / connections; a warning is printed |

`tor off` switches routing back to direct and, on a terminal, offers to stop the
tor service.

> SOCKS support comes from the `PySocks` package (in `requirements.txt`). If
> it's missing, `tor on` says so instead of enabling Tor.

---

## Module options

Every module lists its options with `opts` (or `info`):

```text
tid2 > load subdom
tid2(subdom) > opts
tid2(subdom) > set BRUTE n
tid2(subdom) > set WORDLIST /path/to/labels.txt
tid2(subdom) > attack
```

An option's value is resolved in this order:

1. the value you `set`; `set KEY none` means "explicitly empty";
2. otherwise, when running in an interactive terminal, a prompt where
   **Enter accepts the default** shown in brackets;
3. otherwise (CLI one-shots, VAL files, piped input) the default, so
   unattended runs never block on a prompt.

Commonly used options:

| Option | Modules | Meaning |
|---|---|---|
| `WORDLIST` | active-recon `*brute`, `apachestat`, `phpinfo`, `subdom` | Path list to try; defaults live in `files/fuzz-db/` |
| `TYPES` | `filebrute` | Comma list of `backdoor,backup,dot,pass,proxy,index,log`, or `all` |
| `CRAWL` | info-disclosure modules, `commentssrc` | `y` to also scan same-host pages linked from the target |
| `PORTS` | `getports`, port scanners, `osdetect`, `nmapmain`, `censysdom` | e.g. `22,80,443,8000-8100`; empty means the common-ports list |
| `EMAIL` | `hackedmail`, `mailtodom` | Comma-separated addresses to look up |
| `LIMIT` | Google modules, `webarchive` | Maximum number of results |
| `TIMEOUT` | raw scanners, `servicedetect`, `arpscan`, `nmapmain` | Seconds to wait (decimals allowed for scanners, e.g. `0.5`) |
| `VERBOSE` | raw scanners, `tcpconnectscan` | `y` to also list closed ports |
| `MAXPAGES`, `INCLUDE_EXTERNAL` | `crawler1/2/3` | Page cap (default 200); list off-host links (never followed) |
| `PROFILE`, `TIMING`, `EXTRA`, `DECOY`, `LEAK` | `nmapmain` | Scan profile (default `basic`; `info` lists all), `-T0`..`-T5`, extra nmap args (output/input/proxy options are rejected), decoys for `evade`, allow scanning with Tor on |
| `IP`, `NMASK`, `FORCE` | `arpscan` | Network to sweep (CIDR or IP + mask); `FORCE=y` for sweeps larger than /16 |
| `PORT` | `ssltlsscan`, `sslcert` | TLS port (default: the URL's port for https, else 443) |
| `PARAM` | injection scanners (`sqli`, `xss`, `lfi`, `rfi`, `phpi`, `rce`, `htmli`, `crlf`, `openredirect`, `ldap`, `xpathi`) | Endpoint to test: `/page.php?id=1`, a full URL, or `POST /login user=a&pass=b`. Every parameter in it is tested. Empty: the target URL's own parameters plus a crawl |
| `DEPTH`, `MAXPOINTS` | injection scanners, `csrf` | Crawl depth when `PARAM` is empty (default 1); cap on parameters tested (default 40) |
| `COOKIE`, `HEADERS` | `crawler1/2/3`, injection scanners, `csrf`, `pathtrav`, `cookiecheck`, `icors`, `hhi`, info-disclosure modules, `commentssrc` | Authenticated testing. `COOKIE` is a Cookie header (`PHPSESSID=abc; role=x`); `HEADERS` adds request headers, several separated by `\|\|` (`Authorization: Bearer eyJ... \|\| X-Api-Key: k1`). Both go with every request, including the parameter-discovery crawl. These are never prompted for: set them or they're empty. (`sessionfix` only takes `COOKIE`.) |
| `TECHNIQUE`, `DELAY` | `sqli` | `error`, `boolean`, `time` or `all` (default `error,boolean`; time-based is opt-in because sleep payloads load the target's database); sleep seconds for `time` |
| `BLIND`, `SLEEP` | `phpi`, `rce` | Time-based checks on/off (default y) and the sleep length (default 5) |
| `TESTHEADERS` | `xss` | Also test User-Agent, Referer and cookie reflection (default y) |
| `RFIURL`, `RFIMARK` | `rfi` | Remote file to include and the text that proves it was included (default: example.com and its `<title>`) |
| `PATH` | `strutsshock` | Comma-separated action path(s) or URL(s) to test (default: the target URL) |
| `PATH`, `SHELL-IP`, `SHELL-PORT` | `shellshock` | CGI path to test (default: the target URL). Set `SHELL-IP`/`SHELL-PORT` (with a listener ready) to send a reverse shell once the bug is confirmed; left empty it only detects |
| `LANG`, `PARAM`, `PASSWORD` | `shellcraft` (post) | Webshell language (`php`/`jsp`/`asp`, default `php`), the command parameter name (default `cmd`), and the access password (a random one is generated if empty). The shell is written to `tmp/logs/<host>-logs/` |
| `STRING` | `hashes`, `encodeall` (aid) | Text to hash / encode; empty prompts interactively |
| `PATH` | `imgext` (aid) | Path to the image whose EXIF/GPS metadata to read |
| `IP`, `PORT`, `USERS`, `PASSWORDS`, `COMBO`, `THREADS`, `DELAY`, `TIMEOUT`, `STOP` | `*brute` (vlnysis) | Host (default: the target's IP), port (protocol default), credential lists (defaults in `files/brute-db/`), optional `user:pass` file, parallel logins (2-4 by default; servers ban fast), pause between attempts, socket timeout, stop at the first valid login (default y) |
| `SUBDOM`, `PASSIVE`, `BRUTE` | `subdomover` | Check one subdomain; otherwise enumerate via passive sources (default y) and/or DNS bruteforce (default n) |
| `DNSV`, `DOMAIN` | `zone`, `mailspoof` | Name server to try AXFR against (default: all NS); mail domain to check (default: the target's domain) |

When a crawl is authenticated (`COOKIE`/`HEADERS`, or credentials in the
target URL), links and forms that look like logout (`logout`, `signout`,
`logoff`, ...) are listed but never requested, and the injection scanners
don't test them, so the session survives the crawl.

Concurrency for brute-forcing, crawling and port scanning follows the console's
`processes N` setting (default: number of CPUs).

### Modules that need root

Run the console as root (as `tidos` and `sudo -E` do) for these; without root
they stop with a clear message and suggest an unprivileged alternative:

| Module | Why |
|---|---|
| `tcpstealthscan`, `finscan`, `xmasscan` | Craft raw TCP packets (use `tcpconnectscan` / `getports` otherwise) |
| `arpscan`, `vicadd --net` | Raw ARP sweep |
| `nmapmain` profiles `syn`, `os`, `udp`, `aggressive`, `reflectors`, `evade` | nmap needs root for these scan types |
| `osdetect` | Only its optional `nmap -O` step; the rest works unprivileged |
| `traceroute` | ICMP/TCP modes on Linux |

---

## Automation

**One module, one target:**

```bash
tidos -v https://target.example -l whoischeckup
tidos -v https://target.example -l passive-all     # every passive module
```

**Several modules with options, several targets: VAL files.** Put the file in
`core/sessioncache/` and run `tidos -c NAME`:

```text
<victim https://target.example>
  <module subdom>
    BRUTE:n;
    PASSIVE:y
  </module>
  <module filebrute>
    TYPES:dot,backup
  </module>
</victim>
```

> The `photon` module is gone: `crawler1/2/3` (Katana) cover crawling, and the
> info-disclosure modules cover what Photon extracted (emails, keys, secrets).
>
> VAL files from older TIDoS versions: `crawler3`'s `LIMIT` option is now
> `MAXPAGES` (shared by `crawler1/2/3`); `nmapmain` and `filebrute` now take
> their choices from `PROFILE` / `TYPES` instead of interactive menus.
> Vulnerability analysis:
> - `PARALLEL` is gone from every scanner; concurrency follows `processes`.
> - `sqli` picks error/blind with `TECHNIQUE` instead of a menu.
> - `lfi` no longer has `EVASION` / `FILE`; its payload list covers the
>   evasion variants.
> - `htmli`, `crlf` and `openredirect` dropped `DICT`, because their payloads
>   are built around random markers.
> - `rfi`'s `DICT` is now an optional list of known vulnerable-application paths.
> - `pathtrav` is now a native scanner (no external Vailyn): it tests traversal
>   both through parameters (`PARAM`) and in the URL path (`DIRECTORY`, `DEPTH`,
>   `MAXDIRS`). Use `lfi` for absolute-path reads and php:// wrappers.

In the console, `sessions save NAME --val` writes the current targets and the
options you've `set` to such a file, and `sessions load NAME.val` restores them.

The `*-all` modules (`passive-all`, `active-all`, `infdisc-all`, `scan-all`,
`vlnysis-all`) run a whole
category. They continue past a failing module and finish with a summary such
as `osint-active: 24/24 modules completed`.

---

## Output

| What | Where |
|---|---|
| Findings, per target/module | SQLite: `core/database/tidos.db` (created on first run) |
| Files written by modules (subdomain lists, Censys JSON, PoCs) | `tmp/logs/<host>-logs/` |
| Crawled URL lists (`crawler1/2/3`) | `tmp/logs/<host>-logs/<host>-links.lst` |
| Clickjacking PoC, successful zone transfers | `tmp/logs/<host>-logs/clickjack-poc.html`, `<domain>-axfr-<server>.txt` |
| Saved target lists / VAL sessions | `core/sessioncache/` |

> These locations collect real engagement data. `core/database/tidos.db` and
> `tmp/logs/*-logs/` are git-ignored, so `git add -A` won't pick them up. Back
> them up or wipe them per engagement as your rules require.
