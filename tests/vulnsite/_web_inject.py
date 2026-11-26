#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Fixture for webinj modules: vulnerable and safe twins. Port 8773."""
import html
import re
import secrets
import sqlite3
from fnmatch import fnmatch
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlsplit

from lxml import etree

PORT = 8773
XML = etree.fromstring(b"<users><user><name>alice</name><role>admin</role></user>"
                       b"<user><name>bob</name><role>user</role></user></users>")
USERS = [{"uid": "alice", "objectClass": "person", "mail": "a@x"},
         {"uid": "bob", "objectClass": "person", "mail": "b@x"}]
DB = sqlite3.connect(":memory:", check_same_thread=False)
DB.execute("create table u(name text, role text)")
DB.executemany("insert into u values(?,?)", [("alice", "admin"), ("bob", "user")])
STATIC_TOKEN = "c2b6f0e1a9d84f7b8e3a5d1c0f9e2b7a"


def page(body, title="fixture"):
    return f"<html><head><title>{title}</title></head><body>{body}</body></html>"


def ldap_eval(value):
    """Mini LDAP filter evaluation of (&(uid=VALUE)(objectClass=person))."""
    flt = f"(&(uid={value})(objectClass=person))"
    if flt.count("(") != flt.count(")") or "\\" in value or "\x00" in value:
        raise ValueError("Bad search filter")
    conds = re.findall(r"\((\w+)=([^()]*)\)", flt)
    return [u for u in USERS if all(fnmatch(u.get(k, ""), v) for k, v in conds)]


def ldap_page(rows):
    return page("<ul>" + "".join(f"<li>{u['uid']} {u['mail']}</li>" for u in rows) + "</ul>"
                if rows else "<p>No such user.</p>" + "<p>Directory search help: use the exact uid.</p>")


def xpath_rows(value):
    return XML.xpath(f"//user[name/text()='{value}']")


