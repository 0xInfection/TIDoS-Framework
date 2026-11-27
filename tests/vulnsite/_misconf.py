#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""Misconfiguration fixture: HTTP :8774, HTTPS :18774, telnet :18775, ssh-like :18776."""
import re
import secrets
import socket
import ssl
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, parse_qs

HERE = sys.path[0]
SESSIONS = set()
HTML = "<html><head><title>Fixture {t}</title></head><body>{b}</body></html>"


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "fixture"
    sys_version = ""

    def log_message(self, *a):
        pass

    def send(self, code=200, body="", headers=(), ctype="text/html"):
        data = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        for k, v in headers:
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(data)

    def page(self, t="page", b="hello", headers=(), code=200):
        self.send(code, HTML.format(t=t, b=b), headers)

    def do_GET(self):
        u = urlsplit(self.path)
        p = u.path
        q = parse_qs(u.query)
        origin = self.headers.get("Origin")
        host = self.headers.get("Host", "")
        cookie = self.headers.get("Cookie", "")
        hp = [("Server", "nginx")]
        # ---------------- headers
        if p.startswith("/hdr/bad"):
            return self.page(headers=[("Server", "Apache/2.4.1 (Unix)"), ("X-Powered-By", "PHP/7.4.3"),
                                      ("Content-Security-Policy", "script-src 'self' 'unsafe-inline' 'unsafe-eval' *"),
                                      ("X-XSS-Protection", "1; mode=block"), ("X-Debug-Token", "abc123"),
                                      ("Referrer-Policy", "unsafe-url")])
        if p.startswith("/hdr/good"):
            return self.page(headers=hp + [
                ("Content-Security-Policy", "default-src 'self'; script-src 'self' 'nonce-r4nd'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"),
                ("X-Content-Type-Options", "nosniff"), ("Referrer-Policy", "strict-origin-when-cross-origin"),
                ("Permissions-Policy", "geolocation=()"), ("Cross-Origin-Opener-Policy", "same-origin"),
                ("Cross-Origin-Resource-Policy", "same-origin")])
        # ---------------- clickjacking
        cj = {"/cj/none": [], "/cj/allowfrom": [("X-Frame-Options", "ALLOW-FROM https://x.com")],
              "/cj/fastar": [("Content-Security-Policy", "frame-ancestors *")],
              "/cj/ro": [("Content-Security-Policy-Report-Only", "frame-ancestors 'none'")],
              "/cj/deny": [("X-Frame-Options", "DENY")],
              "/cj/fa": [("Content-Security-Policy", "default-src 'self'; frame-ancestors 'self'"),
                         ("X-Frame-Options", "ALLOW-FROM https://x.com")],
              "/cj/conflict": [("X-Frame-Options", "DENY"), ("X-Frame-Options", "SAMEORIGIN")]}
        for k, v in cj.items():
            if p.rstrip("/") == k:
                return self.page(headers=v)
        if p.startswith("/cj/json"):
            return self.send(200, '{"a":1}', ctype="application/json")
        # ---------------- cookies
        if p.startswith("/ck/bad"):
            return self.page(headers=[("Set-Cookie", "PHPSESSID=abc123; path=/"),
                                      ("Set-Cookie", "theme=dark; Expires=Wed, 21 Oct 2037 07:28:00 GMT; path=/"),
                                      ("Set-Cookie", "auth=1; SameSite=None; HttpOnly")])
        if p.startswith("/ck/good"):
            return self.page(headers=[("Set-Cookie", "__Host-sess=abc; Secure; HttpOnly; SameSite=Lax; Path=/"),
                                      ("Set-Cookie", "csrftoken=x; Secure; SameSite=Strict; Path=/"),
                                      ("Set-Cookie", "old=; Max-Age=0; Path=/")])
        if p.startswith("/ck/redir"):
            return self.send(302, "", [("Location", "/ck/good"), ("Set-Cookie", "sessionid=zz; Path=/")])
        # ---------------- CORS
        if p.startswith("/cors/"):
            mode = p.split("/")[2]
            h = []
            me = host.split(":")[0]
            allow = None
            creds = True
            if mode == "reflectcreds" and origin:
                allow = origin
            elif mode == "reflect" and origin:
                allow, creds = origin, False
            elif mode == "null" and origin == "null":
                allow = origin
            elif mode == "prefix" and origin and origin.startswith("https://" + me):
                allow = origin
            elif mode == "suffix" and origin and origin.endswith(me):
                allow = origin
            elif mode == "dot" and origin and re.match(r"^https?://" + me + "$", origin):
                allow = origin
            elif mode == "http" and origin in ("https://" + me, "http://" + me):
                allow = origin
            elif mode == "static":
                allow = "https://trusted.example"
            elif mode == "star":
                allow, creds = "*", False
            elif mode == "exact" and origin == "https://app." + me:
                allow = origin
            if allow:
                h.append(("Access-Control-Allow-Origin", allow))
                if creds:
                    h.append(("Access-Control-Allow-Credentials", "true"))
                h.append(("Vary", "Origin"))
            return self.send(200, '{"secret": 1}', h, "application/json")
        # ---------------- host header injection
        if p.startswith("/hhi/redirect"):
            return self.send(302, "", [("Location", f"http://{host}/login")])
        if p.startswith("/hhi/link"):
            return self.page(b=f'<a href="http://{host}/reset?t=1">reset</a>')
        if p.startswith("/hhi/xfh"):
            h2 = self.headers.get("X-Forwarded-Host") or host
            return self.page(b=f'<script src="//{h2}/app.js"></script>')
        if p.startswith("/hhi/safe"):
            return self.page(b='<a href="/reset">reset</a> <a href="http://127.0.0.1:8774/x">abs</a>')
        if p.startswith("/hhi/error"):
            if not host.startswith(("127.0.0.1", "localhost")):
                return self.page("err", f"Unknown virtual host {host}", code=400)
            return self.page(b='<a href="/x">x</a>')
        # ---------------- session fixation
        if p.startswith("/sf/vuln"):
            if "SESSID=" in cookie:
                return self.page(b="welcome back")
            return self.page(headers=[("Set-Cookie", f"SESSID={secrets.token_hex(16)}; Path=/; HttpOnly")])
        if p.startswith("/sf/url"):
            sid = q.get("SESSID", [None])[0]
            m = re.search(r"SESSID=([0-9a-f]+)", cookie)
            if sid:
                return self.page(headers=[("Set-Cookie", f"SESSID={sid}; Path=/")])
            if m and m.group(1) in SESSIONS:
                return self.page()
            new = secrets.token_hex(16)
            SESSIONS.add(new)
            return self.page(headers=[("Set-Cookie", f"SESSID={new}; Path=/")])
        if p.startswith("/sf/safe"):
            m = re.search(r"SESSID=([0-9a-f]+)", cookie)
            if m and m.group(1) in SESSIONS:
                return self.page()
            new = secrets.token_hex(16)
            SESSIONS.add(new)
            return self.page(headers=[("Set-Cookie", f"SESSID={new}; Path=/")])
        if p.startswith("/sf/none"):
            return self.page()
        # ---------------- HSTS (HTTPS server)
        if p.startswith("/hsts/good"):
            return self.page(headers=[("Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload")])
        if p.startswith("/hsts/short"):
            return self.page(headers=[("Strict-Transport-Security", "max-age=300")])
        if p.startswith("/hsts/zero"):
            return self.page(headers=[("Strict-Transport-Security", "max-age=0")])
        if p.startswith("/hsts/none"):
            return self.page()
        return self.page()

    def trace(self):
        p = self.path
        if p.startswith("/trace/on"):
            raw = f"{self.command} {self.path} {self.request_version}\r\n" + str(self.headers)
            return self.send(200, raw, ctype="message/http")
        if p.startswith("/trace/fake"):
            return self.send(200, "<html>TRACE is not echoed</html>")
        return self.send(405, "Method Not Allowed", [("Allow", "GET")])

    do_TRACE = trace
    do_TRACK = trace


