#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Recon & information-disclosure fixture.

Covers the active-recon modules (server-status, WebDAV, HTTP methods, source
comments, robots/phpinfo) and the information-disclosure modules (emails,
credit cards, SSNs, phone numbers, internal IPs, secrets, error messages).
Content is crafted to match the framework's own signatures; a /clean page
carries none of it so the modules can be checked for false positives too.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# --- leak payloads, each crafted to match one module's signatures -----------
EMAILS = "Reach us at admin@corp-internal.net or security@corp-internal.net for help."
CARDS = "Saved Visa card on file: 4111111111111111 (expires 05/27)."
SSNS = "Employee record SSN: 123-45-6789 on file."
PHONES = "Support hotline: +1-202-555-0143, or +44 20 7946 0958."
INTERNAL_IPS = "Upstream backend at 10.10.14.22 and cache 192.168.1.50; db 172.16.0.9."
SECRETS = (
    "aws_access_key_id = AKIAZ2XICF7G5KQ9WPLM\n"
    "github_token = ghp_A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8\n"
    'db_password = "S3cr3tP4ssw0rd"\n'
    "-----BEGIN RSA PRIVATE KEY-----\nMIIEvQ...snip...\n-----END RSA PRIVATE KEY-----\n"
)
PHP_ERROR = ("<b>Fatal error</b>: Uncaught Error: Call to undefined function render() "
             "in <b>/var/www/html/index.php</b> on line <b>42</b>")

COMMENTS = ("<!-- TODO: remove before release, admin creds are admin/admin -->"
            "<!-- debug build 42, internal api at 10.0.0.5 -->")

PHPINFO = ("<title>phpinfo()</title><h1 class=p>PHP Version 7.4.3</h1>"
           "<table><tr><td>System</td><td>Linux web01</td></tr>"
           "<tr><td>Loaded Configuration File</td><td>/etc/php/7.4/php.ini</td></tr></table>")

ROBOTS = "User-agent: *\nDisallow: /admin/\nDisallow: /backup/\nSitemap: /sitemap.xml\n"

LINKS = ["/leak/emails", "/leak/cards", "/leak/ssn", "/leak/phone", "/leak/internalip",
         "/leak/secrets", "/leak/error", "/comments", "/phpinfo", "/clean"]


def doc(title, body):
    return f"<html><head><title>{title}</title></head><body>{body}</body></html>"


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "Apache/2.4.7"
    sys_version = "(Unix) PHP/7.4.3"

    def log_message(self, *a):
        pass

    def out(self, body, code=200, ctype="text/html", headers=()):
        data = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        for k, v in headers:
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(data)

    def do_GET(self):
        p = self.path.split("?")[0]
        pages = {
            "/leak/emails": doc("Contact", f"<p>{EMAILS}</p>"),
            "/leak/cards": doc("Billing", f"<p>{CARDS}</p>"),
            "/leak/ssn": doc("HR", f"<p>{SSNS}</p>"),
            "/leak/phone": doc("Support", f"<p>{PHONES}</p>"),
            "/leak/internalip": doc("Ops", f"<pre>{INTERNAL_IPS}</pre>"),
            "/leak/secrets": doc("Config", f"<pre>{SECRETS}</pre>"),
            "/leak/error": doc("Error", PHP_ERROR),
            "/comments": doc("Home", f"{COMMENTS}<p>Welcome.</p>"),
            "/phpinfo": doc("phpinfo", PHPINFO),
            "/info.php": doc("phpinfo", PHPINFO),
            "/clean": doc("Clean", "<p>Nothing sensitive here. Just marketing copy.</p>"),
        }
        if p == "/":
            links = " ".join(f'<a href="{l}">{l}</a>' for l in LINKS)
            ext = '<a href="https://external.example.org/x">ext</a>'
            form = '<form method=post action="/submit"><input name=q></form>'
            return self.out(doc("Index", links + ext + form))
        if p == "/robots.txt":
            return self.out(ROBOTS, ctype="text/plain")
        if p == "/server-status":
            return self.out(doc("Apache Status", "Apache Server Status for web01<br>"
                                "Total accesses: 12345 - Total Traffic: 1.2 GB"))
        if p == "/server-info":
            return self.out("forbidden", code=403)
        if p in pages:
            return self.out(pages[p])
        return self.out(doc("404", "<h1>Oops, nothing here</h1><a href='/'>home</a>"), code=404)

    def do_OPTIONS(self):
        self.out("", headers=[("Allow", "GET, POST, OPTIONS, HEAD, PUT, DELETE, PROPFIND")])

    def _drain(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n:
            self.rfile.read(n)

    def do_POST(self):
        self._drain()
        self.out(doc("Thanks", "<p>received</p>"))

    def do_PROPFIND(self):
        self._drain()
        self.out('<?xml version="1.0"?><D:multistatus xmlns:D="DAV:"><D:response>'
                 '<D:href>/</D:href></D:response></D:multistatus>', code=207, ctype="application/xml")


def make_server(port):
    ThreadingHTTPServer.daemon_threads = True
    return ThreadingHTTPServer(("127.0.0.1", port), H)


if __name__ == "__main__":
    import sys
    make_server(int(sys.argv[1]) if len(sys.argv) > 1 else 8775).serve_forever()
