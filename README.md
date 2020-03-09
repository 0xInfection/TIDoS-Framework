<h1 align="center">
  <br>
  <a href="https://github.com/0xinfection"><img src="https://i.imgur.com/QAbaVdU.png" alt="TIDoS"></a>
  <br>
  The TIDoS Framework
  <br>
</h1>

<h4 align="center">The Offensive Web Application Penetration Testing Framework.</h4>

<p align="center">
  <a href="https://www.python.org/download/releases/2.7">
    <img src="https://img.shields.io/badge/Python-2.7-green.svg">
  </a>
  <a href="https://github.com/0xinfection/TIDoS-Framework/releases">
    <img src="https://img.shields.io/badge/TIDoS-v1.7-blue.svg">
  </a>
  <a href="https://github.com/0xinfection/tidos-framework/">
      <img src="https://img.shields.io/badge/Supported%20OS-Linux-yellow.svg">
  </a>
  <a href="https://github.com/0xinfection/TIDoS-Framework/blob/master/doc/LICENSE/">
    <img src="https://img.shields.io/badge/License-GPLv3-orange.svg">
  </a> 
  <a href="https://github.com/0xinfection/TIDoS-Framework#flawless-features--">
    <img src="https://img.shields.io/badge/Modules-108-red.svg">
  </a>
  <a href="https://travis-ci.org/0xinfection/TIDoS-Framework">
    <img src="https://img.shields.io/badge/Build-Passing-brightgreen.svg?logo=travis">
  </a>
  <a href="https://github.com/0xinfection/TIDoS-Framework/releases/tag/v1.7/">
    <img src="https://img.shields.io/badge/Release-Stable-green.svg">
  </a>
</p>

### Highlights :-
Here is some light on what the framework is all about:
- [x] A complete versatile framework to cover up everything from Reconnaissance to Vulnerability Analysis.
- [x] Has 5 main phases, subdivided into __14 sub-phases__ consisting a total of <a href="https://github.com/0xinfection/TIDoS-Framework/blob/master/doc/man/tree.man">__108 modules__</a>.
- [x] Reconnaissance Phase has 50 modules of its own (including active and passive recon, information disclosure modules).
- [x] Scanning & Enumeration Phase has got 16 modules (including port scans, WAF analysis, etc)
- [x] Vulnerability Analysis Phase has 37 modules (including most common vulnerabilites in action).
- [x] Exploits Castle has only 1 exploit. `(purely developmental)`
- [x] And finally, Auxillaries have got 4 modules. `more under development`
- [x] All four phases each have a `Auto-Awesome` module which automates every module for you.
- [x] You just need the domain, and leave everything is to this tool.
- [x] TIDoS has full verbose out support, so you'll know whats going on.
- [x] Fully user friendly interaction environment. `(no shits)`

<img src='https://i.imgur.com/Gb30Y4k.gif' />

### Installation :-

#### Global Installation:

> __NOTE:__
>
> Presently, for installing globally, you will need to default your Python version to 2.x.
> However, the work of migration from Python2 to Python3 is already underway.

* Clone the repository locally and navigate there:
```
git clone https://github.com/0xinfection/tidos-framework.git
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

#### Manual Installation (Locally) :

TIDoS needs some libraries to run, which can be installed via `aptitude` or `yum` Package Managers.
```
sudo apt-get install libncurses5 libxml2 nmap tcpdump libexiv2-dev build-essential python-pip python-xmpp
```
Now after these dependencies are finished installing, we need to install the remaining Python Package dependencies, hence run:
```
pip2 install -r requirements.txt
```
Thats it. You now have TIDoS at your service. Fire it up using:
```
python2 tidos.py
```

#### Docker image :

You can build it from Dockerfile :
```
git clone https://github.com/0xinfection/tidos-framework.git
cd tidos-framework/docker
docker build -t tidos .
```

To run TIDoS :

```
docker run --interactive --tty --rm tidos bash
tidos
```

### Getting Started :-

TIDoS is built to be a comprehensive, flexible and versatile framework where you just have to select and use modules.

So to get started, you need to set your own `API KEYS` for various OSINT & Scanning and Enumeration purposes. To do so, open up `API_KEYS.py` under `files/` directory and set your own keys and access tokens for `SHODAN`, `CENSYS`, `FULL CONTACT`, `GOOGLE` and `WHATCMS`.

> __GOOD NEWS__:
>
> The latest release of TIDoS includes all API KEYS and ACCESS TOKENS for `SHODAN`, `CENSYS`, `FULL CONTACT`, `GOOGLE` and `WHATCMS` by default. I found these tokens on various repositories on GitHub itself. __You can now use all the modules__ which use the API KEYS. :)

Finally, as the framework opens up, enter the website name `eg. http://www.example.com` and let TIDoS lead you. Thats it! Its as easy as that.

> Recommended:
> - Follow the order of the tool (Run in a schematic way).
> ```
> Reconnaissance ➣ Scanning & Enumeration ➣ Vulnerability Analysis
> ```

To update this tool, use `tidos_updater.py` module under `tools/` folder.

### Flawless Features :-

TIDoS Framework presently supports the following: `and more modules are under active development`

* __Reconnaissance + OSINT__

	+ __Passive Reconnaissance:__
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

	+ __Active Reconnaissance:__
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

	+ __Information Disclosure:__
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
		- Port Based `Web Socket Based`
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
v1.7 [latest release] [#stable]
```

### Upcoming:

These are some modules which I have thought of adding:
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
	- A complete new method of multi-threaded fuzzing of parameters.
	- Keeping better of new console stuff.

### Disclaimer:

TIDoS is provided as a offensive web application audit framework. It has built-in modules which can reveal potential misconfigurations and vulnerabilties in web applications which could possibly be exploited maliciously.

__THEREFORE, THE AUTHOR AND NEITHER THE CONTRIBUTORS ARE NOT EXCLUSIVELY RESPONSIBLE FOR ANY MISUSE OR DAMAGE DUE TO THIS TOOLKIT.__

### Final Words:

This project is a very fresh and new project which just simply springed off my mind, and is presently under active development so you may want to put it on a watch, since it is updated frequently.

TIDoS is an in progress work far from perfection and I admit that there may be bugs out there which may cause many modules not to work properly and just bug out. However, being the only single author and maintainer behind this framework, it is my humble request to all users of this framework to hand me the list of modules via raising a [new issue](https://github.com/0xInfection/TIDoS-Framework/issues/new) which simply do not work and bug out, and I would be more than happy to fix them as we jointly make our journey to realising TIDoS as the greatest web penetration testing framework ever built.

Got more suggestions or new ideas? Raise up an [issue](https://github.com/0xinfection/TIDoS-Framework/issues/new) or hit me up via DM on [twitter](https://twitter.com/0xinfection).

> Copyright © [__Infected Drake__](https://twitter.com/0xinfection)
