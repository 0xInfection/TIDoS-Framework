#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""Secret hunter -- information disclosure."""

import re

from core.methods import harvest
from core.methods import modkit as kit
from core.methods.print import pleak
from files.signaturedb.infodisc_signatures import SECRET_SIGNATURES

info = ("Finds credentials leaking in the target's pages and same-host JavaScript: "
        "cloud keys (AWS, GCP, Azure, DigitalOcean), GitHub/GitLab/npm tokens, "
        "Slack/Discord webhooks, Stripe/Twilio/SendGrid/Mailgun/OpenAI/Anthropic "
        "keys, private keys, JWTs, credentials in connection URLs and hardcoded "
        "passwords or API secrets.")
searchinfo = "Secret hunter"
properties = {
    "CRAWL": ["Also scan same-host pages and scripts linked from the target (y/n)", ""],
    **kit.AUTH_OPTIONS,
}

COMPILED = [(label, re.compile(rx)) for label, rx in SECRET_SIGNATURES]
GENERIC = "Hardcoded secret"
URL_CREDS = "Credentials in URL"

# values that are obviously placeholders, not secrets
PLACEHOLDER = re.compile(
    r"\{[^}]*\}|\$\{|%s|<%|xxxx|\*{4}|\.{4}|changeme|example|placeholder|your[_-]|"
    r"dummy|redacted|undefined|null|true|false",
    re.I,
)


def _shorten(value: str, width: int = 100) -> str:
    return value if len(value) <= width else value[:width - 3] + "..."



def extract(body):
    specific = []
    for label, rx in COMPILED:
        for m in rx.finditer(body):
            value = m.group(0)
            if label == GENERIC:
                # skip placeholders, plain words (UI labels, translations) and
                # values a specific signature already named
                secret = re.split(r"[:=]\s*", value, maxsplit=1)[-1].strip("'\"")
                if (PLACEHOLDER.search(secret) or any(v in value for v in specific)
                        or not re.search(r"\d", secret) or not re.search(r"[A-Za-z]", secret)):
                    continue
            else:
                if label == URL_CREDS and PLACEHOLDER.search(value):
                    continue  # documentation examples (user:pass@example.com)
                specific.append(value)
            yield f"{label}: {_shorten(value)}"


def secrets(web):
    pleak("secret hunter")
    return harvest.run(web, properties, noun="secrets", lvl2="secrets",
                       extract=extract, scripts=True)


def attack(web):
    secrets(web)
