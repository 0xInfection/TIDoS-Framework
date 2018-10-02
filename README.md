<h1 align="center">
  <br>
  <a href="https://github.com/theinfecteddrake"><img src="https://i.imgur.com/QAbaVdU.png" alt="TIDoS"></a>
  <br>
  TIDoS Framework
  <br>
</h1>

<h4 align="center">The Offensive Web Application Penetration Testing Framework.</h4>

<p align="center">
  <a href="https://www.python.org/download/releases/2.7">
    <img src="https://img.shields.io/badge/Python-2.7-green.svg">
  </a>
  <a href="https://github.com/theInfectedDrake/TIDoS-Framework/releases">
    <img src="https://img.shields.io/badge/TIDoS-v1.6.1-blue.svg">
  </a>
  <a href="https://github.com/theinfecteddrake/tidos-framework/">
      <img src="https://img.shields.io/badge/Supported%20OS-Linux-yellow.svg">
  </a>
  <a href="https://github.com/theInfectedDrake/TIDoS-Framework/blob/master/doc/LICENSE/">
    <img src="https://img.shields.io/badge/License-GPLv3-orange.svg">
  </a>  
  <a href="https://github.com/theInfectedDrake/TIDoS-Framework/blob/master/CHANGELOG/">
    <img src="https://img.shields.io/badge/Build-0090-red.svg">
  </a>
  <a href="https://github.com/theInfectedDrake/TIDoS-Framework#flawless-features--">
    <img src="https://img.shields.io/badge/Modules-108-blue.svg">
  </a>
  <a href="https://github.com/theInfectedDrake/TIDoS-Framework/releases/tag/v1.6.1/">
    <img src="https://img.shields.io/badge/Build%20Status-passing-brightgreen.svg">
  </a>
  <a href="https://github.com/theInfectedDrake/TIDoS-Framework/releases/tag/v1.6.1/">
    <img src="https://img.shields.io/badge/Release-Stable-green.svg">
  </a>
</p>

### Highlights :-
Here is some light on what the framework is all about:
- [x] TIDoS Framework now boasts of a century+ of modules.
- [x] A complete versatile framework to cover up everything from Reconnaissance to Vulnerability Analysis.
- [x] Has 5 main phases, subdivided into __14 sub-phases__ consisting a total of <a href="https://github.com/theInfectedDrake/TIDoS-Framework/blob/master/doc/man/tree.man">__108 modules__</a>.
- [x] Reconnaissance Phase has 50 modules of its own (including active and passive recon, information disclosure modules).
- [x] Scanning & Enumeration Phase has got 16 modules (including port scans, WAF analysis, etc)
- [x] Vulnerability Analysis Phase has 37 modules (including most common vulnerabilites in action).
- [x] Exploits Castle has only 1 exploit. `(purely developmental)`
- [x] And finally, Auxillaries have got 4 modules. `under dev.`
- [x] All four phases each have a `Auto-Awesome` module which automates every module for you.
- [x] You just need the domain, and leave everything is to this tool.
- [x] TIDoS has full verbose out support, so you'll know whats going on.
- [x] Fully user friendly interaction environment. `(no shits)`

<img src='https://i.imgur.com/Gb30Y4k.gif' />

### Installation :-

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
<img src='https://i.imgur.com/zxZBUoW.gif' />

Thats it! Now you are good to go! Now lets run the tool:
```
tidos
```

### Getting Started :-

TIDoS is made to be comprehensive and versatile. It is a highly flexible framework where you just have to select and use modules.

But before that, you need to set your own `API KEYS` for various OSINT purposes. To do so, open up `API_KEYS.py` under `files/` directory and set your own keys and access tokens for `SHODAN`, `CENSYS`, `FULL CONTACT`, `GOOGLE` and `WHATCMS`. Public `API KEYS` and `ACCESS TOKENS` for `SHODAN` and `WHATCMS` have been provided with the TIDoS release itself. You can still add your own... `no harm!`

Finally, as the framework opens up, enter the website name `eg. http://www.example.com` and let TIDoS lead you. Thats it! Its as easy as that.

> Recommended:
> - Follow the order of the tool (Run in a schematic way).
>
>    `Reconnaissance ➣ Scanning & Enumeration ➣ Vulnerability Analysis`

To update this tool, use `tidos_updater.py` module under `tools/` folder.

### Flawless Features :-

TIDoS Framework presently supports the following: `and is under active development`

