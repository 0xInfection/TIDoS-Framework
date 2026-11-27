#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Web technology fingerprinter -- servers, languages, frameworks, CMS and libraries."""

from __future__ import annotations

import re

import requests

from core.methods import modkit as kit
from core.methods.print import pscan

info = ("This module tries to find out what technologies the target uses: web "
        "server, language/runtime, framework, CMS, CDN/hosting, JavaScript/CSS "
        "libraries (with versions) and third-party services. Evidence comes from "
        "response headers, cookies, the meta generator tag, script/stylesheet URLs "
        "and a few framework-specific HTML attributes; ordinary page text is never "
        "matched.")
searchinfo = "Web Technology Fingerprinter"
properties = {}

MAX_BODY = 1024 * 1024

# (category, technology, kind, field, pattern)
#   header -- `field` is a regex fullmatched against header names, `pattern`
#             searched in the value ("" = presence)
#   cookie -- `pattern` fullmatched against cookie names
#   asset  -- `pattern` searched in script src / stylesheet href URLs
#   html   -- `pattern` searched in the HTML; anchor it on tags/attributes
# A named group `v` captures the version.
SIGNATURES = (
    # ---- languages / runtimes ---------------------------------------------
    ("Language", "PHP", "header", "x-powered-by", r"\bPHP/(?P<v>\d+(?:\.\d+)+)"),
    ("Language", "PHP", "cookie", "", r"PHPSESSID"),
    ("Language", "Java", "cookie", "", r"JSESSIONID"),
    ("Language", "Java", "header", "x-powered-by", r"\b(?:Servlet|JSP)/(?P<v>[\d.]+)"),
    ("Language", "ASP.NET", "header", "x-aspnet-version", r"(?P<v>\d+(?:\.\d+)+)"),
    ("Language", "ASP.NET", "header", "x-powered-by", r"^ASP\.NET$"),
    ("Language", "ASP.NET", "cookie", "", r"ASP\.NET_SessionId|\.AspNetCore\.[\w.]+|\.ASPXAUTH"),
    ("Language", "ASP.NET", "html", "", r"<input[^>]+name=[\"']__VIEWSTATE[\"']"),
    ("Language", "Classic ASP", "cookie", "", r"ASPSESSIONID[A-Z]{8}"),
    ("Language", "ColdFusion", "cookie", "", r"CFID|CFTOKEN"),
    ("Language", "Node.js", "cookie", "", r"connect\.sid"),

    # ---- frameworks -------------------------------------------------------
    ("Framework", "ASP.NET MVC", "header", "x-aspnetmvc-version", r"(?P<v>\d+(?:\.\d+)+)"),
    ("Framework", "Blazor", "asset", "", r"/_framework/blazor\.(?:web|server|webassembly)\.js"),
    ("Framework", "Express", "header", "x-powered-by", r"^Express$"),
    ("Framework", "Next.js", "header", "x-powered-by", r"^Next\.js(?: (?P<v>[\d.]+))?"),
    ("Framework", "Next.js", "html", "", r"<script[^>]+id=[\"']__NEXT_DATA__[\"']"),
    ("Framework", "Next.js", "asset", "", r"/_next/static/"),
    ("Framework", "Nuxt", "asset", "", r"/_nuxt/"),
    ("Framework", "Nuxt", "html", "", r"<script>window\.__NUXT__="),
    ("Framework", "Gatsby", "html", "", r"<div[^>]+id=[\"']___gatsby[\"']"),
    ("Framework", "Angular", "html", "", r"<[a-z][\w-]*\s[^>]*\bng-version=[\"'](?P<v>\d+(?:\.\d+)+)[\"']"),
    ("Framework", "AngularJS", "html", "", r"<(?:html|body|div|main|section)\s[^>]*\b(?:data-)?ng-app\b"),
    ("Framework", "React", "html", "", r"<[a-z][\w-]*\s[^>]*\bdata-react(?:root|id)\b"),
    ("Framework", "Vue.js", "html", "", r"<[a-z][\w-]*\s[^>]*\bdata-server-rendered=[\"']true[\"']"),
    ("Framework", "Django", "html", "", r"<input[^>]+name=[\"']csrfmiddlewaretoken[\"']"),
    ("Framework", "Django", "cookie", "", r"django_language"),
    ("Framework", "Laravel", "cookie", "", r"laravel_session"),
    ("Framework", "Laravel Livewire", "html", "", r"<[a-z][\w-]*\s[^>]*\bwire:id=[\"']"),
    ("Framework", "CodeIgniter", "cookie", "", r"ci_session"),
    ("Framework", "CakePHP", "cookie", "", r"CAKEPHP"),
    ("Framework", "Ruby on Rails", "html", "", r"<meta[^>]+name=[\"']csrf-param[\"'][^>]+content=[\"']authenticity_token[\"']"),
    ("Framework", "JavaServer Faces", "html", "", r"<input[^>]+name=[\"']javax\.faces\.ViewState[\"']"),

    # ---- CMS / platforms --------------------------------------------------
    ("CMS", "WordPress", "asset", "", r"/wp-(?:content|includes)/"),
    ("CMS", "WordPress", "header", "link", r"/wp-json/>;\s*rel=[\"']https://api\.w\.org/"),
    ("CMS", "WordPress", "cookie", "", r"wordpress_(?:test_cookie|logged_in_[0-9a-f]+|sec_[0-9a-f]+)|wp-settings-\d+"),
    ("CMS", "Drupal", "header", "x-generator", r"^Drupal (?P<v>\d+)"),
    ("CMS", "Drupal", "header", "x-drupal-(?:cache|dynamic-cache)", ""),
    ("CMS", "Drupal", "cookie", "", r"S?SESS[0-9a-f]{32}"),
    ("CMS", "Drupal", "asset", "", r"/sites/(?:default|all)/(?:files|themes|modules)/|/core/misc/drupal\.js"),
    ("CMS", "Joomla", "asset", "", r"/media/(?:jui|system)/js/[\w.-]+\.js"),
    ("CMS", "Magento", "cookie", "", r"mage-cache-(?:sessid|storage)"),
    ("CMS", "Magento", "html", "", r"<[a-z][\w-]*\s[^>]*\bdata-mage-init=|<script[^>]+type=[\"']text/x-magento-init[\"']"),
    ("CMS", "PrestaShop", "cookie", "", r"PrestaShop-[0-9a-f]{32}"),
    ("CMS", "Shopify", "header", "x-shopid|x-shopify-stage", ""),
    ("CMS", "Shopify", "asset", "", r"//cdn\.shopify\.com/"),
    ("CMS", "Squarespace", "asset", "", r"//static1\.squarespace\.com/"),
    ("CMS", "Wix", "asset", "", r"//static\.(?:parastorage|wixstatic)\.com/"),
    ("CMS", "Ghost", "asset", "", r"/ghost/(?:api|assets)/|/public/ghost-sdk(?:\.min)?\.js"),

    # ---- CDN / hosting / proxies ------------------------------------------
    ("CDN / hosting", "Cloudflare", "header", "cf-ray", r"^[0-9a-f]{12,20}"),
    ("CDN / hosting", "Amazon CloudFront", "header", "x-amz-cf-id", ""),
    ("CDN / hosting", "Akamai", "header", "server", r"^AkamaiGHost\b"),
    ("CDN / hosting", "Fastly", "header", "x-served-by", r"^cache-[a-z0-9-]+"),
    ("CDN / hosting", "Fastly", "header", "x-fastly-request-id", ""),
    ("CDN / hosting", "Varnish", "header", "x-varnish", r"^\d+(?: \d+)?$"),
    ("CDN / hosting", "Vercel", "header", "x-vercel-id", ""),
    ("CDN / hosting", "Netlify", "header", "x-nf-request-id", ""),
    ("CDN / hosting", "GitHub Pages", "header", "x-github-request-id", ""),
    ("CDN / hosting", "Heroku", "header", "via", r"\bvegur\b"),
    ("CDN / hosting", "Azure Front Door", "header", "x-azure-ref", ""),

    # ---- third-party services ---------------------------------------------
    ("Analytics / services", "Google Tag Manager", "asset", "", r"//www\.googletagmanager\.com/gtm\.js"),
    ("Analytics / services", "Google Analytics", "asset", "",
     r"//www\.googletagmanager\.com/gtag/js|//(?:www|ssl)\.google-analytics\.com/(?:analytics|ga|urchin)\.js"),
    ("Analytics / services", "Hotjar", "asset", "", r"//static\.hotjar\.com/"),
    ("Analytics / services", "Matomo", "asset", "", r"/(?:matomo|piwik)\.js(?:[?#]|$)"),
    ("Analytics / services", "Plausible", "asset", "", r"//plausible\.io/js/"),
    ("Analytics / services", "Segment", "asset", "", r"//cdn\.segment\.com/"),
    ("Analytics / services", "HubSpot", "asset", "", r"//js\.hs-scripts\.com/"),
    ("Analytics / services", "Facebook Pixel / SDK", "asset", "", r"//connect\.facebook\.net/"),
    ("Analytics / services", "Cloudflare Web Analytics", "asset", "", r"//static\.cloudflareinsights\.com/"),
    ("Analytics / services", "Sentry", "asset", "", r"//browser\.sentry-cdn\.com/(?P<v>[\d.]+)/"),
    ("Analytics / services", "Stripe.js", "asset", "", r"//js\.stripe\.com/"),
    ("Analytics / services", "Google reCAPTCHA", "asset", "", r"//www\.(?:google|recaptcha)\.(?:com|net)/recaptcha/"),
    ("Analytics / services", "hCaptcha", "asset", "", r"//(?:js\.)?hcaptcha\.com/"),
    ("Analytics / services", "Cloudflare Turnstile", "asset", "", r"//challenges\.cloudflare\.com/turnstile/"),
)

