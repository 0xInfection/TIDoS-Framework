"""Fixture for lfi / rfi / pathtrav_legacy / phpi / rce / shellshock / strutsshock.

Host 127.0.0.1 -> vulnerable CGI set, Host localhost -> safe CGI set.
Nothing is ever executed: shell / PHP / OGNL behaviour is emulated with regexes.
"""
import base64
import html
import posixpath
import random
import re
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlsplit

PORT = 8772
PASSWD = "root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\nwww-data:x:33:33::/var/www:/usr/sbin/nologin\n"
WININI = "; for 16-bit app support\n[fonts]\n[extensions]\n[mci extensions]\n[files]\n[Mail]\nMAPI=1\n"
ENVIRON = "PATH=/usr/local/bin:/usr/bin\x00HOSTNAME=web01\x00HOME=/var/www\x00"
FS = {
    "/etc/passwd": PASSWD,
    "/proc/self/environ": ENVIRON,
    "/var/www/html/pages/about.php": "<?php echo 'About us'; ?>\n",
    "/var/www/html/pages/home.php": "<?php echo 'Welcome home'; ?>\n",
    "/var/www/html/pages/about": "About us\n",
    "/var/www/static/logo.txt": "LOGO\n",
    "/var/www/static/app.css": "body{}\n",
}
CHROOT_FS = {k: v for k, v in FS.items() if k != "/etc/passwd"}
WINFS = {"c:/windows/win.ini": WININI, "c:/inetpub/wwwroot/pages/about.txt": "About\n"}
REMOTE = "Remote include file. TIDREMOTE-q8z3 marker.\n"


def page(body, title="fixture"):
    return f"<html><head><title>{title}</title></head><body>{body}</body></html>"


def resolve(base, value, fs):
    value = value.split("\x00")[0]
    if value.startswith("file://"):
        value = value[7:]
    path = value if value.startswith("/") else posixpath.join(base, value)
    return fs.get(posixpath.normpath(path))


# --- emulators -------------------------------------------------------------
def sh(cmdline, windows=False, output=True):
    out = []
    if windows:
        for a, b in re.findall(r"set /a (\d+)\*(\d+)", cmdline):
            out.append(str(int(a) * int(b)))
        for n in re.findall(r"ping -n (\d+) 127\.0\.0\.1", cmdline):
            time.sleep(int(n) - 1)
    else:
        for w, a, b in re.findall(r"echo (\w*)\$\(\((\d+)\*(\d+)\)\)", cmdline):
            out.append(f"{w}{int(a) * int(b)}")
        # plain `echo <token>` (e.g. the Shellshock canary): reflect the token
        for tok in re.findall(r"echo ([A-Za-z][\w-]*)(?![\w$(])", cmdline):
            out.append(tok)
        for x, y in re.findall(r"printf %s%s (\w+) (\w+)", cmdline):
            out.append(x + y)
        for n in re.findall(r"sleep (\d+)", cmdline):
            time.sleep(int(n))
    return "\n".join(out) if output else ""


def php(code, output=True):
    out = []
    for a, b in re.findall(r"print\((\d+)\*(\d+)\)", code):
        out.append(str(int(a) * int(b)))
    for n in re.findall(r"print\(strrev\((\d+)\)\)", code):
        out.append(n[::-1])
    for n in re.findall(r"(?<!u)sleep\((\d+)\)", code):
        time.sleep(int(n))
    for n in re.findall(r"usleep\((\d+)\)", code):
        time.sleep(int(n) / 1e6)
    return "".join(out) if output else ""


def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as e:
        return f"<!-- fetch failed: {type(e).__name__} -->"