* __Reconnaissance + OSINT__

	+ Passive Reconnaissance:
	    - Nping Enumeration `Via external APi`
	    - WhoIS Lookup `Domain info gathering`
	    - GeoIP Lookup `Pinpoint physical location`
	    - DNS Configuration Lookup `DNSDump`
	    - Subdomains Lookup `Indexed ones`
	    - Reverse DNS Lookup `Host Instances`
	    - Reverse IP Lookup `Hosts on same server`
	    - Subnets Enumeration `Class Based`
	    - Domain IP History `IP Instances`
	    - Web Links Gatherer `Indexed ones`
	    - Google Search `Manual search`
	    - Google Dorking (multiple modules) `Automated`
	    - Email to Domain Resolver `Email WhoIs`
	    - Wayback Machine Lookups `Find Backups`
	    - Breached Email Check `Pwned Email Accounts`
	    - Enumeration via Google Groups `Emails Only`
	    - Check Alias Availability `Social Networks`
	    - Find PasteBin Posts `Domain Based`
	    - LinkedIn Gathering `Employees & Company`
	    - Google Plus Gathering `Domain Profiles`
	    - Public Contact Info Scraping `FULL CONTACT`
	    - Censys Intel Gathering `Domain Based`
	    - Threat Intelligence Gathering `Bad IPs`

	+ Active Reconnaissance
	    - Ping Enumeration `Advanced`
	    - CMS Detection `(185+ CMSs supported)` `IMPROVED`
	    - Advanced Traceroute `IMPROVED`
	    - `robots.txt` and `sitemap.xml` Checker
	    - Grab HTTP Headers `Live Capture`
	    - Find HTTP Methods Allowed `via OPTIONS`
	    - Detect Server Type `IMPROVED`
	    - Examine SSL Certificate `Absolute`
	    - Apache Status Disclosure Checks `File Based`
	    - WebDAV HTTP Enumeration `PROFIND & SEARCH`
	    - PHPInfo File Enumeration `via Bruteforce`
	    - Comments Scraper `Regex Based`
	    - Find Shared DNS Hosts `Name Server Based`
	    - Alternate Sites Discovery `User-Agent Based`
	    - Discover Interesting Files `via Bruteforce`
		    - Common Backdoor Locations `shells, etc.`
		    - Common Backup Locations `.bak, .db, etc.`
		    - Common Password Locations ` .pgp, .skr, etc.`
		    - Common Proxy Path Configs. `.pac, etc.`
		    - Multiple Index Paths `index, index1, etc.`
		    - Common Dot Files `.htaccess, .apache, etc`
		    - Common Logfile Locations `.log, .changelog, etc`

	+ Information Disclosure
	    - Credit Cards Disclosure `If Plaintext`
	    - Email Harvester `IMPROVED`
	    - Fatal Errors Enumeration `Includes Full Path Disclosure`
	    - Internal IP Disclosure `Signature Based`
	    - Phone Number Havester `Signature Based`
	    - Social Security Number Harvester `US Ones`

* __Scanning & Enumeration__

	+ Remote Server WAF Enumeration `Generic` `54 WAFs`
	+ Port Scanning `Ingenious Modules`
	    - Simple Port Scanner `via Socket Connections`
	    - TCP SYN Scan `Highly reliable`
	    - TCP Connect Scan `Highly Reliable`
	    - XMAS Flag Scan `Reliable Only in LANs`
	    - FIN Flag Scan `Reliable Only in LANs`
	    - Port Service Detector
	+ Web Technology Enumeration `Absolute`
	+ Complete SSL Enumeration `Absolute`
	+ Operating System Fingerprinting `IMPROVED`
	+ Banner Grabbing of Services `via Open Ports`
	+ Interactive Scanning with NMap `16 preloaded modules`
	+ Internet Wide Servers Scan `Using CENSYS Database`
	+ Web and Links Crawlers
	    - Depth 1 `Indexed Uri Crawler`
	    - Depth 2 `Single Page Crawler`
	    - Depth 3 `Web Link Crawler`

+ __Vulnerability Analysis__

    __Web-Bugs & Server Misconfigurations__
    
	+ Insecure CORS `Absolute`
	+ Same-Site Scripting `Sub-domain based`
	+ Zone Transfer `DNS Server based`
	+ Clickjacking 
		- Frame-Busting Checks
		- `X-FRAME-OPTIONS` Header Checks
	+ Security on Cookies
		- `HTTPOnly` Flag
		- `Secure` Flag on Cookies
	+ Cloudflare Misconfiguration Check
		- DNS Misconfiguration Checks
		- Online Database Lookup `For Breaches`
	+ HTTP Strict Transport Security Usage
		- HTTPS Enabled but no HSTS
	+ Domain Based Email Spoofing
		- Missing `SPF` Records
		- Missing `DMARC` Records
	+ Host Header Injection
		- Port Based Injection `via Web-Sockets`
		- `X-Forwarded-For` Header Injection
	+ Security Headers Analysis `Live Capture`
	+ Cross-Site Tracing `HTTP TRACE Method`
	+ Session Fixation `via Cookie Injection`
	+ Network Security Misconfig.
		- Checks for `TELNET` Enabled `via Port 23`
	
    __Serious Web Vulnerabilities__
    
	+ File Inclusions
	    - Local File Inclusion (LFI) `Param based`
	    - Remote File Inclusion (RFI) `IMPROVED`
	    	- Parameter Based
		     - Pre-loaded Path Based
	+ OS Command Injection `Linux & Windows (RCE)`
	+ Path Traversal `(Sensitive Paths)`
	+ Cross-Site Request Forgery `Absolute`
	+ SQL Injection 
	    + Error Based Injection
		    - Cookie Value Based
		    - Referer Value Based
		    - User-Agent Value Based
		    - Auto-gathering `IMPROVED`
	    + Blind Based Injection `Crafted Payloads`
		    - Cookie Value Based
		    - Referer Value Based
		    - User-Agent Value Based
		    - Auto-gathering `IMPROVED`
	+ LDAP Injection `Parameter Based`
	+ HTML Injection `Parameter Based`
	+ Bash Command Injection `ShellShock`
	+ Apache Struts Shock `Apache RCE`
	+ XPATH Injection `Parameter Based`
	+ Cross-Site Scripting `IMPROVED`
	    - Cookie Value Based
	    - Referer Value Based
	    - User-Agent Value Based
	    - Parameter Value Based `Manual`
	+ Unvalidated URL Forwards `Open Redirect`
	+ PHP Code Injection `Windows + Linux RCE`
	+ CRLF Injection `HTTP Response Splitting`
	    - User-Agent Value Based
	    - Parameter value Based `Manual`
	+ Sub-domain Takeover `50+ Services`
	    - Single Sub-domain `Manual`
	    - All Subdomains `Automated`

    __Other__

	+ PlainText Protocol Default Credential Bruteforce 

	    - FTP Protocol Bruteforce
	    - SSH Protocol Bruteforce
	    - POP 2/3 Protocol Bruteforce
	    - SQL Protocol Bruteforce
	    - XMPP Protocol Bruteforce
	    - SMTP Protocol Bruteforce
	    - TELNET Protocol Bruteforce