# script/stylesheet file names of well-known libraries: jquery-3.7.1.min.js,
# bootstrap.bundle.min.js, vue.global.prod.js ...
LIBRARIES = {
    "jquery": "jQuery", "jquery-ui": "jQuery UI", "jquery-migrate": "jQuery Migrate",
    "bootstrap": "Bootstrap", "react": "React", "react-dom": "React", "vue": "Vue.js",
    "angular": "AngularJS", "lodash": "Lodash", "underscore": "Underscore.js",
    "moment": "Moment.js", "d3": "D3.js", "three": "three.js", "axios": "Axios",
    "backbone": "Backbone.js", "knockout": "Knockout", "ember": "Ember.js",
    "handlebars": "Handlebars", "modernizr": "Modernizr", "popper": "Popper",
    "alpine": "Alpine.js", "htmx": "htmx", "socket.io": "Socket.IO", "chart": "Chart.js",
    "font-awesome": "Font Awesome", "fontawesome": "Font Awesome",
    "bulma": "Bulma", "foundation": "Foundation", "materialize": "Materialize",
    "swiper": "Swiper", "select2": "Select2", "leaflet": "Leaflet", "prototype": "Prototype",
    "mootools": "MooTools", "require": "RequireJS", "highlight": "highlight.js",
    # cdnjs / npm package names
    "lodash.js": "Lodash", "underscore.js": "Underscore.js", "twitter-bootstrap": "Bootstrap",
    "moment.js": "Moment.js", "chart.js": "Chart.js", "three.js": "three.js", "backbone.js": "Backbone.js",
    "angular.js": "AngularJS", "vue-router": "Vue Router", "alpinejs": "Alpine.js",
    "@popperjs/core": "Popper", "@fortawesome/fontawesome-free": "Font Awesome",
}
VERSION_PARAM = re.compile(r"[?&](?:ver|v|version)=(\d+(?:\.\d+){1,3})\b")
LIB_FILE = re.compile(
    r"/(?P<lib>[a-z][a-z0-9.-]*?)(?:[.-]v?(?P<v>\d+(?:\.\d+){1,3}))?"
    r"(?:\.(?:min|slim|bundle|umd|global|prod|production|esm-browser|full))*\.(?:js|css)(?:[?#]|$)", re.I)
