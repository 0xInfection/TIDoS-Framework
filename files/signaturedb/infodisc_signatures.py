#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

"""
Signatures used by the information-disclosure modules.

All patterns are meant to be *searched* inside page bodies (re.finditer),
so none of them are anchored to the start/end of the string.
"""

# user@example.com -- the TLD must be alphabetic and not a file extension,
# so retina asset names like "logo@2x.png" are not reported as addresses.
EMAIL_HARVESTER_SIGNATURE = (
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*"
    r"\.(?!(?:png|jpe?g|gif|svg|webp|ico|css|js)\b)[A-Za-z]{2,24}\b"
)

# Addresses that are documentation placeholders or SDK-internal, not leaks
EMAIL_IGNORE_SIGNATURE = (
    r"(?i)@(?:[\w-]+\.)*(?:example\.(?:com|org|net)|domain\.(?:com|tld)|email\.com|"
    r"yourdomain\.\w+|company\.com|test\.com|sentry(?:\.wixpress)?\.(?:io|com)|"
    r"ingest\.(?:us\.)?sentry\.io)$|^(?:your|user(?:name)?|name|email|john\.?doe|jane\.?doe)@"
)

# International (+CC ...) numbers: +44 20 7946 0958, +1-202-555-0143, +4915112345678
# Not preceded by word chars / closing brackets / operators, which in minified
# JS means arithmetic (a+1295307597, )+886263092).
PHONE_NUMBER_SIGNATURE = r"(?<![\w+)\]}*/%=.-])\+\d{1,3}[\s.-]?(?:\(?\d{1,4}\)?[\s.-]?){2,4}\d{2,4}\b"

# RFC 1918 / link-local / CGNAT IPv4, plus IPv6 ULA (fc00::/7)
# and link-local (fe80::/10) addresses. Loopback (127/8, ::1) is left out on
# purpose: it's everywhere (dev-server URLs, docs) and discloses nothing.
INTERNAL_IP_SIGNATURE = (
    r"(?<![\w.])(?:"
    r"10(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}"
    r"|172\.(?:1[6-9]|2\d|3[01])(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){2}"
    r"|192\.168(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){2}"
    r"|169\.254(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){2}"
    r"|100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){2}"
    r")(?![\d.]*\d)(?!\.\d)"
    r"|(?i:(?<![\w:])(?:f[cd][0-9a-f]{2}|fe[89ab][0-9a-f])(?::{1,2}[0-9a-f]{1,4}){2,7}(?![\w:]))"
)

# US SSN, AAA-GG-SSSS, excluding never-issued ranges (000, 666, 9xx, 00, 0000)
SOCIAL_SECURITY_SIGNATURE = r"(?<![\w.-])(?!000|666|9\d\d)\d{3}-(?!00)\d{2}-(?!0000)\d{4}(?![\w-])"

# Card numbers: either 13-19 contiguous digits, or the printed groupings
# 4-4-4-4(-3) / 4-6-5 (Amex) / 4-6-4 (Diners) with one consistent separator.
# Candidates must additionally pass the Luhn check and an issuer prefix, and
# contiguous ones need card-related words nearby (see creditcards module).
CARD_CANDIDATE_SIGNATURE = (
    r"(?<![\w.,-])(?:"
    r"(?P<plain>\d{13,19})"
    r"|\d{4}(?P<s1>[ -])\d{4}(?P=s1)\d{4}(?P=s1)\d{4}(?:(?P=s1)\d{3})?"
    r"|\d{4}(?P<s2>[ -])\d{6}(?P=s2)\d{4,5}"
    r")(?![\w.,-])"
)
CARD_CONTEXT_SIGNATURE = r"(?i)card|credit|debit|\bcc[_-]?(?:num|no|number)?\b|\bpan\b|visa|master|amex|payment|billing"

# Issuer prefixes, matched against the digits-only card number.
VISA_SIGNATURE = r"^4\d{12}(?:\d{3}){0,2}$"
MASTERCARD_SIGNATURE = r"^(?:5[1-5]\d{2}|222[1-9]|22[3-9]\d|2[3-6]\d{2}|27[01]\d|2720)\d{12}$"
AMEX_CARD_SIGNATURE = r"^3[47]\d{13}$"
DISCOVER_CARD_SIGNATURE = r"^6(?:011|5\d{2}|4[4-9]\d)\d{12,15}$"
DINERS_CARD_SIGNATURE = r"^3(?:0[0-5]|[689]\d)\d{11,16}$"
JCB_CARD_SIGNATURE = r"^35(?:2[89]|[3-8]\d)\d{12,15}$"

CARD_ISSUERS = (
    ("Visa", VISA_SIGNATURE),
    ("MasterCard", MASTERCARD_SIGNATURE),
    ("American Express", AMEX_CARD_SIGNATURE),
    ("Discover", DISCOVER_CARD_SIGNATURE),
    ("Diners Club", DINERS_CARD_SIGNATURE),
    ("JCB", JCB_CARD_SIGNATURE),
)


