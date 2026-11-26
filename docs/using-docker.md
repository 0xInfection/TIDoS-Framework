# Using TIDoS with Docker

A Debian-based image lets you run TIDoS without installing its system packages
or Python dependencies on the host. The `Dockerfile` lives at the repository
root and copies your local checkout (honouring `.dockerignore`), so the image
runs the code you have on disk.

- [Build the image](#build-the-image)
- [Run the console](#run-the-console)
- [Run modules non-interactively](#run-modules-non-interactively)
- [API keys](#api-keys)
- [Keeping output](#keeping-output)
- [Tor](#tor)
- [Notes](#notes)

## Build the image

```bash
cd tidos-framework
docker build -t tidos .
```

The build installs the system tools the modules shell out to (`nmap`,
`tcpdump`, `tor`, `dig`, `traceroute`, `ping`, build tools) and the Python
requirements into a virtualenv, then copies the framework to `/opt/TIDoS`.

## Run the console

Run interactively with a TTY so the console and its first-run disclaimer work:

```bash
docker run -it --rm tidos
```

The container's default user is root, which the console needs (several modules
open raw sockets). `--rm` removes the container on exit; drop it to keep state.

Drop to a shell instead of the console:

```bash
docker run -it --rm tidos bash
```

## Run modules non-interactively

The image's default command is the console, but you can pass CLI arguments
straight through. Modules are addressed by path, `<phase>[/<sub>]/<module>`:

```bash
docker run --rm tidos --list
docker run --rm tidos --info osint/passiverecon/getgeoip
docker run -it --rm tidos -u http://host -m osint/passiverecon/getgeoip
docker run -it --rm tidos -u http://host -m osint/all --tor
docker run -it --rm tidos -u http://host -m sqli --set PARAM=/p.php?id=1
```

Use `-it` for any run that produces live output you want to watch.

## API keys

TIDoS reads keys from the environment (see [setup.md](setup.md#api-keys)); the
image ships none. Pass the keys the run needs:

```bash
# single keys
docker run -it --rm -e TIDOS_SHODAN_API_KEY=... tidos -u http://host -m scan/shodan

# or a file of TIDOS_*=value lines
docker run -it --rm --env-file ~/.config/tidos/keys.env tidos
```

The `--env-file` format is the same one described in
[setup.md](setup.md#keeping-keys-in-a-file): one `TIDOS_NAME=value` per line.

## Keeping output

Findings and logs are written under `tmp/logs/<host>-logs/` inside the
container and vanish with it unless you mount a host directory there:

```bash
docker run -it --rm \
  -v "$PWD/out:/opt/TIDoS/tmp/logs" \
  tidos -u http://host -m osint/all
```

The session database (`core/database/tidos.db`) can be persisted the same way.

## Tor

The image includes `tor`, but no Tor service is started automatically. To route
HTTP through Tor (the `--tor` flag or the console's `tor on`), run a Tor client
reachable from the container on `127.0.0.1:9050` -- for example start it inside
the container shell, or share the host's Tor with `--network host` and a host
Tor daemon. Raw-socket modules never go through Tor; see
[setup.md](setup.md#tor).

## Notes

- Run interactively (`-it`) for the console and for any live output; the console
  shows the usage disclaimer on first start.
- The image copies your checkout, so rebuild (`docker build -t tidos .`) after
  changing code.
- For a host install instead, see [install.md](install.md).
