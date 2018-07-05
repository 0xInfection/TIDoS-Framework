<p align="middle"><img src='https://i.imgur.com/QAbaVdU.png' /></p>

![Python](https://img.shields.io/badge/Python-2.7-green.svg) ![TIDoS](https://img.shields.io/badge/TIDoS-v1.3-blue.svg) ![Supported OS](https://img.shields.io/badge/Supported%20OS-Linux-yellow.svg) ![License](https://img.shields.io/badge/License-GPLv3-orange.svg) ![Build](https://img.shields.io/badge/Build-0080-red.svg) ![Modules](https://img.shields.io/badge/Modules-91-blue.svg) ![Status](https://img.shields.io/badge/Build%20Status-passing-brightgreen.svg) ![Stage](https://img.shields.io/badge/Release-Stable-green.svg)


# TIDoS Framework 
TIDoS Framework is a comprehensive web application audit framework. `let's keep this simple`

### Highlights :-
The main highlights of this framework is:
- [x] Basic first release (but huge).
- [x] Has 4 main phases, subdivided into __13 sub-phases__ containing total of __91 modules__.
- [x] Reconnaissance Phase has 33 modules of its own (including active and passive reconnaissance, and information disclosure modules).
- [x] Scanning & Enumeration Phase has got 26 modules (including port scans, WAF analysis, etc)
- [x] Vulnerability Analysis Phase has 31 modules (including most common vulnerabilites in action.
- [x] Exploits Castle has only 1 exploit. `(purely developemental)`
- [x] All four phases each have a `Auto-Awesome` module which automates every module for you.
- [x] You just need the domain, and leave everything is to this tool.
- [x] TIDoS has full verbose out support, so you'll know whats going on behind.
- [x] Fully user friendly interaction environment. `(no shits)`


<img src='https://i.imgur.com/AcErfM9.png' />

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
<img src='https://i.imgur.com/3JrbOPH.png' />

Thats it! Now you are good to go! Now lets run the tool:
```
tidos
```

### Usage :-
TIDoS is made to be comprehensive. It is a highly flexible framework where you just have to select and use modules. 

As the framework opens up, enter the website name `eg. http://www.example.com` and let TIDoS lead you. Thats it! Its as easy as that.

> Recommended:
> - Follow the order of the tool (Run in a schematic way).
>
>    `Reconnaissance ➣ Scanning & Enumeration ➣ Vulnerability Analysis`

To update this tool, use `tidos_updater.py` module under `tools/` folder.

### Flawless Features :-

TIDoS Framework presently supports the following:

* __Reconnaissance + OSINT__

	+ Passive Reconnaissance:
	    - Nping Enumeration `Via external APi`
	    - WhoIS Lookup `Domain info gathering`
	    - GeoIP Lookup `Pinpoint physical location`
	    - DNS Configuration Lookup `DNSDump`
	    - Subdomains Lookup `Indexed ones`
	    - Reverse DNS Configuration Lookup
	    - Reverse IP Lookup `Hosts on same server`
	    - Web Links Gatherer `Indexed ones`
	    - Google Search `Manual search`
	    - Google Dorking (multiple modules) `Automated`
	    - Email to Domain Resolver `Email WhoIs`
	    - Wayback Machine Lookups `Find Backups`
	    - Breached Email Check `Pwned Email Accounts`
	    - Enumeration via Google Groups 
	    - Check Alias Availability `Social Networks`
	    - Find PasteBin Posts `Domain Based`
	    - LinkedIn Gathering `Employees & Company`

	+ Active Reconnaissance
	    - Ping enumeration `Advanced`
	    - CMS Detection `(185+ CMSs supported)`
	    - Advanced Traceroute `IMPROVED`
	    - Grab HTTP Headers `Live Capture`
	    - Detect Server `IMPROVED`
	    - Examine SSL Certificate `Absolute`
	    - `robots.txt` and `sitemap.xml` Checker
	    - Subnets Enumeration `Class Based`
	    - Find Shared DNS Hosts `Name Server Based`
	    - Operating System Fingerprinting `IMPROVED`

	+ Information Disclosure
	    - Credit Cards Disclosure `If Plaintext`
	    - Email Harvester `IMPROVED`
	    - Fatal Errors Enumeration `Includes Full Path Disclosure`
	    - Internal IP Disclosure `Signature Based`
	    - Phone Number Havester `Signature Based`
	    - Social Security Number Harvester `US Ones`

* __Scanning & Enumeration__

	+ Remote Server WAF Analysis
	+ Port Scanning `Ingenious Modules`
	    - Simple Port Scanner `via Socket Connections`
	    - TCP SYN Scan `Highly reliable`
	    - TCP Connect Scan `Highly Reliable`
	    - XMAS Flag Scan `Reliable Only in LANs`
	    - Fin Flag Scan `Reliable Only in LANs`
	    - Port Service Detector
	+ Web Technology Enumeration `Absolute`
	+ Interactive Scanning with NMap `16 preloaded modules`
	+ Crawlers
	    - Depth 1
	    - Depth 2 `IMPROVED`

+ __Vulnerability Analysis__

    __Web-Bugs & Server Misconfigurations__
    
	- Insecure CORS `Absolute`
	- Same-Site Scripting `Sub-domain based`
	- Zone Transfer `DNS Server based`
	- Clickjacking `Framable response based`
	- Security on Cookies `HTTPOnly/Secure Flags`
	- Cloudflare Misconfiguration Check `+ Getting Real IP` 
	- HTTP High Transport Security Usage
	- Spoofable Email `Missing SPF and DMARC Records`
	- Security Headers Analysis `Live Capture`
	- Cross-Site Tracing `Port Based`
	- Network Security Misconfig. `Telnet Enabled`
	
    __Serious Web Vulnerabilities__
    
	+ File Intrusions
	    - Local File Intrusion (LFI) `Param based`
	    - Remote File Inclusion (RFI)
	    	- Parameter Based
		- Pre-loaded Path Based
	+ OS Command Injection `Linux & Windows (RCE)`
	+ Path Traversal `(Sensitive Paths)`
	+ Cross-Site Request Forgery `Absolute`
	+ SQL Injection
	    - Cookie Value Based
	    - Referer Value Based
	    - User-Agent Value Based
	    - Auto-gathering `IMPROVED`
	    - Parameter Based `Manual`
	+ Host Header Injection `port based`
	+ Bash Command Injection `Shellshock` 
	+ Cross-Site Scripting `beta`
	    - Cookie Value Based
	    - Referer Value Based
	    - User-Agent Value Based
	    - Parameter Value Based `Manual`
	+ Unvalidated URL Forwards `Open Redirect`
	+ CRLF Injection and HTTP Response Splitting
	    - User-Agent Value Based
	    - Parameter value Based `Manual`

    __Auxillaries__

	+ Protocol Credential Bruteforce 

	    - FTP Protocol Bruteforce
	    - SSH Protocol Bruteforce
	    - POP 2/3 Protocol Bruteforce
	    - SQL Protocol Bruteforce
	    - XMPP Protocol Bruteforce
	    - SMTP Protocol Bruteforce
	    - TELNET Protocol Bruteforce
	    
	+ String & Payload Encoder
	
	    - URL Character Encoding
	    - Base64 Character Encoding
	    - HTML Character Encoding
	    - Plain ASCII Character Encoding
	    - Hex Character Encoding
	    - Octal Character Encoding
	    - Binary Character Encoding
	    - GZip Character Encoding

- __Exploitation__ `purely developmental`

	+ ShellShock

### Upcoming:

There are some bruteforce modules to be added:
- Common Backups
- Common Password Locations
- Common Dot files `(eg. .htaccess)`
- Interesting Directories
- Interesting Filepaths
- Lots more of OSINT

### Known Bugs:

This version of TIDoS is purely developmental and is presently `stable`. There are bugs in resolving the `[99] Back` at various end-points which results in blind fall-backs. Though I have added global exception handling, still, there maybe bugs out there. Also TIDoS needs to develop more on logging all info displayed on the screen `(help needed)`.

### Final Words:

Put this project on a watch, since it is updated frequently `(you can take a look at past commits history)`. This project is one of the best frameworks I have ever built and I would really like your constructive criticism, suggestions and help in converting this project into the best web penetration testing framework ever built `and trust me, it will be ;)`.

> Thank you,
>
> @_tID | CodeSploit