def xpath_page(rows):
    return page("<ul>" + "".join(f"<li>{r.findtext('name')} is {r.findtext('role')}</li>" for r in rows) + "</ul>"
                if rows else "<p>No match.</p><p>Search the staff directory by exact name.</p>")


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def log_message(self, *a):
        pass

    def raw(self, status, headers, body=""):
        data = body.encode()
        out = f"HTTP/1.0 {status} X\r\n"
        for k, v in headers:
            out += f"{k}: {v}\r\n"
        out += f"Content-Length: {len(data)}\r\n\r\n"
        self.wfile.write(out.encode("latin-1", "replace") + data)

    def send(self, body, status=200, ctype="text/html", headers=()):
        self.raw(status, [("Content-Type", ctype), *headers], body)

    def redirect(self, loc, status=302):
        self.raw(status, [("Location", loc), ("Content-Type", "text/html")], "")

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        self.body = self.rfile.read(n).decode()
        self.do_GET()

    def do_GET(self):
        u = urlsplit(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query, keep_blank_values=True).items()}
        if getattr(self, "body", None):
            q.update({k: v[0] for k, v in parse_qs(self.body, keep_blank_values=True).items()})
        p = u.path
        v = lambda k: q.get(k, "")

        # ---------------- index (links for crawling) ----------------
        if p == "/":
            return self.send(page("<a href='/htmli/vuln?q=a'>x</a>"))

        if p in ("/csrf", "/csrf/"):
            return self.send(page("".join(f"<a href='/csrf/{n}'>{n}</a>" for n in
                                          ("vuln", "token", "entropy", "static", "samesite", "search", "meta"))))

        # ---------------- HTML injection ----------------
        if p == "/htmli/vuln":
            return self.send(page(f"<p>Results for {v('q')}</p>"))
        if p == "/htmli/attr":
            return self.send(page(f"<input name=q value=\"{v('q')}\">"))
        if p == "/htmli/post":
            return self.send(page(f"<form method=post><input name=comment></form><div>{v('comment')}</div>"))
        if p == "/htmli/safe":
            return self.send(page(f"<p>Results for {html.escape(v('q'))}</p>"))
        if p == "/htmli/textarea":
            val = re.sub(r"(?i)</textarea", "", v("q"))
            return self.send(page(f"<textarea>{val}</textarea>"))
        if p == "/htmli/comment":
            return self.send(page(f"<!-- debug: {v('q').replace('-->', '')} --><p>hi</p>"))
        if p == "/htmli/strip":
            return self.send(page(f"<p>{re.sub(r'<[^>]*>', '', v('q'))}</p>"))
        if p == "/htmli/json":
            return self.send(f'{{"q": "{v("q")}"}}', ctype="application/json")
        if p == "/htmli/attrsafe":
            return self.send(page(f"<input name=q value=\"{v('q').replace(chr(34), '&quot;')}\">"))

        # ---------------- CRLF ----------------
        if p == "/crlf/vuln":   # header injection in Location
            return self.raw(302, [("Location", "/home?lang=" + v("r"))], "")
        if p == "/crlf/lf":     # only bare LF works
            val = v("r").replace("\r", "")
            return self.raw(200, [("Content-Type", "text/html"), ("X-Lang", val)], page("ok"))
        if p == "/crlf/body":   # reflected in body only
            return self.send(page(f"<pre>{html.escape(v('r'))}</pre>"))
        if p == "/crlf/bodyraw":  # raw CRLF + header text in body
            return self.send(v("r"), ctype="text/plain")
        if p == "/crlf/safe":
            return self.raw(302, [("Location", "/home?lang=" + re.sub(r"[\r\n]", "", v("r")))], "")
        if p == "/crlf/encoded":
            from urllib.parse import quote
            return self.raw(302, [("Location", "/home?lang=" + quote(v("r")))], "")
        if p.startswith("/crlfpath/"):
            return self.raw(301, [("Location", unquote(p) + "/")], "")

        # ---------------- open redirect ----------------
        if p == "/redir/vuln":
            return self.redirect(v("next"))
        if p == "/redir/meta":
            return self.send(page(f"<meta http-equiv=\"refresh\" content=\"0; url={v('url')}\">"))
        if p == "/redir/js":
            return self.send(page(f"<script>window.location = \"{v('url')}\";</script>"))
        if p == "/redir/contains":  # weak check: must mention our host
            nxt = v("url")
            return self.redirect(nxt if "127.0.0.1" in nxt else "/")
        if p == "/redir/backslash":  # blocks // and http(s):// but not /\
            nxt = v("url")
            ok = nxt.startswith("/") and not nxt.startswith("//")
            return self.redirect(nxt if ok else "/")
        if p == "/redir/safe":
            nxt = v("next")
            ok = nxt.startswith("/") and not nxt.startswith(("//", "/\\")) and "\\" not in nxt
            return self.redirect(nxt if ok else "/")
        if p == "/redir/samehost":
            nxt = v("next")
            host = urlsplit(nxt.replace("\\", "/")).hostname
            return self.redirect(nxt if host in (None, "127.0.0.1") and not nxt.startswith(("//", "/\\", "\\")) and "@" not in nxt and ":" not in nxt.split("/")[0] else "/home")
        if p == "/redir/reflect":
            return self.send(page(f"<p>You came from {html.escape(v('next'))}</p><a href='/'>home</a>"))
        if p == "/redir/local":
            return self.redirect("/" + v("next").lstrip("/\\"))
        if p == "/redir/query":   # keeps evil in the query of a same-host URL
            return self.redirect("/landing?from=" + v("next"))
        if p == "/redir/jssafe":
            return self.send(page(f"<script>var from = \"{html.escape(v('url'))}\"; window.location = '/home';</script>"))
        if p == "/login":           # no params on the page: common-param fallback
            if "returnTo" in q:
                return self.redirect(q["returnTo"])
            return self.send(page("<p>Please log in</p>"))
        if p == "/logout":          # safe page for fallback
            return self.send(page("<p>Bye</p>"))

        # ---------------- LDAP ----------------
        if p in ("/ldap/vuln", "/ldap/blind"):
            try:
                return self.send(ldap_page(ldap_eval(v("user"))))
            except ValueError as e:
                if p == "/ldap/vuln":
                    return self.send(page(f"<pre>javax.naming.directory.InvalidSearchFilterException: {e}</pre>"), 500)
                return self.send(ldap_page([]))
        if p == "/ldap/static":
            return self.send(page("<p>Known issue: javax.naming.NameNotFoundException and 'Bad search filter' "
                                  "errors are logged during sync.</p>" + ldap_page([])))
        if p == "/ldap/safe":
            val = re.sub(r"[()*\\\x00]", lambda m: "\\%02x" % ord(m.group(0)), v("user"))
            rows = [u for u in USERS if u["uid"] == val]
            return self.send(ldap_page(rows))
        if p == "/ldap/search":   # supports * wildcard, escapes parentheses
            val = re.sub(r"[()\\]", "", v("user"))
            return self.send(ldap_page([u for u in USERS if fnmatch(u["uid"], val)]))
        if p == "/ldap/random":   # dynamic page, error text on errors only for some input
            return self.send(page(f"<p>{secrets.token_hex(8)}</p>" + ldap_page([u for u in USERS if u['uid'] == v('user')])))

        # ---------------- XPath ----------------
        if p in ("/xpath/vuln", "/xpath/blind"):
            try:
                return self.send(xpath_page(xpath_rows(v("name"))))
            except etree.XPathError as e:
                if p == "/xpath/vuln":
                    return self.send(page(f"<pre>System.Xml.XPath.XPathException: '{html.escape(v('name'))}' has an invalid token. ({e})</pre>"), 500)
                return self.send(xpath_page([]))
        if p == "/xpath/static":
            return self.send(page("<p>FAQ: if you see System.Xml.XPath.XPathException or XPathException, "
                                  "contact support.</p>" + xpath_page([])))
        if p == "/xpath/safe":
            return self.send(xpath_page(XML.xpath("//user[name/text()=$n]", n=v("name"))))
        if p == "/xpath/sqli":     # SQL injectable (boolean): must not be XPath
            try:
                rows = DB.execute(f"select name, role from u where name = '{v('name')}'").fetchall()
            except sqlite3.Error:
                rows = []
            return self.send(page("<ul>" + "".join(f"<li>{a} is {b}</li>" for a, b in rows) + "</ul>"
                                  if rows else "<p>No match.</p><p>Search the staff directory by exact name.</p>"))

        # ---------------- CSRF ----------------
        sid_hdr = ("Set-Cookie", f"PHPSESSID={secrets.token_hex(8)}; Path=/; HttpOnly")
        if p == "/csrf/vuln":
            return self.send(page("<form method=post action=/csrf/do><input name=email>"
                                  "<input type=submit value=Change></form>"), headers=[sid_hdr])
        if p == "/csrf/token":
            tok = secrets.token_urlsafe(24)
            return self.send(page(f"<form method=post action=/csrf/do><input type=hidden name=csrf_token value={tok}>"
                                  "<input name=email></form>"),
                             headers=[("Set-Cookie", f"session={secrets.token_hex(8)}; Path=/; SameSite=None; Secure")])
        if p == "/csrf/entropy":   # unnamed high-entropy hidden field
            tok = secrets.token_hex(20)
            return self.send(page(f"<form method=post action=/csrf/do><input type=hidden name=fx value={tok}>"
                                  "<input name=email></form>"), headers=[sid_hdr])
        if p == "/csrf/static":
            return self.send(page(f"<form method=post action=/csrf/do><input type=hidden name=authenticity_token "
                                  f"value={STATIC_TOKEN}><input name=email></form>"), headers=[sid_hdr])
        if p == "/csrf/samesite":
            return self.send(page("<form method=post action=/csrf/do><input name=email></form>"),
                             headers=[("Set-Cookie", f"sessionid={secrets.token_hex(8)}; Path=/; SameSite=Strict")])
        if p == "/csrf/search":
            return self.send(page("<form method=post action=/csrf/find><input name=q><input type=submit></form>"
                                  "<form action=/csrf/find><input name=term></form>"), headers=[sid_hdr])
        if p == "/csrf/meta":
            return self.send(page("<meta name=csrf-token content=abcdef0123456789abcdef>"
                                  "<form method=post action=/csrf/do><input name=email></form>"), headers=[sid_hdr])

        return self.send(page("not found"), 404)


def make_server(port):
    ThreadingHTTPServer.daemon_threads = True
    return ThreadingHTTPServer(("127.0.0.1", port), H)


if __name__ == "__main__":
    make_server(PORT).serve_forever()
