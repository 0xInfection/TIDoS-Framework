#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

# This module requires TIDoS Framework
# https://github.com/0xInfection/TIDoS-Framework

"""
Subdomain takeover fingerprints, after EdOverflow's can-i-take-over-xyz.

Each entry:
    service      -- provider name
    cname        -- regexes matched against every name of the CNAME chain
    fingerprint  -- regex matched against the HTTP body of the subdomain
                    ("" when the DNS state alone is the signal)
    nxdomain     -- True when a CNAME to the service that does not resolve
                    (NXDOMAIN) is the takeover signal
    status       -- "vulnerable" (claimable today) or "edge" (claimable only
                    in some setups: verify manually before reporting)

A subdomain is reported only when its CNAME chain points at the service AND
the fingerprint matches (or, for nxdomain services, the chain dangles).
"""

TAKEOVER_SIGNATURES = [
    # ---- dangling CNAME (NXDOMAIN) is the signal --------------------------
    {"service": "Microsoft Azure", "status": "vulnerable", "nxdomain": True, "fingerprint": "",
     "cname": [r"\.cloudapp\.net$", r"\.cloudapp\.azure\.com$", r"\.azurewebsites\.net$",
               r"\.blob\.core\.windows\.net$", r"\.azure-api\.net$", r"\.azurehdinsight\.net$",
               r"\.azureedge\.net$", r"\.azurecontainer\.io$", r"\.database\.windows\.net$",
               r"\.azuredatalakestore\.net$", r"\.search\.windows\.net$", r"\.azurecr\.io$",
               r"\.redis\.cache\.windows\.net$", r"\.servicebus\.windows\.net$",
               r"\.visualstudio\.com$", r"\.trafficmanager\.net$", r"\.azurestaticapps\.net$",
               r"\.azurefd\.net$"]},
    {"service": "AWS Elastic Beanstalk", "status": "vulnerable", "nxdomain": True, "fingerprint": "",
     "cname": [r"\.[a-z]{2}-[a-z]+-\d\.elasticbeanstalk\.com$"]},
    {"service": "Discourse", "status": "vulnerable", "nxdomain": True, "fingerprint": "",
     "cname": [r"\.trydiscourse\.com$"]},
    {"service": "SmugMug", "status": "vulnerable", "nxdomain": True, "fingerprint": "",
     "cname": [r"^domains\.smugmug\.com$"]},

    # ---- HTTP fingerprint is the signal ----------------------------------
    {"service": "AWS S3", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"<Code>NoSuchBucket</Code>|The specified bucket does not exist",
     "cname": [r"\.s3[.-](?:[a-z0-9-]+\.)?amazonaws\.com$", r"\.s3-website[.-][a-z0-9-]+\.amazonaws\.com$"]},
    {"service": "Agile CRM", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"Sorry, this page is no longer available\.", "cname": [r"\.agilecrm\.com$"]},
    {"service": "Airee.ru", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"Ошибка 402\. Сервис\s+Айри\.рф не оплачен", "cname": [r"\.airee\.ru$"]},
    {"service": "Anima", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"The page you were looking for does not exist", "cname": [r"\.animaapp\.io$"]},
    {"service": "Bitbucket", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"Repository not found", "cname": [r"\.bitbucket\.io$"]},
    {"service": "Campaign Monitor", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"Trying to access your account\?|Double check the URL or <a href=\"mailto:help@createsend\.com",
     "cname": [r"\.createsend\.com$"]},
    {"service": "Canny", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"Company Not Found|There is no such company\. Did you enter the right URL\?",
     "cname": [r"\.canny\.io$"]},
    {"service": "Digital Ocean", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"Domain uses DO name servers with no records in DO\.",
     "cname": [r"\.digitaloceanspaces\.com$"]},
    {"service": "Frontify", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"404 - Page Not Found|Oops… looks like you got lost", "cname": [r"\.frontify\.com$"]},
    {"service": "Gemfury", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"404: This page could not be found\.", "cname": [r"\.furyns\.com$"]},
    {"service": "Ghost", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"Site unavailable\.|Failed to resolve DNS path for this host", "cname": [r"\.ghost\.io$"]},
    {"service": "GitHub Pages", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"There isn't a GitHub Pages site here\.|For root URLs \(like http://example\.com/\) you must provide an index\.html file",
     "cname": [r"\.github\.io$", r"^github\.map\.fastly\.net$"]},
    {"service": "HatenaBlog", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"404 Blog is not found", "cname": [r"\.hatenablog\.com$", r"^hatenablog\.com$"]},
    {"service": "Help Juice", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"We could not find what you're looking for\.", "cname": [r"\.helpjuice\.com$"]},
    {"service": "Help Scout", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"No settings were found for this company:", "cname": [r"\.helpscoutdocs\.com$"]},
    {"service": "Helprace", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"Alias not configured!|Admin of this Helprace account needs to set up domain alias",
     "cname": [r"\.helprace\.com$"]},
    {"service": "JetBrains YouTrack", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"is not a registered InCloud YouTrack", "cname": [r"\.myjetbrains\.com$"]},
    {"service": "Kinsta", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"No Site For Domain", "cname": [r"\.kinsta\.cloud$"]},
    {"service": "LaunchRock", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"It looks like you may have taken a wrong turn somewhere\. Don't worry\.\.\.it happens to all of us\.",
     "cname": [r"\.launchrock\.com$"]},
    {"service": "Ngrok", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"Tunnel [\w.-]+\.ngrok(?:-free)?\.(?:io|app|dev) not found|ERR_NGROK_3200",
     "cname": [r"\.ngrok\.io$", r"\.ngrok(?:-free)?\.(?:app|dev)$"]},
    {"service": "Pantheon", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"404 error unknown site!|The gods are wise, but do not know of the site which you seek",
     "cname": [r"\.pantheonsite\.io$"]},
    {"service": "Pingdom", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"Sorry, couldn&#39;t find the status page|Sorry, couldn't find the status page",
     "cname": [r"^stats\.pingdom\.com$"]},
    {"service": "Readme.io", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"The creators of this project are still working on making everything perfect!|Project doesnt exist\.\.\. yet!",
     "cname": [r"\.readme\.io$", r"\.readmessl\.com$"]},
    {"service": "Read the Docs", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"The link you have followed or the URL that you entered does not exist\.|unknown to Read the Docs",
     "cname": [r"\.readthedocs\.io$", r"^readthedocs\.io$"]},
    {"service": "Short.io", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"Link does not exist", "cname": [r"^cname\.short\.io$", r"\.short\.io$"]},
    {"service": "SmartJobBoard", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"This job board website is either expired or its domain name is invalid\.",
     "cname": [r"\.smartjobboard\.com$"]},
    {"service": "Strikingly", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"But if you're looking to build your own website|PAGE NOT FOUND\.",
     "cname": [r"\.strikinglydns\.com$"]},
    {"service": "Surge.sh", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"project not found", "cname": [r"\.surge\.sh$", r"^na-west1\.surge\.sh$"]},
    {"service": "SurveySparrow", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"Account not found\.", "cname": [r"\.surveysparrow\.com$"]},
    {"service": "Tumblr", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"Whatever you were looking for doesn't currently exist at this address|There's nothing here\.",
     "cname": [r"^domains\.tumblr\.com$"]},
    {"service": "Uberflip", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"The URL you've accessed does not provide a hub\.|Non-hub domain, The URL you've accessed does not provide a hub",
     "cname": [r"^read\.uberflip\.com$"]},
    {"service": "Uptimerobot", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"page not found", "cname": [r"^stats\.uptimerobot\.com$"]},
    {"service": "WordPress.com", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"Do you want to register <em>[\w.-]+\.wordpress\.com</em>\?|Do you want to register [\w.-]+\.wordpress\.com\?",
     "cname": [r"\.wordpress\.com$"]},
    {"service": "Worksites", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"Hello! Sorry, but the website you(?:’|')re looking for doesn(?:’|')t exist\.",
     "cname": [r"\.worksites\.net$"]},
    {"service": "Teamwork", "status": "vulnerable", "nxdomain": False,
     "fingerprint": r"Oops - We didn't find your site\.", "cname": [r"\.teamwork\.com$"]},

    # ---- edge cases: claimable only in some setups -----------------------
    {"service": "Heroku", "status": "edge", "nxdomain": False,
     "fingerprint": r"<title>No such app</title>|herokucdn\.com/error-pages/no-such-app\.html",
     "cname": [r"\.herokuapp\.com$", r"\.herokudns\.com$", r"\.herokussl\.com$"]},
    {"service": "Shopify", "status": "edge", "nxdomain": False,
     "fingerprint": r"Sorry, this shop is currently unavailable\.|Only one step left!",
     "cname": [r"\.myshopify\.com$", r"^shops\.myshopify\.com$"]},
    {"service": "Webflow", "status": "edge", "nxdomain": False,
     "fingerprint": r"The page you are looking for doesn't exist or has been moved\.",
     "cname": [r"^proxy(?:-ssl)?\.webflow\.com$"]},
    {"service": "Fastly", "status": "edge", "nxdomain": False,
     "fingerprint": r"Fastly error: unknown domain", "cname": [r"\.fastly\.net$"]},
    {"service": "Netlify", "status": "edge", "nxdomain": False,
     "fingerprint": r"Not Found - Request ID:", "cname": [r"\.netlify\.(?:app|com)$"]},
    {"service": "Zendesk", "status": "edge", "nxdomain": False,
     "fingerprint": r"Help Center Closed|this help center no longer exists", "cname": [r"\.zendesk\.com$"]},
    {"service": "Unbounce", "status": "edge", "nxdomain": False,
     "fingerprint": r"The requested URL was not found on this server\.", "cname": [r"\.unbouncepages\.com$"]},
    {"service": "Gitbook", "status": "edge", "nxdomain": False,
     "fingerprint": r"If you need specifics, here's the error|Domain not found", "cname": [r"\.gitbook\.io$"]},
    {"service": "Mashery", "status": "edge", "nxdomain": False,
     "fingerprint": r"Unrecognized domain <strong>", "cname": [r"\.mashery\.com$"]},
    {"service": "Tilda", "status": "edge", "nxdomain": False,
     "fingerprint": r"Please renew your subscription", "cname": [r"\.tilda\.ws$"]},
    {"service": "Vercel", "status": "edge", "nxdomain": False,
     "fingerprint": r"The deployment could not be found on Vercel|DEPLOYMENT_NOT_FOUND",
     "cname": [r"^cname\.vercel-dns\.com$", r"\.vercel\.app$"]},
    {"service": "Cloudflare Pages", "status": "edge", "nxdomain": True, "fingerprint": "",
     "cname": [r"\.pages\.dev$"]},
]
