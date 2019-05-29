<!-- #∂ Welcome to MkDocs

For full documentation visit [mkdocs.org](https://mkdocs.org).

#∂#∂ Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs help` - Print this help message.

#∂#∂ Project layout

    mkdocs.yml    #∂ The configuration file.
    docs/
        index.md  #∂ The documentation homepage.
        ...       # Other markdown pages, images and other files. -->

# TIDoS Framework

## An OSCP & pentesting framework

Threat hunting / Exploitation / Analysis / Reporting

___

## Table of Contents

- [TIDoS Framework](#tidos-framework)
  - [An OSCP & pentesting framework](#an-oscp--pentesting-framework)
  - [Table of Contents](#table-of-contents)
  - [Project Layout](#project-layout)

___

## Project Layout

    TIDoS-FRAMEWORK/                    # Project Root (aka Threat/)
    ├── core/                           # Core Functionality (Menu builder, Multiprocessing, etc.)
    │   ├── build_menu.py
    │   ├── colors.py
    │   ├── functions.py
    │   ├── process.py
    │   └── useragents.py
    ├── db/                             # Database Functionality
    │   └── database.py
    ├── modules/                        # All Modules
    │   ├── enumeration/                # Enumeration Modules
    │   │   ├── scanenum.py
    │   │   └── scraper.py
    │   ├── exploitation/               # Exploitation Modules
    │   │   └── exploitation.py
    │   ├── recon/                      # Recon Modules
    │   │   ├── active/                 # Active Recon
    │   │   │   ├── altsites.py
    │   │   │   ├── apachestat.py
    │   │   │   ├── backbrute.py
    │   │   │   ├── backupbrute.py
    │   │   │   ├── cms.py
    │   │   │   ├── commentssrc.py
    │   │   │   ├── dav.py
    │   │   │   ├── dotbrute.py
    │   │   │   ├── filebrute.py
    │   │   │   ├── getports.py
    │   │   │   ├── grabhead.py
    │   │   │   ├── httpmethods.py
    │   │   │   ├── indexmulbrute.py
    │   │   │   ├── logbrute.py
    │   │   │   ├── passbrute.py
    │   │   │   ├── phpinfo.py
    │   │   │   ├── piwebenum.py
    │   │   │   ├── proxybrute.py
    │   │   │   ├── robot.py
    │   │   │   ├── serverdetect.py
    │   │   │   ├── sharedns.py
    │   │   │   ├── sslcert.py
    │   │   │   ├── subdom.py
    │   │   │   └── traceroute.py
    │   │   ├── active_recon.py
    │   │   ├── dig.py
    │   │   ├── info/                   # Info Gathering
    │   │   │   ├── creditcards.py
    │   │   │   ├── emailtext.py
    │   │   │   ├── errors.py
    │   │   │   ├── internalip.py
    │   │   │   ├── phone.py
    │   │   │   └── ssn.py
    │   │   ├── infodisc.py
    │   │   ├── passive/                # Passive Recon
    │   │   │   ├── censysdom.py
    │   │   │   ├── checkuser.py
    │   │   │   ├── dig.py
    │   │   │   ├── dnschk.py
    │   │   │   ├── getconinfo.py
    │   │   │   ├── getgeoip.py
    │   │   │   ├── googleSearch.py
    │   │   │   ├── googledorker.py
    │   │   │   ├── googlegroups.py
    │   │   │   ├── googlenum.py
    │   │   │   ├── gsearch.py
    │   │   │   ├── hackedmail.py
    │   │   │   ├── iphistory.py
    │   │   │   ├── linkedin.py
    │   │   │   ├── links.py
    │   │   │   ├── mailtodom.py
    │   │   │   ├── nping.py
    │   │   │   ├── pastebin.py
    │   │   │   ├── piweb.py
    │   │   │   ├── revdns.py
    │   │   │   ├── revip.py
    │   │   │   ├── subdom.py
    │   │   │   ├── subnet.py
    │   │   │   ├── threatintel.py
    │   │   │   ├── webarchive.py
    │   │   │   └── whois.py
    │   │   ├── passive_recon.py
    │   │   └── recon.py
    │   └── vulnysis/                   # Vulnerability Analysis
    │       └── vulnysis.py
    └── threat.py

___