# Leaked credentials / secrets: (label, regex). Prefix-anchored token formats
# first; the generic assignment patterns last since they are the noisiest.
SECRET_SIGNATURES = (
    # cloud providers
    ("AWS access key ID", r"\b(?:AKIA|ASIA|ABIA|ACCA)[0-9A-Z]{16}\b"),
    ("AWS secret access key", r"(?i)aws.{0,20}?(?:secret|private).{0,20}?['\"][0-9a-zA-Z/+]{40}['\"]"),
    ("Google API key", r"\bAIza[0-9A-Za-z_-]{35}\b"),
    ("Google OAuth client ID", r"\b\d+-[0-9a-z_]{32}\.apps\.googleusercontent\.com\b"),
    ("GCP service account", r"\"type\":\s*\"service_account\""),
    ("Azure storage connection string", r"DefaultEndpointsProtocol=https?;AccountName=[^;]+;AccountKey=[A-Za-z0-9+/=]{40,}"),
    ("Azure SAS token", r"[?&]sig=[A-Za-z0-9%]{40,}(?:&|$)[^\s\"']*?se=\d{4}-\d{2}-\d{2}"),
    ("DigitalOcean token", r"\bdo[pore]_v1_[a-f0-9]{64}\b"),
    ("Heroku API key", r"(?i)heroku.{0,20}?['\"][0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}['\"]"),
    # source control / CI / package registries
    ("GitHub token", r"\b(?:gh[pousr]_[A-Za-z0-9]{36,255}|github_pat_[A-Za-z0-9_]{82})\b"),
    ("GitLab token", r"\bglpat-[A-Za-z0-9_-]{20}\b"),
    ("npm token", r"\bnpm_[A-Za-z0-9]{36}\b"),
    ("PyPI token", r"\bpypi-AgEIcHlwaS5vcmc[A-Za-z0-9_-]{50,}\b"),
    # SaaS / messaging / payments
    ("Slack token", r"\bxox[abposr]-[A-Za-z0-9-]{10,72}\b"),
    ("Slack webhook", r"https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]{20,}"),
    ("Discord webhook", r"https://(?:ptb\.|canary\.)?discord(?:app)?\.com/api/webhooks/\d+/[\w-]{60,}"),
    ("Telegram bot token", r"\b\d{8,10}:AA[0-9A-Za-z_-]{33}\b"),
    ("Stripe secret key", r"\b(?:sk|rk)_live_[0-9a-zA-Z]{24,99}\b"),
    ("Square access token", r"\bEAAA[0-9A-Za-z_-]{60}\b|\bsq0(?:atp|csp)-[0-9A-Za-z_-]{22,43}\b"),
    ("PayPal Braintree token", r"\baccess_token\$production\$[0-9a-z]{16}\$[0-9a-f]{32}\b"),
    ("Shopify token", r"\bshp(?:at|ca|pa|ss)_[a-fA-F0-9]{32}\b"),
    ("Twilio API key", r"\bSK[0-9a-fA-F]{32}\b"),
    ("SendGrid API key", r"\bSG\.[\w-]{22}\.[\w-]{43}\b"),
    ("Mailgun API key", r"\bkey-[0-9a-zA-Z]{32}\b"),
    ("Mailchimp API key", r"\b[0-9a-f]{32}-us\d{1,2}\b"),
    ("OpenAI API key", r"\bsk-(?:proj-|svcacct-|admin-)?[A-Za-z0-9_-]{20,}T3BlbkFJ[A-Za-z0-9_-]{20,}\b"),
    ("Anthropic API key", r"\bsk-ant-(?:api|admin)\d{2}-[A-Za-z0-9_-]{80,}\b"),
    # keys, tokens, connection strings
    ("Private key", r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED |PGP )?PRIVATE KEY(?: BLOCK)?-----"),
    ("JSON Web Token", r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
    ("Credentials in URL", r"\b(?:mongodb(?:\+srv)?|mysql|postgres(?:ql)?|redis|rediss|amqps?|mssql|sqlserver|ftp|smtp)://[^\s:/@\"'<>]+:[^\s@/\"'<>]+@[^\s\"'<>]+"),
    ("Basic auth header", r"(?i)authorization['\"]?\s*[:=]\s*['\"]basic [A-Za-z0-9+/=]{12,}['\"]"),
    ("Bearer token", r"(?i)authorization['\"]?\s*[:=]\s*['\"]bearer [A-Za-z0-9._~+/=-]{20,}['\"]"),
    # generic: value must be 8-128 chars without whitespace; the module also
    # requires a digit + a letter and drops placeholders (labels, templates)
    ("Hardcoded secret", r"(?i)(?<![\w-])['\"]?(?:[a-z0-9]+[_-])*(?:api[_-]?key|api[_-]?secret|client[_-]?secret|secret(?:[_-]?key)?|access[_-]?token|auth[_-]?token|private[_-]?key|password|passwd|db[_-]?pass(?:word)?)['\"]?\s*[:=]\s*['\"][^'\"\s<>]{8,128}['\"]"),
)