# versioned CDN paths: cdnjs /ajax/libs/<lib>/<ver>/, jsDelivr /npm/<lib>@<ver>, unpkg /<lib>@<ver>
LIB_CDN = re.compile(
    r"/ajax/libs/(?P<lib>[\w.-]+)/(?P<v>\d+(?:\.\d+)+)/"
    r"|//(?:cdn\.jsdelivr\.net/npm|unpkg\.com)/(?P<lib2>(?:@[\w.-]+/)?[\w.-]+)@(?P<v2>\d+(?:\.\d+)+)", re.I)

ASSET = re.compile(
    r"<script\b[^>]*?\ssrc\s*=\s*[\"']?([^\"'\s>]+)"
    r"|<link\b[^>]*?\shref\s*=\s*[\"']?([^\"'\s>]+)", re.I)
GENERATOR = re.compile(
    r"<meta\s+(?:[^>]*?\s)?(?:name=[\"']generator[\"'][^>]*?\scontent=[\"']([^\"']+)"
    r"|content=[\"']([^\"']+)[\"'][^>]*?\sname=[\"']generator[\"'])", re.I)
COOKIE_NAME = re.compile(r"\s*([^=;,\s]+)\s*=")


def _compile(kind, field, pattern):
    name = re.compile(field, re.I) if kind == "header" else None
    if kind == "cookie":
        return name, re.compile(pattern)
    if kind == "html":
        return name, re.compile(pattern, re.I)
    return name, re.compile(pattern, re.I) if pattern else None


