# Installing TIDoS

TIDoS runs on **Linux** with **Python 3.7+**. The console must run as **root**,
because several modules open raw sockets (port scans, ARP, traceroute). The Qt5
GUI runs as a normal user.

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
| `konsole` | optional; only needed by the GUI |

Python packages worth knowing about: `scapy` powers the raw scanners and
`arpscan`. `sslyze` powers `ssltlsscan`; current sslyze releases need
**Python 3.9+**, and on 3.7/3.8 the module falls back to a basic stdlib
protocol check. `PySocks` is required for `tor on`. `paramiko` and `PyMySQL`
power `sshbrute` and `sqlbrute`; without them those two modules say so and stop.
`Pillow` powers the `imgext` (aid) EXIF/GPS reader; without it the module says so
and stops.

If a tool is missing, the module that needs it stops and says so. The rest of
the framework keeps working.

## 2. Install TIDoS

### Option A: local checkout (recommended)

Recent Debian and Ubuntu releases block `pip install` into the system Python
(PEP 668, "externally-managed-environment"). A virtual environment avoids that:

```bash
git clone https://github.com/0xinfection/tidos-framework.git
cd tidos-framework
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Run the console as root with the venv's interpreter. `-E` keeps your exported
API keys, because sudo drops the environment by default:

```bash
sudo -E .venv/bin/python3 tidconsole.py
```

Run the GUI as your normal user:

```bash
.venv/bin/python3 tidv2
```

> Always launch from the repository root. TIDoS reads `core/doc/*` and writes
> `tmp/logs/` relative to the current directory.

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
tidos -v http://target -l dig
tidos --app                  # GUI, runs as you
```

The launcher passes every `TIDOS_*` environment variable through `sudo`. Export
keys with the `TIDOS_` prefix and they reach the console without any extra
flags (see [setup.md](setup.md#api-keys)).

> The installer runs `pip3 install` against the system Python. On distributions
> that enforce PEP 668 this step fails. Either use Option A, or install the
> requirements yourself first (for example into a venv you point `python3` at).

### Option C: Docker

```bash
cd tidos-framework/core/docker
docker build -t tidos .
docker run -it --rm --env-file ~/.config/tidos/keys.env tidos bash
tidos
```

`--env-file` takes the same `TIDOS_*=value` lines described in
[setup.md](setup.md#keeping-keys-in-a-file); you can also pass single keys with
`-e TIDOS_SHODAN_API_KEY=...`.

> The Dockerfile clones the upstream repository from GitHub. It does not copy
> your local checkout, so local changes only show up in the image once they are
> pushed. The `vainlystrain/tidos-framework` image on Docker Hub predates this
> version.

## 3. Optional external tools

| Tool | Needed by | Setup |
|---|---|---|
| [Katana](https://github.com/projectdiscovery/katana) | all crawling: `crawler1/2/3`, the injection scanners when `PARAM` is empty, `csrf`, `pathtrav_legacy`, `CRAWL=y` in the info-disclosure modules | **Automatic.** The first crawl downloads the pinned release (v1.8.0) for your OS/CPU from GitHub, checks its SHA-256 against the value pinned in `core/methods/katana.py` and installs it in `tools/bin/` (git-ignored), or `~/.cache/tidos/bin/` if the checkout isn't writable. Offline or locked-down hosts: put the binary there yourself, or set `TIDOS_KATANA=/path/to/katana`; `TIDOS_NO_DOWNLOAD=1` turns the download off. Without Katana, scanners still work with `PARAM` set and the info-disclosure modules scan just the target page. |
| [Vailyn](https://github.com/VainlyStrain/Vailyn) | `pathtrav` (path traversal) | Install per its README. TIDoS asks for the install directory on first launch and stores it in `core/doc/vailyn`. Without Vailyn, use the built-in `lfi` (parameters) and `pathtrav_legacy` (URL path). |
| [phpsploit](https://github.com/nil0x42/phpsploit) | the `phpsploit` console command | Clone next to the TIDoS checkout (`../phpsploit/phpsploit`), or enter the path when asked. |

## 4. First launch

On the first console start TIDoS:

1. shows the disclaimer and asks you to accept it (stored in `core/doc/choice`);
2. asks for your **unprivileged user name**, which the GUI uses to avoid
   root-owned files (stored in `core/doc/local`);
3. asks for the **Vailyn directory**; leave it empty if you don't use
   `pathtrav` (stored in `core/doc/vailyn`).

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