def include_remote(v):
    if v.startswith("data://text/plain;base64,"):
        try:
            return php(base64.b64decode(v.split(",", 1)[1]).decode())
        except Exception:
            return "Warning: data decode failed"
    if v.startswith(("http://", "https://")):
        return fetch(v)
    return None


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def log_message(self, *a):
        pass

    def send(self, code, body, ctype="text/html", headers=None):
        data = body.encode("utf-8", "surrogateescape") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        self.body = self.rfile.read(n).decode("latin-1")
        self.do_GET()

    def do_GET(self):
        u = urlsplit(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query, keep_blank_values=True).items()}
        if getattr(self, "body", None):
            q.update({k: v[0] for k, v in parse_qs(self.body, keep_blank_values=True).items()})
        p = u.path
        host = (self.headers.get("Host") or "").split(":")[0]
        v = q.get("file", q.get("page", q.get("code", q.get("name", q.get("host", q.get("expr", ""))))))
        try:
            return self.route(p, q, v, host)
        except BrokenPipeError:
            pass

    def route(self, p, q, v, host):
        # ---------------- index (for crawling) ----------------
        if p == "/":
            links = ["/static/logo.txt", "/files/readme.txt", "/docs/intro.txt", "/assets/app.css",
                     "/lfi/read?file=about.php", "/rce/echo?host=127.0.0.1"]
            return self.send(200, page("".join(f'<a href="{l}">{l}</a><br>' for l in links)))

        # ---------------- LFI ----------------
        if p == "/lfi/read":
            c = resolve("/var/www/html/pages", v, FS)
            return self.send(200, page(f"<pre>{c}</pre>" if c else "File not found"))
        if p == "/lfi/post" and self.command == "POST":
            c = resolve("/var/www/html/pages", v, FS)
            return self.send(200, page(f"<pre>{c}</pre>" if c else "File not found"))
        if p == "/lfi/suffix":
            if v.startswith("php://filter/convert.base64-encode/resource="):
                c = resolve("/var/www/html/pages", v.split("=", 1)[1] + ".php", FS)
                return self.send(200, page(base64.b64encode(c.encode()).decode() if c else ""))
            c = resolve("/var/www/html/pages", v + ".php", FS)
            return self.send(200, page(f"<div>{c}</div>" if c else "Page not found"))
        if p == "/lfi/filteronly":
            if v.startswith("php://filter/convert.base64-encode/resource="):
                c = resolve("/var/www/html/pages", v.split("=", 1)[1] + ".php", FS)
                return self.send(200, page(base64.b64encode(c.encode()).decode() if c else ""))
            if ".." in v or v.startswith("/") or ":" in v:
                return self.send(200, page("Hacking attempt blocked"))
            c = resolve("/var/www/html/pages", v + ".php", FS)
            return self.send(200, page(c or "Page not found"))
        if p == "/lfi/strip":
            if v.startswith("/") or ":" in v:
                return self.send(200, page("absolute paths not allowed"))
            c = resolve("/var/www/html/pages", v.replace("../", ""), FS)
            return self.send(200, page(f"<pre>{c}</pre>" if c else "nope"))
        if p == "/lfi/double":
            if ".." in v or v.startswith("/") or ":" in v:
                return self.send(403, page("forbidden"))
            c = resolve("/var/www/html/pages", unquote(v), FS)
            return self.send(200, page(f"<pre>{c}</pre>" if c else "nope"))
        if p == "/lfi/win":
            w = v.split("\x00")[0].replace("\\", "/").lower()
            if w.startswith("file:///"):
                w = w[8:]
            path = w if re.match(r"[a-z]:/", w) else posixpath.join("c:/inetpub/wwwroot/pages", w)
            drive, rest = path[:2], path[2:]
            c = WINFS.get(drive + posixpath.normpath(rest)) if drive.endswith(":") else None
            return self.send(200, page(f"<pre>{c}</pre>" if c else "not found"))
        if p == "/lfi/environ":
            c = resolve("/var/www/html/pages", v, CHROOT_FS)
            return self.send(200, page(f"<pre>{c}</pre>" if c else "File not found"))
        if p == "/lfi/err":
            if v == "about.php":
                return self.send(200, page("About us"))
            return self.send(200, page(f"<b>Warning</b>: include({html.escape(v)}): failed to open stream: "
                                       "No such file or directory in /var/www/html/err.php on line 3"))
        # safe twins
        if p == "/lfi/static":
            return self.send(200, page("<h2>passwd format</h2><pre>root:x:0:0:root:/root:/bin/bash</pre>"
                                       "<pre>; for 16-bit app support\n[fonts]\n[extensions]</pre>"))
        if p == "/lfi/echo":
            return self.send(200, page(f"You asked for {v}"))
        if p == "/lfi/helpful":
            if v in ("about.php", "home.php"):
                return self.send(200, page("ok"))
            return self.send(200, page("Invalid. Lines look like root:x:0:0:root:/root:/bin/bash"))
        if p == "/lfi/scary":
            return self.send(200, page("<b>Warning</b>: include(): failed to open stream in x.php"
                                       f" -- you said {html.escape(v)}"))
        if p == "/lfi/whitelist":
            c = FS.get("/var/www/html/pages/" + posixpath.basename(v))
            return self.send(200, page(c or "unknown page"))
        if p == "/lfi/b64static":
            src = base64.b64encode(b"<?php echo 'demo source'; ?>\n").decode()
            return self.send(200, page(f"Example: {src} for {html.escape(v)}"))
        if p == "/lfi/nullsafe":  # suffix appended, null byte NOT honoured (modern PHP)
            if "\x00" in v:
                return self.send(200, page("ValueError: must not contain any null bytes"))
            c = resolve("/var/www/html/pages", v + ".php", FS)
            return self.send(200, page(c or "Page not found"))

        # ---------------- RFI ----------------
        if p == "/rfi/remote.txt":
            return self.send(200, REMOTE, "text/plain")
        if p == "/rfi/inc":
            c = include_remote(v)
            return self.send(200, page(c if c is not None else (resolve("/var/www/html/pages", v + ".php", FS) or "home")))
        if p == "/rfi/suffix":
            c = include_remote(v + ".php") if v.startswith("http") else include_remote(v)
            return self.send(200, page(c if c is not None else "home"))
        if p == "/rfi/err":
            if v.startswith(("http://", "https://", "data:")):
                return self.send(200, page("<b>Warning</b>: include(): http:// wrapper is disabled in the server "
                                           "configuration by allow_url_include=0<br><b>Warning</b>: include("
                                           f"{html.escape(v)}): failed to open stream: no suitable wrapper"))
            return self.send(200, page("home"))
        if p == "/rfi/echo":
            return self.send(200, page(f'Link: <a href="{html.escape(v)}">{html.escape(v)}</a>'))
        if p == "/rfi/static":
            return self.send(200, page("Example Domain TIDREMOTE-q8z3 is our partner. " + html.escape(v)))
        if p == "/rfi/whitelist":
            return self.send(200, page("home" if v not in ("home", "about") else v))

        # ---------------- PHPi ----------------
        if p == "/phpi/eval":  # eval($code)
            s = v.strip()
            ok = s.startswith(("print(", "sleep(", ";"))
            return self.send(200, page(php(v) if ok else "Parse error: syntax error, unexpected"))
        if p == "/phpi/str":  # eval("$x = '" . $name . "';")
            ok = "';" in v or "'." in v
            return self.send(200, page(("Hello " + php(v)) if ok else f"Hello {html.escape(v)}"))
        if p == "/phpi/blind":
            s = v.strip()
            if s.startswith(("print(", "sleep(", ";")):
                php(v, output=False)
            return self.send(200, page("done"))
        if p == "/phpi/echo":
            return self.send(200, page(f"Code: {v}"))
        if p == "/phpi/calc":  # computes products anywhere in the input (not code injection)
            prods = [str(int(a) * int(b)) for a, b in re.findall(r"(\d+)\*(\d+)", v)]
            return self.send(200, page("Results: " + ", ".join(prods)))
        if p == "/phpi/slow":
            time.sleep(random.uniform(3, 7))
            return self.send(200, page("slow " + html.escape(v)))

        # ---------------- RCE ----------------
        if p == "/rce/ping":  # ping -c 1 $host
            seps = (";", "|", "&", "\n", "$(", "`")
            out = sh(v) if any(x in v for x in seps) else ""
            return self.send(200, page(f"<pre>PING {html.escape(v.split(';')[0])}\n{out}</pre>"))
        if p == "/rce/quoted":  # ping -c 1 "$host"
            ok = '"' in v or "$(" in v or "`" in v
            return self.send(200, page(f"<pre>{sh(v) if ok else 'PING ok'}</pre>"))
        if p == "/rce/blind":
            if any(x in v for x in (";", "|", "&", "\n", "$(", "`")):
                sh(v, output=False)
            return self.send(200, page("queued"))
        if p == "/rce/win":
            out = sh(v, windows=True) if ("&" in v or "|" in v) else ""
            return self.send(200, page(f"<pre>Pinging {html.escape(v)}\n{out}</pre>"))
        if p == "/rce/echo":
            return self.send(200, page(f"<pre>ping -c 1 {v}</pre>"))
        if p == "/rce/slow":
            time.sleep(random.uniform(3, 7))
            return self.send(200, page("slow"))
        if p == "/rce/safe":
            ok = re.fullmatch(r"[\d.]+", v)
            return self.send(200, page("PING ok" if ok else "invalid host"))

        # ---------------- CGI / Shellshock ----------------
        if p.startswith("/cgi-bin/"):
            hv = [self.headers.get(h, "") for h in ("User-Agent", "Referer", "Cookie")]
            vuln_host = host == "127.0.0.1"
            name = p[len("/cgi-bin/"):]
            if vuln_host and name in ("test-cgi", "vuln.cgi"):
                for val in hv:
                    m = re.match(r"\(\) \{.*?\};(.*)", val)
                    if m:
                        out = sh(m.group(1))
                        return self.send(200, "\n" + out + "\n", "text/plain")
                return self.send(200, "hello from cgi", "text/plain")
            if name == "echo.cgi" or (not vuln_host and name == "test-cgi"):
                env = "\n".join(f"HTTP_{h.upper().replace('-', '_')}={v}" for h, v in zip(("User-Agent", "Referer", "Cookie"), hv))
                return self.send(200, env, "text/plain")
            if name in ("err.cgi", "status"):
                if any(x.startswith("() {") for x in hv):
                    return self.send(500, "Internal Server Error", "text/plain")
                return self.send(200, "status ok", "text/plain")
            return self.send(404, "Not Found", "text/plain")

        # ---------------- Struts ----------------
        if p.startswith("/struts/"):
            ct = self.headers.get("Content-Type", "")
            name = p[len("/struts/"):]
            if name in ("vuln.action", "bodyonly.action"):
                hdr = {}
                body = "Struts app"
                m = re.search(r"addHeader\('([\w-]+)',(\d+)\*(\d+)\)", ct)
                if m and name == "vuln.action":
                    hdr[m.group(1)] = str(int(m.group(2)) * int(m.group(3)))
                m = re.search(r"println\('(\w+)'\+\((\d+)\*(\d+)\)\)", ct)
                if m and "multipart/form-data" in ct:
                    body = m.group(1) + str(int(m.group(2)) * int(m.group(3)))
                return self.send(200, body, "text/plain", hdr)
            if name == "echo.action":
                return self.send(200, "Content-Type was: " + ct, "text/plain",
                                 {"X-Tid-Check": ct[:200].encode("latin-1", "replace").decode("latin-1")})
            if name == "err.action":
                if "%{" in ct:
                    return self.send(500, "ognl.OgnlException: source is null for getProperty", "text/plain")
                return self.send(200, "ok", "text/plain")
            return self.send(404, "nf")

        # ---------------- path traversal ----------------
        for prefix, mode in (("/static/", "vuln"), ("/assets/", "double"), ("/files/", "safe"), ("/docs/", "trap")):
            if p.startswith(prefix) or self.path.startswith(prefix):
                rest = self.path[len(prefix):].split("?")[0]
                if mode == "trap":
                    return self.send(200, page("Doc page. Sample: root:x:0:0:root:/root:/bin/bash"))
                once = unquote(rest)
                if mode == "safe":
                    if ".." in once:
                        return self.send(403, page("Forbidden"))
                    c = FS.get("/var/www/static/" + once)
                    return self.send(200 if c else 404, page(c or "Not found"))
                if mode == "double":
                    if ".." in once:
                        return self.send(403, page("Forbidden"))
                    once = unquote(once)
                c = FS.get(posixpath.normpath(posixpath.join("/var/www/static", once.replace("\\", "/"))))
                return self.send(200 if c else 404, page(f"<pre>{c}</pre>" if c else "Not found"))
        return self.send(404, page("Not found"))


def make_server(port):
    ThreadingHTTPServer.daemon_threads = True
    return ThreadingHTTPServer(("127.0.0.1", port), H)


if __name__ == "__main__":
    make_server(PORT).serve_forever()
