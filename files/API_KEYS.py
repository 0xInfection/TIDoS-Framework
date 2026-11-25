#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API credentials for TIDoS modules -- read from the environment only.

Never put key values in this file. Export them instead, e.g.

    export TIDOS_SHODAN_API_KEY=...

Each name is looked up as TIDOS_<NAME> first, then <NAME>.
See docs/setup.md for what each key unlocks and where to get it.
"""

import os


def _env(name: str) -> str:
    return (os.environ.get(f"TIDOS_{name}") or os.environ.get(name) or "").strip()


SHODAN_API_KEY = _env("SHODAN_API_KEY")
CENSYS_API_TOKEN = _env("CENSYS_API_TOKEN")
GOOGLE_API_TOKEN = _env("GOOGLE_API_TOKEN")
WHATCMS_ACCESS_TOKEN = _env("WHATCMS_ACCESS_TOKEN")
VIEWDNS_API_KEY = _env("VIEWDNS_API_KEY")
HACKERTARGET_API_KEY = _env("HACKERTARGET_API_KEY")
