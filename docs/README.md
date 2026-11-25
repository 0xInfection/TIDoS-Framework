# TIDoS documentation

| Guide | Covers |
|---|---|
| [install.md](install.md) | System packages, local / global / Docker installs, optional tools, first launch, updating |
| [setup.md](setup.md) | API keys and environment variables, third-party services each module contacts, Tor, module options, automation, output locations |

Quick start:

```bash
git clone https://github.com/0xinfection/tidos-framework.git && cd tidos-framework
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
export TIDOS_SHODAN_API_KEY=...          # only the keys you need; see setup.md
sudo -E .venv/bin/python3 tidconsole.py
```
