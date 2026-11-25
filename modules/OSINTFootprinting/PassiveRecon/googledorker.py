#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Google dorker -- passive recon."""

import random
import time

from core.methods import modkit as kit
from core.methods.google import Blocked, blocked_hint, search
from core.methods.print import posintpas

info = "Finding interesting pages using Google, like logins, open redirects or backdoors."
searchinfo = "Information Gathering with Google"
properties = {
    "LIMIT": ["Maximum results per dork", ""],
    "DELAY": ["Seconds to pause between dorks (avoids Google's captcha)", ""],
}

# (description, dork) -- {s} is the target domain
DORKS = [
    ("login pages", "site:{s} inurl:wp- OR inurl:login OR inurl:signin OR inurl:checkin OR inurl:join"),
    ("subdomains", "site:*.{s}"),
    ("sub-subdomains", "site:*.*.{s}"),
    ("upload / download pages", "site:{s} inurl:wp- OR inurl:plugin OR inurl:upload OR inurl:download"),
    ("backdoors", "site:{s} inurl:shell OR inurl:backdoor OR inurl:wso OR inurl:cmd OR shadow OR passwd OR boot.ini"),
    ("install / setup files", "site:{s} inurl:readme OR inurl:license OR inurl:install OR inurl:setup OR inurl:config"),
    ("open redirects", "site:{s} inurl:redir OR inurl:url OR inurl:redirect OR inurl:return OR inurl:src=http OR inurl:r=http"),
    ("files by extension", "site:{s} ext:cgi OR ext:php OR ext:asp OR ext:aspx OR ext:jsp OR ext:jspx OR ext:swf OR ext:fla OR ext:xml"),
    ("documents by extension", "site:{s} ext:doc OR ext:docx OR ext:csv OR ext:pdf OR ext:txt OR ext:log OR ext:bak"),
    ("employees on LinkedIn", "site:linkedin.com employees {s}"),
    ("phpinfo files", "inurl:'/phpinfo.php' {s}"),
    ("files containing passwords", "site:{s} intext:'connectionString' AND inurl:'web' AND ext:'config'"),
    (".htaccess & sensitive files", "inurl:'/phpinfo.php' OR inurl:'.htaccess' OR inurl:'/.git' {s} -github"),
    ("callback endpoints", "site:{s} inurl:callback"),
]


def googledorker(web):
    posintpas("google dorker")
    site = kit.domain(web)
    limit = kit.integer(properties, "LIMIT", "Maximum results per dork", 30)
    delay = kit.integer(properties, "DELAY", "Pause between dorks in seconds", 20)
    record = kit.Recorder(web, kit.PASSIVE, "googledorker")
    kit.warn("You may get a captcha if you dork too frequently.")

    results = {}
    for n, (what, dork) in enumerate(DORKS):
        if n and delay > 0:
            pause = random.uniform(delay, delay * 2)
            kit.info(f"Pausing {pause:.0f}s to avoid the captcha...")
            time.sleep(pause)
        query = dork.format(s=site)
        kit.info(f"Finding {what} for {site}...")
        try:
            links = search(query, limit)
        except Blocked:
            blocked_hint()
            kit.bad(f"Aborting: {len(DORKS) - n} dork(s) not run.")
            break
        except Exception as e:
            kit.bad(f"Search failed: {e}")
            continue
        if not links:
            kit.bad("Nothing found.")
            continue
        for link in links:
            kit.found("Site found", link)
        results[query] = links
        record([query] + links)

    kit.good(f"Google dorking done: {sum(map(len, results.values()))} result(s).")
    return results


def attack(web):
    googledorker(web)
