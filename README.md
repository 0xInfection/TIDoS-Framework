<p align="middle"><img src='https://i.imgur.com/QAbaVdU.png' /></p>

![Python](https://img.shields.io/badge/Python-2.7-green.svg) ![TIDoS](https://img.shields.io/badge/TIDoS-v1.1.1-blue.svg) ![Supported OS](https://img.shields.io/badge/Supported%20OS-Linux-yellow.svg) ![License](https://img.shields.io/badge/License-GPLv3-orange.svg) ![Build](https://img.shields.io/badge/Build-0074-red.svg) ![Modules](https://img.shields.io/badge/Modules-83-blue.svg) ![Status](https://img.shields.io/badge/Build%20Status-passing-green.svg) ![Stage](https://img.shields.io/badge/Release-Stable-brightgreen.svg)


# TIDoS Framework 
TIDoS Framework is a comprehensive web application audit framework. `let's keep this simple`

### Highlights :-
The main highlights of this framework is:
- [x] Basic first release (but huge).
- [x] Has 4 main phases, subdivided into __13 sub-phases__ containing total of __83 modules__.
- [x] Reconnaissance Phase has 29 modules of its own (including active reconnaissance, passive reconnaissance and information disclosure modules).
- [x] Scanning & Enumeration Phase has got 12 modules (including port scans, WAF analysis, etc)
- [x] Vulnerability Analysis Phase has 34 modules (including most common vulnerabilites in action.
- [x] Exploits Castle has only 1 exploit. `(alpha)`
- [x] All four phases each have a `auto-awesome` module which automates every module for you.
- [x] You just need the domain, and leave everything is to this tool.
- [x] TIDoS has full verbose out support, so you'll know whats going on.
- [x] User friendly interaction environment. `(no shits)`


<img src='https://i.imgur.com/ZhBUrDB.png' />

### Installing TIDoS :-
* Clone the repository locally and navigate there:
```
git clone https://github.com/theinfecteddrake/tidos.git
cd tidos
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
>
>    `Reconnaissance ➣ Scanning & Enumeration ➣ Vulnerability Analysis`

### Flawless Features :-

TIDoS Framework presently supports the following:

* __Reconnaissance + OSINT__

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
	    - Hacked Emails Lookup
	    - Google Dorking (multiple modules) `automated`
	    - Email to Domain Resolver
	    - Wayback Machine Lookups 

	+ Active Reconnaissance
	    - HPing3 enumeration `(under dev)`
	    - CMS Detection `(185+ CMSs supported)`
	    - Advanced Traceroute `IMPROVED`
	    - Grab HTTP Headers
	    - Detect Server `IMPROVED`
	    - Examine SSL Certificate
	    - `robots.txt` and `sitemap.xml` Checker
	    - Subnets Enumeration
	    - Find Shared DNS Hosts
	    - Operating System Fingerprinting `IMPROVED`

	+ Information Disclosure
	    - Credit Cards Disclosure in Plaintext
	    - Email Harvester
	    - Fatal Errors Enumeration `Includes Full Path Disclosure checks`
	    - Internal IP Disclosure
	    - Phone Number Havester
	    - Social Security Number Harvester

* __Scanning & Enumeration__

	+ Remote Server WAF Analysis
	+ Port Scanning `Ingenious Modules`
	    - Simple Port Scanner `via Socket Connections`
	    - TCP SYN Scan
	    - TCP Connect Scan
	    - XMAS Flag Scan 
	    - Fin Flag Scan
	    - Service Detector
	+ Interactive Scanning with NMap `16 modules`
	+ Crawlers
	    - Depth 1
	    - Depth 2 `IMPROVED`

+ __Vulnerability Analysis__

    __Web-Bugs & Server Misconfigurations__
    
	- Insecure CORS `iCORS`
	- Same-Site Scripting `Sub-domain based`
	- Zone Transfer `DNS Server based`
	- Clickjacking `Framable Response`
	- Security on Cookies `HTTPOnly/Secure Flags`
	- Cloudflare Misconfiguration Check `+ Getting Real IP` 
	- HTTP High Transport Security Usage
	- Spoofable Email `(Missing SPF and DMARC Records)`
	- Security Headers Analysis 
	- Cross-Site Tracing `(Port Based)`
	- Network Security Misconfig. `(Telnet Enabled)`
	
    __Serious Web Vulnerabilities__
    
	+ File Intrusions
	    - Local File Intrusion (LFI)
	    - Remote File Inclusion (RFI)
	+ OS Command Execution `Linux & Windows (RCE)`
	+ Path Traversal `(Sensitive Paths)`
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
	+ Unvalidated URL Forwards 
	+ CRLF Injection and HTTP Response Splitting

    __Auxillaries__

	+ Protocol Credential Bruteforce `3 more under dev.`
	    - FTP Bruteforce
	    - SSH Bruteforce
	    - POP 2/3 Bruteforce
	    - SQL Bruteforce
	    - XMPP Bruteforce
	    - SMTP Bruteforce
	    - TELNET Bruteforce
	    
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

This project is one of the best frameworks I have ever built and I would really like your constructive criticism, suggestions and help in converting this project into the best web penetration testing framework ever built `and trust me, it will be ;)`.

> Thank you,
>
> ✎ @_tID | Codesploit