COMPILED = tuple((cat, tech, kind, *_compile(kind, field, pattern))
                 for cat, tech, kind, field, pattern in SIGNATURES)


def _version(m) -> str:
    return (m.groupdict().get("v") or "") if m else ""


def cookie_names(responses) -> list[str]:
    names = []
    for r in responses:
        raw = getattr(getattr(r, "raw", None), "headers", None)
        lines = raw.getlist("Set-Cookie") if hasattr(raw, "getlist") else [r.headers.get("Set-Cookie", "")]
        for line in lines:
            m = COOKIE_NAME.match(line or "")
            if m and m.group(1) not in names:
                names.append(m.group(1))
    return names


def assets(html: str) -> list[str]:
    return list(dict.fromkeys(a or b for a, b in ASSET.findall(html)))


def libraries(urls) -> list[tuple[str, str]]:
    """(library, version) pairs named by script/stylesheet URLs."""
    found = []
    for u in urls:
        m = LIB_CDN.search(u)
        if m:
            lib = (m.group("lib") or m.group("lib2")).lower()
            found.append((LIBRARIES.get(lib) or lib, m.group("v") or m.group("v2")))
            continue
        m = LIB_FILE.search(u)
        if m and m.group("lib").lower() in LIBRARIES:
            param = VERSION_PARAM.search(u)
            found.append((LIBRARIES[m.group("lib").lower()], m.group("v") or (param.group(1) if param else "")))
    return found


def fingerprint(headers, cookies, html) -> dict[str, dict[str, str]]:
    """{category: {technology: version}} from one page."""
    html = html[:MAX_BODY]
    urls = assets(html)
    result: dict[str, dict[str, str]] = {}

    def add(cat, tech, version=""):
        techs = result.setdefault(cat, {})
        techs[tech] = techs.get(tech) or version

    server = headers.get("Server", "").strip()
    if server:
        add("Web server", server)
    for m in GENERATOR.finditer(html):
        add("Generator", (m.group(1) or m.group(2)).strip())
    if headers.get("X-Generator"):
        add("Generator", headers["X-Generator"].strip())

    for cat, tech, kind, name_rx, rx in COMPILED:
        if kind == "header":
            for name, value in headers.items():
                if name_rx.fullmatch(name):
                    m = rx.search(value) if rx else None
                    if rx is None or m:
                        add(cat, tech, _version(m))
        elif kind == "cookie":
            if any(rx.fullmatch(c) for c in cookies):
                add(cat, tech)
        elif kind == "asset":
            for u in urls:
                m = rx.search(u)
                if m:
                    add(cat, tech, _version(m))
                    break
        else:
            m = rx.search(html)
            if m:
                add(cat, tech, _version(m))

    # raw X-Powered-By, unless a signature already explained it
    powered = headers.get("X-Powered-By", "").strip()
    if powered and not any(t in powered for techs in result.values() for t in techs):
        add("Powered by", powered)
    for lib, version in libraries(urls):
        add("JavaScript / CSS libraries", lib, version)
    return result


def webtech(web):
    pscan("web technologies")
    url = kit.url(web)
    record = kit.Recorder(web, kit.SCAN, "webtech")
    kit.info(f"Fingerprinting {url}...")
    try:
        resp = kit.http().get(url)
    except requests.RequestException as e:
        kit.bad(f"Could not fetch {url}: {type(e).__name__}")
        return {}

    ctype = resp.headers.get("Content-Type", "")
    html = resp.text if "html" in ctype or not ctype else ""
    result = fingerprint(resp.headers, cookie_names([*resp.history, resp]), html)
    if not result:
        kit.bad("No technologies identified.")
        record("No technologies identified.")
        return {}

    kit.good(f"Technologies identified (HTTP {resp.status_code}, {resp.url}):")
    for cat, techs in result.items():
        names = ", ".join(f"{t} {v}".strip() for t, v in techs.items())
        kit.found(cat, names)
        record(f"{cat} :> {names}")
    kit.good("Fingerprinting done!")
    return result


def attack(web):
    webtech(web)