def telnet_server(port, payload):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", port))
    s.listen(5)
    while True:
        c, _ = s.accept()
        try:
            c.sendall(payload)
            c.settimeout(2)
            try:
                c.recv(100)
            except OSError:
                pass
        finally:
            c.close()


TELNET_BANNER = b"\xff\xfd\x18\xff\xfd\x20\xff\xfb\x01Ubuntu 22.04\r\nlogin: "
SSH_BANNER = b"SSH-2.0-OpenSSH_9.0\r\n"


def make_http_server(port):
    ThreadingHTTPServer.daemon_threads = True
    return ThreadingHTTPServer(("127.0.0.1", port), H)


def make_https_server(port, certfile, keyfile):
    ThreadingHTTPServer.daemon_threads = True
    tls = ThreadingHTTPServer(("127.0.0.1", port), H)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(certfile, keyfile)
    tls.socket = ctx.wrap_socket(tls.socket, server_side=True)
    return tls


def start_banner_server(port, payload):
    """Run a raw TCP banner server (telnet/ssh) in a daemon thread."""
    threading.Thread(target=telnet_server, args=(port, payload), daemon=True).start()


if __name__ == "__main__":
    start_banner_server(18775, TELNET_BANNER)
    start_banner_server(18776, SSH_BANNER)
    make_http_server(8774).serve_forever()