- __Auxillary Modules__

	+ Hash Generator `MD5, SHA1, SHA256, SHA512`
	+ String & Payload Encoder `7 Categories`
	+ Forensic Image Analysis `Metadata Extraction`
	+ Web HoneyPot Probability `ShodanLabs HoneyScore` 

- __Exploitation__ `purely developmental`

	+ ShellShock
	
### Other Tools:
- `net_info.py` - Displays information about your network. Located under `tools/`.
- `tidos_updater.py` - Updates the framework to the latest release via signature matching. Located under `tools/`.

### TIDoS In Action:

Lets see some screenshots of TIDoS in real world pentesting action:

<img src='https://i.imgur.com/78NuLE0.gif'></img>
<img src='https://i.imgur.com/j9Bl8mc.gif' width='33%'>  </img><img src='https://i.imgur.com/LeX5dOi.gif' width='33%'>  </img><img src='https://i.imgur.com/2BPvLRu.gif' width='33%'></img>

<img src='https://i.imgur.com/wLyefRk.gif'></img>
<img src='https://i.imgur.com/YL4mbgu.gif' width='33%'>  </img><img src='https://i.imgur.com/ccnL1wo.gif' width='33%'>  </img><img src='https://i.imgur.com/GswFCse.gif' width='33%'> </img>

<img src='https://i.imgur.com/iMqvozm.gif'></img>
<img src='https://i.imgur.com/SdDgG8Q.gif' width='50%'></img><img src='https://i.imgur.com/f5p0DJ1.gif' width='50%'>
<img src='https://i.imgur.com/ltETFN8.gif' width='33%'>  </img><img src='https://i.imgur.com/d7UIuYw.gif' width='33%'>  </img><img src='https://i.imgur.com/tvsqDOS.gif' width='33%'> </img>

### Version:
```
v1.6.1 [latest release] [#stable]
```

### Upcoming:

There are some bruteforce modules to be added:
- Some more of Enumeraton & Information Disclosure modules.
- Lots more of OSINT & Stuff (let that be a suspense).
- More of Auxillary Modules.
- Some Exploits are too being worked on.

### Ongoing:

- Working on a full-featured Web UI implementation on Flask and MongoDB and Node.js.
- Working on a new framework, a real framework. `To be released with v2`
- Working on a campaign feature + addition of arguments.
- Normal Bug Fixing Stuffs. `As per the issues being raised`
- Some other perks:
	- Working on a way for contributing new modules easily.
	- A complete new method of multi-threaded fuzzing.
	- Keeping better of new console stuff.

### Disclaimer:

TIDoS is provided as a offensive web application audit framework. It has built-in modules which can reveal potential misconfigurations and vulnerabilties in web applications which could possibly be exploited maliciously. 

__THEREFORE, I AM NOT EXCLUSIVELY RESPONSIBLE FOR ANY MISUSE OF THIS TOOLKIT.__

### Final Words:

This project is presently under active development so you may want to put it on a watch, since it is updated frequently `(you can take a look at past commits history)`. This project is one of the best frameworks I have ever built and I would really like your constructive criticism, suggestions and help in converting this project into the best web penetration testing framework ever built `and trust me, it will be ;)`.

> __TEMPORARY UPDATE__:
> 
> Please avoid doing pull requests temporarily, since work on v2 of this framework has already begun, which actually will fix the shitty code which I casually wrote all the way through. :)

Got any suggestions? Encountering bugs with this framework? Raise up an [issue](https://github.com/theInfectedDrake/TIDoS-Framework/issues/new) or hit me up via DM on [twitter](https://twitter.com/infecteddrake).

> Copyright © __The Infected Drake__.


