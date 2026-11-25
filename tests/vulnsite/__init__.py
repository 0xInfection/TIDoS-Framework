"""The deliberately-vulnerable test site.

A cluster of local HTTP(S) servers, each exposing endpoints crafted to be
detected by one group of TIDoS modules. Start it, point modules at the URLs
it reports, stop it:

    from tests.vulnsite import VulnSite
    with VulnSite() as site:
        print(site.url("sqli"))        # http://127.0.0.1:8771
        print(site.url("recon"))       # http://127.0.0.1:8775

Everything binds to 127.0.0.1 and serves fabricated data only; nothing is
ever really executed (shell/PHP/SQL behaviour is emulated).
"""
from __future__ import annotations

import socket
import subprocess
import tempfile
import threading
import time
from pathlib import Path

from . import _file_inject, _misconf, _recon, _sqli_xss, _web_inject

PORTS = {
    "sqli": 8771,      # SQLi / XSS
    "fileinj": 8772,   # LFI / RFI / PHPi / RCE / shellshock / struts / pathtrav
    "webinj": 8773,    # htmli / crlf / open-redirect / ldap / xpath / csrf
    "misconf": 8774,   # headers / clickjack / cookies / cors / hhi / sessionfix / trace
    "recon": 8775,     # info-disclosure + active recon
}
MISCONF_HTTPS = 18774  # hsts / sslcert / ssltlsscan
TELNET_PORT = 18775
SSH_PORT = 18776


def _wait(port, timeout=5.0):
    end = time.time() + timeout
    while time.time() < end:
        try:
            with socket.create_connection(("127.0.0.1", port), 0.3):
                return True
        except OSError:
            time.sleep(0.05)
    return False


def _gen_cert(directory: Path):
    """Self-signed cert via openssl; returns (certfile, keyfile) or None."""
    cert, key = directory / "cert.pem", directory / "key.pem"
    try:
        subprocess.run(
            ["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
             "-keyout", str(key), "-out", str(cert), "-days", "3",
             "-subj", "/CN=127.0.0.1",
             "-addext", "subjectAltName=IP:127.0.0.1"],
            capture_output=True, timeout=30, check=True)
        return str(cert), str(key)
    except (OSError, subprocess.SubprocessError):
        return None


class VulnSite:
    def __init__(self, host="127.0.0.1"):
        self.host = host
        self._servers = []
        self._tmp = None
        self.https_available = False

    def url(self, name: str) -> str:
        return f"http://{self.host}:{PORTS[name]}"

    @property
    def https_url(self) -> str:
        return f"https://{self.host}:{MISCONF_HTTPS}"

    def start(self):
        servers = [
            _sqli_xss.make_server(PORTS["sqli"]),
            _file_inject.make_server(PORTS["fileinj"]),
            _web_inject.make_server(PORTS["webinj"]),
            _misconf.make_http_server(PORTS["misconf"]),
            _recon.make_server(PORTS["recon"]),
        ]
        self._tmp = tempfile.TemporaryDirectory(prefix="vulnsite-")
        certpair = _gen_cert(Path(self._tmp.name))
        if certpair:
            try:
                servers.append(_misconf.make_https_server(MISCONF_HTTPS, *certpair))
                self.https_available = True
            except OSError:
                pass
        for srv in servers:
            threading.Thread(target=srv.serve_forever, daemon=True).start()
        self._servers = servers
        _misconf.start_banner_server(TELNET_PORT, _misconf.TELNET_BANNER)
        _misconf.start_banner_server(SSH_PORT, _misconf.SSH_BANNER)
        for port in list(PORTS.values()):
            if not _wait(port):
                raise RuntimeError(f"vulnsite server on port {port} did not come up")
        return self

    def stop(self):
        for srv in self._servers:
            try:
                srv.shutdown()
                srv.server_close()
            except Exception:
                pass
        self._servers = []
        if self._tmp:
            self._tmp.cleanup()
            self._tmp = None

    def __enter__(self):
        return self.start()

    def __exit__(self, *exc):
        self.stop()
