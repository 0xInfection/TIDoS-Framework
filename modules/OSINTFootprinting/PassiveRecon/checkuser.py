#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Alias (username) check across public websites -- passive recon."""

from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor

from core.methods import modkit as kit
from core.methods.print import posintpas

info = ("Checks whether the target's aliases (usernames) are registered on popular websites. "
        "May return false positives when a site rate-limits or changes its pages.")
searchinfo = "Alias Check"
properties = {
    "USERNAMES": ["Aliases to check, comma separated (default: target usernames, else the domain name)", ""],
    "THREADS": ["Number of concurrent requests", ""],
}

# name -> (profile URL, text that only appears when the user does NOT exist;
#          None = the site answers 404 for unknown users)
SITES = {
    "GitHub": ("https://github.com/{}", None),
    "GitLab": ("https://gitlab.com/api/v4/users?username={}", "[]"),
    "Bitbucket": ("https://bitbucket.org/{}/", None),
    "SourceForge": ("https://sourceforge.net/u/{}/profile", None),
    "Docker Hub": ("https://hub.docker.com/v2/users/{}/", None),
    "PyPI": ("https://pypi.org/user/{}/", None),
    "npm": ("https://www.npmjs.com/~{}", None),
    "Keybase": ("https://keybase.io/{}", None),
    "Dev.to": ("https://dev.to/{}", None),
    "Hacker News": ("https://news.ycombinator.com/user?id={}", "No such user."),
    "Pastebin": ("https://pastebin.com/u/{}", None),
    "Vimeo": ("https://vimeo.com/{}", None),
    "SoundCloud": ("https://soundcloud.com/{}", None),
    "Gravatar": ("https://en.gravatar.com/{}.json", None),
    "Steam": ("https://steamcommunity.com/id/{}", "The specified profile could not be found"),
    "Reddit": ("https://www.reddit.com/user/{}/about.json", None),
    "Wikipedia": ("https://en.wikipedia.org/w/api.php?action=query&list=users&format=json&ususers={}",
                  '"missing"'),
}

USERNAME_RE = re.compile(r"[\w.-]{1,64}")


def probe(session, site: str, user: str) -> tuple[str, bool | None]:
    """(site, True if taken / False if free / None if inconclusive)."""
    url, missing = SITES[site]
    try:
        resp = session.get(url.format(user), allow_redirects=False)
    except Exception:
        return site, None
    if resp.status_code == 404 or 300 <= resp.status_code < 400:
        return site, False
    if resp.status_code != 200:
        return site, None
    if missing is not None:
        return site, missing not in resp.text
    return site, True


def usernames(web) -> list[str]:
    known = list(getattr(web, "usernames", None) or [])
    default = ",".join(known) or kit.domain(web).split(".")[0]
    raw = kit.option(properties, "USERNAMES", "Aliases to check (comma separated)", default)
    names = [u.strip().lstrip("@") for u in raw.split(",") if u.strip()]
    for bad_name in [u for u in names if not USERNAME_RE.fullmatch(u)]:
        kit.bad(f"Skipping invalid alias: {bad_name}")
    return list(dict.fromkeys(u for u in names if USERNAME_RE.fullmatch(u)))


def checkuser(web):
    posintpas("check alias")
    users = usernames(web)
    if not users:
        kit.bad("No alias to check (set USERNAMES).")
        return {}
    threads = max(1, kit.integer(properties, "THREADS", "Concurrent requests", 10))
    session = kit.http(headers={"X-Requested-With": "XMLHttpRequest"})
    record = kit.Recorder(web, kit.PASSIVE, "checkuser")

    results = {}
    for user in users:
        kit.info(f"Searching alias {user} on {len(SITES)} websites...")
        with ThreadPoolExecutor(threads) as pool:
            answers = list(pool.map(lambda s: probe(session, s, user), SITES))
        taken = [site for site, hit in answers if hit]
        unknown = [site for site, hit in answers if hit is None]
        for site in taken:
            kit.found(user, f"{site} : {SITES[site][0].format(user)}")
        if not taken:
            kit.bad(f"Alias {user} not found on any site.")
        if unknown:
            kit.warn(f"Inconclusive (blocked / rate-limited): {', '.join(unknown)}")
        results[user] = taken
        record([f"{user}: {site}" for site in taken] or f"{user}: not found")
    return results


def attack(web):
    checkuser(web)
