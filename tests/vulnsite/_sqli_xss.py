"""SQLi/XSS fixture on 127.0.0.1:8771. Vulnerable endpoints run real (sqlite) SQL built by
string concatenation; SLEEP(n) is registered as a sqlite function to mimic MySQL."""
import html
import json
import random
import sqlite3
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

PORT = 8771
ROWS = [(1, "alice", "Alice likes apples and long walks on the beach."),
        (2, "bob", "Bob builds bridges out of balsa wood."),
        (3, "carol", "Carol collects copper coins from Corinth.")]


def db():
    c = sqlite3.connect(":memory:")
    c.create_function("SLEEP", 1, lambda n: time.sleep(float(n)) or 0)
    c.execute("create table users(id integer primary key, name text, bio text)")
    c.executemany("insert into users values (?,?,?)", ROWS)
    return c


MYSQL_ERR = ("<b>Warning</b>: You have an error in your SQL syntax; check the manual that corresponds to "
             "your MySQL server version for the right syntax to use near '{}' at line 1")
PG_ERR = "ERROR:  unterminated quoted string at or near \"{}\"\nLINE 1: SELECT"

PAGE = "<html><head><title>Fixture</title></head><body><h1>Directory</h1>{}<footer>(c) fixture</footer></body></html>"


def rows_html(rows):
    return "".join(f"<div class=row><b>{html.escape(r[1])}</b><p>{html.escape(r[2])}</p></div>" for r in rows) or "<p>No results.</p>"


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def log_message(self, *a):
        pass

    def send(self, body, ctype="text/html", status=200, headers=()):
        b = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        for k, v in headers:
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(b)

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        form = parse_qs(self.rfile.read(n).decode(), keep_blank_values=True)
        self.route(urlsplit(self.path).path, {k: v[0] for k, v in form.items()})

    def do_GET(self):
        u = urlsplit(self.path)
        self.route(u.path, {k: v[0] for k, v in parse_qs(u.query, keep_blank_values=True).items()})

    def route(self, path, q):
        g = q.get
        c = db()
        try:
            # ---------------- SQLi, vulnerable ----------------
            if path == "/sql/err":       # numeric, MySQL-style error shown
                try:
                    rows = c.execute(f"select * from users where id={g('id', '1')}").fetchall()
                    return self.send(PAGE.format(rows_html(rows)))
                except sqlite3.Error:
                    return self.send(PAGE.format(MYSQL_ERR.format(html.escape(g('id', '')))), status=500)
            if path == "/sql/errstr":    # string, PostgreSQL-style error
                try:
                    rows = c.execute(f"select * from users where name='{g('name', 'alice')}'").fetchall()
                    return self.send(PAGE.format(rows_html(rows)))
                except sqlite3.Error:
                    return self.send(PAGE.format(html.escape(PG_ERR.format(g('name', '')))))
            if path == "/sql/bool":      # numeric, errors swallowed
                try:
                    rows = c.execute(f"select * from users where id={g('id', '1')}").fetchall()
                except sqlite3.Error:
                    rows = []
                return self.send(PAGE.format(rows_html(rows)))
            if path == "/sql/boolstr":   # string, errors swallowed, input echoed
                try:
                    rows = c.execute(f"select * from users where name='{g('q', 'bob')}'").fetchall()
                except sqlite3.Error:
                    rows = []
                return self.send(PAGE.format(f"<p>Search: {html.escape(g('q', ''))}</p>" + rows_html(rows)))
            if path == "/sql/time":      # constant output, only timing leaks
                try:
                    c.execute(f"select * from users where id={g('id', '1')}").fetchall()
                except sqlite3.Error:
                    pass
                return self.send(PAGE.format("<p>Thanks, your request was logged.</p>"))
            if path == "/sql/login":     # POST string context
                try:
                    rows = c.execute(f"select * from users where name='{g('user', '')}' and id>0").fetchall()
                except sqlite3.Error:
                    rows = []
                return self.send(PAGE.format("<p>Welcome back!</p>" if rows else "<p>Invalid login.</p>"))
            # ---------------- SQLi, safe ----------------
            if path == "/sql/safe":      # parameterised, echoes input
                rows = c.execute("select * from users where id=?", (g('id', '1'),)).fetchall()
                return self.send(PAGE.format(f"<p>id: {html.escape(g('id', ''))}</p>" + rows_html(rows)))
            if path == "/sql/staticerr":  # scary error always present
                rows = c.execute("select * from users where id=?", (g('id', '1'),)).fetchall()
                return self.send(PAGE.format(MYSQL_ERR.format("x") + rows_html(rows)))
            if path == "/sql/random":    # random content on every request
                junk = "".join(f"<li>{random.random()} {random.choice(['news','sport','tech','art'])}</li>"
                               for _ in range(random.randint(3, 12)))
                return self.send(PAGE.format(f"<ul>{junk}</ul><p>{html.escape(g('id', ''))}</p>"))
            if path == "/sql/intcheck":  # validates integer, error page otherwise
                v = g('id', '1')
                if not v.isdigit():
                    return self.send(PAGE.format("<p>Invalid id: must be numeric. SQL injection attempts are logged.</p>"), status=400)
                rows = c.execute("select * from users where id=?", (int(v),)).fetchall()
                return self.send(PAGE.format(rows_html(rows)))
            if path == "/sql/slow":      # always slow
                time.sleep(2.5)
                return self.send(PAGE.format("<p>slow report</p>"))
            if path == "/sql/jitter":    # randomly slow
                time.sleep(random.choice([0, 0, 0, 3.5]))
                return self.send(PAGE.format("<p>jittery</p>"))
            if path == "/sql/echoerr":   # echoes input raw inside an error-ish message
                return self.send(PAGE.format(f"<p>Database lookup for {g('id', '')} returned nothing.</p>"))
            if path == "/sql/len":       # output depends on input length only (not SQL)
                return self.send(PAGE.format("<p>" + ("short" if len(g('id', '')) < 6 else "Input too long, rejected.") + "</p>"))

            # ---------------- XSS, vulnerable ----------------
            v = g('q', 'hello')
            if path == "/x/html":
                return self.send(PAGE.format(f"<p>Results for {v}</p>"))
            if path == "/x/attrdq":
                return self.send(PAGE.format(f'<form><input type="text" name="q" value="{v}"></form>'))
            if path == "/x/attrsq":
                return self.send(PAGE.format(f"<form><input type='text' name='q' value='{v}'></form>"))
            if path == "/x/attrnq":
                return self.send(PAGE.format(f"<form><input type=text name=q value={v}></form>"))
            if path == "/x/attrdq-noangle":  # < > encoded, quotes not
                return self.send(PAGE.format(f'<input name="q" value="{v.replace("<", "&lt;").replace(">", "&gt;")}">'))
            if path == "/x/scriptdq":
                return self.send(PAGE.format(f'<script>var s = "{v}"; console.log(s);</script>'))
            if path == "/x/scriptsq":
                return self.send(PAGE.format(f"<script>var s = '{v.replace(chr(60), '')}';</script>"))  # strips <
            if path == "/x/scriptcode":
                return self.send(PAGE.format(f"<script>var n = {v};</script>"))
            if path == "/x/comment":
                return self.send(PAGE.format(f"<!-- debug: {v} --><p>ok</p>"))
            if path == "/x/textarea":
                return self.send(PAGE.format(f"<textarea name=q>{v}</textarea>"))
            if path == "/x/href":
                return self.send(PAGE.format(f'<a href="{html.escape(v)}">link</a>'))  # escaped but URL ctx
            if path == "/x/post":
                return self.send(PAGE.format(f"<p>Thanks {v}</p>"))
            if path == "/x/ua":
                ua = self.headers.get("User-Agent", "")
                return self.send(PAGE.format(f"<p>Your browser: {ua}</p>"))
            if path == "/x/cookie":
                pref = ""
                for part in (self.headers.get("Cookie") or "").split(";"):
                    k, _, val = part.strip().partition("=")
                    if k == "theme":
                        pref = val
                return self.send(PAGE.format(f"<p>Theme: {pref or 'light'}</p>"), headers=[("Set-Cookie", "theme=light")])
            # ---------------- XSS, safe ----------------
            if path == "/x/enc":
                return self.send(PAGE.format(f"<p>Results for {html.escape(v)}</p>"))
            if path == "/x/encattr":
                return self.send(PAGE.format(f'<input name="q" value="{html.escape(v)}">'))
            if path == "/x/encattrsq":
                return self.send(PAGE.format(f"<input name='q' value='{html.escape(v)}'>"))
            if path == "/x/attr-ltonly":  # quotes encoded, < > raw -> not exploitable inside "..."
                return self.send(PAGE.format(f'<input name="q" value="{v.replace(chr(34), "&quot;")}">'))
            if path == "/x/scriptsafe":
                return self.send(PAGE.format(f"<script>var s = {json.dumps(v).replace('<', chr(92) + 'u003c')};</script>"))
            if path == "/x/commentsafe":
                return self.send(PAGE.format(f"<!-- debug: {html.escape(v).replace('--', '')} --><p>ok</p>"))
            if path == "/x/textareasafe":
                return self.send(PAGE.format(f"<textarea>{html.escape(v)}</textarea>"))
            if path == "/x/json":
                return self.send(json.dumps({"q": v}), ctype="application/json")
            if path == "/x/plain":
                return self.send(f"you said {v}", ctype="text/plain")
            if path == "/x/stripped":   # removes tags and quotes entirely
                import re
                return self.send(PAGE.format(f'<p>{re.sub(r"[<>\"\']", "", v)}</p><input value="{re.sub(r"[<>\"\']", "", v)}">'))
            if path == "/x/uasafe":
                return self.send(PAGE.format(f"<p>Your browser: {html.escape(self.headers.get('User-Agent', ''))}</p>"))
            if path == "/":
                links = "".join(f'<a href="{p}">{p}</a> ' for p in LINKS)
                form = '<form method=post action="/sql/login"><input name=user><input type=password name=pw></form>'
                form2 = '<form method=post action="/x/post"><input name=q></form>'
                return self.send(PAGE.format(links + form + form2))
            return self.send("not found", "text/plain", 404)
        finally:
            c.close()


LINKS = ["/sql/err?id=1", "/sql/errstr?name=alice", "/sql/bool?id=1", "/sql/boolstr?q=bob", "/sql/time?id=1",
         "/sql/safe?id=1", "/sql/staticerr?id=1", "/sql/random?id=1", "/sql/intcheck?id=1", "/sql/echoerr?id=1",
         "/sql/len?id=1"]

def make_server(port):
    ThreadingHTTPServer.daemon_threads = True
    return ThreadingHTTPServer(("127.0.0.1", port), H)


if __name__ == "__main__":
    make_server(PORT).serve_forever()
