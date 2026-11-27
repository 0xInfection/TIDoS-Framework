# Installing TIDoS

TIDoS runs on **Linux** and **macOS** with **Python 3.7+**. The console must run
as **root**, because several modules open raw sockets (port scans, ARP,
traceroute). On macOS, install the external tools with Homebrew (`brew install
nmap tcpdump tor`, etc.) and use the local checkout below — the global `/opt`
installer is Debian-only.

Once TIDoS is installed, configure your API keys with [setup.md](setup.md).

- [1. System packages](#1-system-packages)
- [2. Install TIDoS](#2-install-tidos)
  - [Option A: local checkout (recommended)](#option-a-local-checkout-recommended)
  - [Option B: global install to /opt](#option-b-global-install-to-opt)
  - [Option C: Docker](#option-c-docker)
- [3. Optional external tools](#3-optional-external-tools)
- [4. First launch](#4-first-launch)
- [5. Updating](#5-updating)
- [6. Uninstalling](#6-uninstalling)

---

## 1. System packages

Debian / Ubuntu / Kali:

```bash
sudo apt-get update
sudo apt-get install -y git python3 python3-pip python3-venv build-essential pkg-config \
    libxml2 libexiv2-dev default-libmysqlclient-dev \
    nmap tcpdump tor dnsutils traceroute iputils-ping
```

Fedora / RHEL:

```bash
sudo dnf install -y git python3 python3-pip gcc gcc-c++ pkgconf-pkg-config \
    libxml2 exiv2-devel mariadb-connector-c-devel \
    nmap tcpdump tor bind-utils traceroute iputils
```

What the system tools are used for:

| Package | Used by |
|---|---|
| `nmap` (includes `nping`) | `nmapmain`, `osdetect` (root only), `piwebenum` |
| `dnsutils` / `bind-utils` (`dig`) | `dig` |
| `traceroute` | `traceroute` |
| `iputils-ping` | `piwebenum`, `vicadd --ip` |
| `tor` | `tor on` (HTTP via Tor, verified against check.torproject.org); see [setup.md](setup.md#tor) |
| `tcpdump` | scapy-based scanners |

Python packages worth knowing about: `scapy` powers the raw scanners and
`arpscan`. `sslyze` powers `ssltlsscan`; current sslyze releases need
**Python 3.9+**, and on 3.7/3.8 the module falls back to a basic stdlib
protocol check. `PySocks` is required for `tor on`. `paramiko` and `PyMySQL`
power `sshbrute` and `sqlbrute`; without them those two modules say so and stop.
`Pillow` powers the `imgext` (aid) EXIF/GPS reader; without it the module says so
and stops.

If a tool is missing, the module that needs it stops and says so. The rest of
the framework keeps working. To see at a glance which Python libraries and
external tools TIDoS can find on this host, run:

```bash
tidos --check
```

It lists every dependency, whether it's present, and what each one powers;
required packages missing make it exit non-zero.

## 2. Install TIDoS

### Option A: local checkout (recommended)

Recent Debian and Ubuntu releases block `pip install` into the system Python
(PEP 668, "externally-managed-environment"). A virtual environment avoids that:

```bash
git clone https://github.com/0xinfection/tidos-framework.git
cd tidos-framework
python3 -m venv .venv
.venv/bin/pip install -e .
```

`pip install -e .` installs the dependencies and a `tidos` command that points
at this checkout. Run the console as root; `-E` keeps your exported API keys,
because sudo drops the environment by default:

```bash
sudo -E .venv/bin/tidos                 # or: sudo -E .venv/bin/python3 tidos.py
```

The `tidos` command works from any directory -- it anchors itself to the
checkout, where TIDoS reads `core/doc/*` and `files/*` and writes `tmp/logs/`.
(If you prefer not to install, `pip install -r requirements.txt` and run
`python3 tidos.py` from the repository root instead.)

### Option B: global install to /opt

`core/install.py` installs the apt packages and pip requirements, copies the
framework to `/opt/TIDoS` and installs a `tidos` launcher in `/usr/bin`. Run it
from inside `core/`:

```bash
cd tidos-framework/core
sudo python3 install.py
```

Then:

```bash
tidos                        # console (the launcher calls sudo itself)
tidos --list                 # list every module and its path
tidos -u http://target -m osint/activerecon/dig
```

The launcher passes every `TIDOS_*` environment variable through `sudo`. Export
keys with the `TIDOS_` prefix and they reach the console without any extra
flags (see [setup.md](setup.md#api-keys)).

> The installer runs `pip3 install` against the system Python. On distributions
> that enforce PEP 668 this step fails. Either use Option A, or install the
> requirements yourself first (for example into a venv you point `python3` at).

### Option C: Docker

A Debian-based `Dockerfile` lives at the repository root:

```bash
cd tidos-framework
docker build -t tidos .
docker run -it --rm --env-file ~/.config/tidos/keys.env tidos   # console
docker run -it --rm tidos bash                                   # drop to a shell
```

`--env-file` takes the same `TIDOS_*=value` lines described in
[setup.md](setup.md#keeping-keys-in-a-file); you can also pass single keys with
`-e TIDOS_SHODAN_API_KEY=...`.

> The image copies your local checkout (honouring `.dockerignore`), so it builds
> the code you have on disk. Run with `-it` -- the console is interactive and
> shows the usage disclaimer on first start. See [using-docker.md](using-docker.md)
> for CLI one-shots, API keys, keeping output and Tor.

## 3. Optional external tools

| Tool | Needed by | Setup |
|---|---|---|
| [Katana](https://github.com/projectdiscovery/katana) | all crawling: `crawler1/2/3`, the injection scanners when `PARAM` is empty, `csrf`, `pathtrav`, `CRAWL=y` in the info-disclosure modules | **Automatic.** The first crawl downloads the pinned release (v1.8.0) for your OS/CPU from GitHub, checks its SHA-256 against the value pinned in `core/methods/katana.py` and installs it in `tools/bin/` (git-ignored), or `~/.cache/tidos/bin/` if the checkout isn't writable. Offline or locked-down hosts: put the binary there yourself, or set `TIDOS_KATANA=/path/to/katana`; `TIDOS_NO_DOWNLOAD=1` turns the download off. Without Katana, scanners still work with `PARAM` set and the info-disclosure modules scan just the target page. |
| [phpsploit](https://github.com/nil0x42/phpsploit) | the `phpsploit` console command | Clone next to the TIDoS checkout (`../phpsploit/phpsploit`), or enter the path when asked. |

## 4. First launch

On the first console start TIDoS shows the disclaimer and asks you to accept it
(stored in `core/doc/choice`).

Check that everything loads:

```text
tid2 > list osint-passive
tid2 > vicadd https://target.example
tid2 > load whoischeckup
tid2(whoischeckup) > attack
```

## 5. Updating

```bash
cd tidos-framework        # or /opt/TIDoS for a global install (needs sudo)
git pull
.venv/bin/pip install -r requirements.txt
```

The console's `fetch` command checks for a newer release and can run the pull
for you.

## 6. Uninstalling

```bash
sudo rm -rf /opt/TIDoS /usr/bin/tidos     # global install
rm -rf tidos-framework                    # local checkout (includes .venv and tools/bin)
rm -rf ~/.cache/tidos                     # Katana, if it was installed there
```
