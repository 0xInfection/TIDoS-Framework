<p align="middle"><img src='https://i.imgur.com/QAbaVdU.png' /></p>

![Python](https://img.shields.io/badge/Python-2.7-green.svg) ![Supported OS](https://img.shields.io/badge/Supported%20OS-Linux-yellow.svg) ![License](https://img.shields.io/badge/License-GPLv3-blue.svg) ![Build](https://img.shields.io/badge/Build-0049-red.svg) ![Modules](https://img.shields.io/badge/Modules-73-blue.svg) ![Status](https://img.shields.io/badge/Build%20Status-passing-green.svg)

# TIDoS Framework 
TIDoS Framework is a comprehensive web application audit framework with some serious perks.

### Highlights :-
The main highlights of this framework is:
- [x] Basic first release (but huge).
- [x] Has 4 main phases, subdivided into __13 sub-phases__ containing total of __73 modules__.
- [x] Reconnaissance Phase has 26 modules of its own (including active, passive and information disclosure modules).
- [x] Scanning & Enumeration Phase has got 12 modules (including port scans, WAF analysis, etc)
- [x] Vulnerability Analysis Phase has 32 modules (including most common vulnerabilites in action.
- [x] Exploitation Phase has only 1 exploit. `(thats in alpha phase)`
- [x] All four phases each have a auto-awesome module which automates every module for you.
- [x] You just need the domain, and leave everything is to this tool.
- [x] TIDoS has full verbose out support, so you'll know whats going on.
- [x] User friendly interaction environment. `(no real shits)`

`Note:` For more info on various modules please refer to the [wiki](https://github.com/theinfecteddrake/TIDOS-Framework/wiki).

<img src='https://i.imgur.com/ZhBUrDB.png' />

### Installing TIDoS :-
* Clone the repository locally and navigate there:
```
git clone https://github.com/theinfecteddrake/tidos-framework.git
cd tidos-framework
```
* Install the dependencies:
```
chmod +x install
./install
```
<img src='https://i.imgur.com/B3eA0H5.png' />

Thats it! Now you are good to go! Now lets run the tool:
```
tidos
```

### Usage :-
TIDoS is made to be comprehensive. Its highly flexible framework where you just have to select and use modules. 

As the framework opens up, enter the website name `eg. http://www.example.com` and let TIDoS lead you. Thats it! Its as easy as that.

> Recommended:
> - Follow the order of the tool (Run in a schematic way).
>    `Reconnaissance ⤃ Scanning & Enumeration ⤃ Vulnerability Analysis`

### Flawless Features :-

TIDoS Framework presently supports the following:

- __Reconnaissance + OSINT__
    + Passive Reconnaissance:
	- Ping/Nping Enumeration
	- WhoIS Lookup
	- GeoIP Lookup
	- DNS Config. Lookup 
	- Subdomains Lookup
	- Reverse DNS Lookup
	- Reverse IP Lookup
	- Web Links Gatherer
	- Google Search (manual search)
	- Google Dorking (multiple modules) `automated`

    + Active Reconnaissance
	- HPing3 enumeration `(automated)`
	- CMS Detection `(185+ CMSs supported)`
	- Advanced Traceroute `IMPROVED`
	- Grab HTTP Headers
	- Detect Server `IMPROVED`
	- Examine SSL Certificate
	- `robots.txt` and `sitemap.xml` Checker
	- Subnets Enumeration
	- Find Shared DNS Hosts
	- Operaing System Fingerprint

    + Information Disclosure
	- Credit Cards Disclosure in Plaintext
	- Email Harvester
	- Fatal Errors Enumeration `Includes Full Path Disclosure checks`
	- Internal IP Disclosure
	- Phone Number Havester
	- Social Security Number Harvester

- __Scanning & Enumeration__

    + Remote Server WAF Analysis
    + Port Scanning `Ingenious Modules`
	- Simple Port Scanner `via Socket Connections`
	- TCP SYN Scan
	- TCP Connect Scan
	- XMAS Flag Scan 
	- Fin Flag Scan
	- Service Detector
    + Interactive Scanning with NMap `Preloaded multiple modules`
    + Crawlers
	- Depth 1
	- Depth 2 `IMPROVED`

- __Vulnerability Analysis__

    + Web-Bugs & Server Misconfigurations

	- Insecure CORS `iCORS`
	- Same-Site Scripting
	- Zone Transfer `DNS Server based`
	- Clickjacking `Framable Response`
	- Security on Cookies `HTTPOnly/Secure Flags`
	- Cloudflare Misconfiguration Check `+ Getting Real IP` 
	- HTTP High Transport Security Usage
	- Security Headers Analysis 
	- Cross-Site Tracing `(Port Based)`
	- Network Security Misconfig. `(Telnet Enabled)`

    - Serious Web Vulnerabilities

	+ File Intrusions
	    - Local File Intrusion (LFI)
	    - Remote File Inclusion (RFI)
	+ OS Command Execution `Linux & Windows (RCE)`
	+ Path Traversal (Sensitive Paths) 
	+ Cross-Site Request Forgery 
	+ SQL Injection
	    - Cookie Value Based
	    - Referer Value Based
	    - User-Agent Value Based
	+ Host Header Injection 
	+ Bash Command Injection `Shellshock` 
	+ Cross-Site Scripting `beta`
	    - Cookie Value Based
	    - Referer Value Based
	    - User-Agent Value Based

    - Auxillaries

	+ Protocol Credential Bruteforce `3 more under dev.`
	    - FTP Bruteforce
	    - SSH Bruteforce
	    - POP 2/3 Bruteforce
	    - SQL Bruteforce
	+ String & Payload Encoder
	    - URL Encode
	    - Base64 Encode
	    - HTML Encode
	    - Plain ASCII Encode
	    - Hex Encode
	    - Octal Encode
	    - Binary Encode
	    - GZip Encode

- __Exploitation__ `purely developmental`

	+ ShellShock

### Known Bugs:

This version of TIDoS is purely developmental `beta`. There are bugs in resolving the `[99] Back` at various end-points. Also TIDoS needs to develop more on logging all info displayed on the screen `(help needed)`.

### Final Words:

This project is one of the best frameworks I have ever built and I would really like your constructive criticism, suggestions and help in converting this project into the best web penetration testing framework ever built `and it will be ;)`.

> Thank you
> ✎ @_tID_
> [Team CodeSploit](https://www.facebook.com/codesploit)
