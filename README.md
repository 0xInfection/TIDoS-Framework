<h1 align="center">
  <img src='files/logo.png' height='500'></img><br>
  TIDoS
  <br>
</h1>

<p align="center">
  <a href="https://github.com/0xInfection/TIDoS-Framework/blob/master/TIDoS">
    <img src="https://img.shields.io/static/v1.svg?label=Version&message=2.0&color=lightgrey&style=flat-square&logo=dev.to&logoColor=white">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/static/v1.svg?label=Python&message=3.7%2B&color=lightgrey&style=flat-square&logo=python&logoColor=white">
  </a><br>
  The Offensive Web Application Penetration Testing Framework.
</p>

> __IMPORTANT__:
>
> The new Qt5 interface is complete, but has additional dependencies. Take a look at the updated installation instructions.

### Highlights :-
Here is some light on what the framework is all about:
-  A complete versatile framework to cover up everything from Reconnaissance to Vulnerability Analysis.
-  Has 5 main phases, subdivided into __14 sub-phases__ consisting a total of __108 modules__.
-  Reconnaissance Phase has 50 modules of its own (including active and passive recon, information disclosure modules).
-  Scanning & Enumeration Phase has got 16 modules (including port scans, WAF analysis, etc)
-  Vulnerability Analysis Phase has 37 modules (including most common vulnerabilities in action).
-  Exploits Castle has only 1 exploit. `(purely developmental)`
-  And finally, Auxiliaries have got 4 modules. `more under development`
-  All four phases each have an `Auto-Awesome` module which automates every module for you.
-  huge performance boost through multiprocessing
-  Piping Attacks through Tor (not implemented everywhere yet)
-  You just need the domain, and leave everything is to this tool.
-  TIDoS has full verbose out support, so you'll know whats going on.
-  Attacking now even easier with a new GUI

### Main new features
-  the programming language: TIDoS is fully ported to Python3
-  the interface: TIDoS presents a new, Metasploit-like console interface
-  Parallelisation: TIDoS uses multiprocessing to speed up attacks
-  An alternative CLI interface for faster interaction with one specific module
-  Anonymity: Attacking through Tor is possible (95% done)
-  Module Completion: Some modules have been feature-extended (e.g. more evasion, supporting more than 1 query parameter)
-  Some new modules: arpscan
-  A Graphical User Interface for easier interaction with the toolkit
-  Supports non-default http(s) ports

### Upcoming
-  results of modules will be stored in a database
-  new modules: nikto&photon

### Installation :-

#### Installation Script (Globally) :

To install the framework globally in /opt, run the provided `core/install.py` script as root. After this, you can launch TIDoS simply by typing `tidos` on the command line.

#### Manual Installation (Locally) :

* Clone the repository locally and navigate there:
```
git clone https://github.com/0xinfection/tidos-framework.git
cd tidos-framework
```

TIDoS needs some libraries to run, which can be installed via `aptitude` or `dnf` Package Managers.
```
sudo apt-get install libncurses5 libxml2 nmap tcpdump libexiv2-dev build-essential python3-pip libmariadbclient18 libmysqlclient-dev tor konsole
```
Now after these dependencies are finished installing, we need to install the remaining Python Package dependencies, hence run:
```
pip3 install -r requirements.txt
```

TIDoS uses Vailyn to scan for path traversals in a new, improved path traversal module. If you want to use that module, head to `https://github.com/VainlyStrain/Vailyn`, and follow the installation instructions there.

Thats it. You now have TIDoS at your service. Fire it up using:
```
python3 tidv2               #Qt5 interface
sudo python3 tidconsole.py  #console interface
```

#### Docker image :

You can build it from Dockerfile :
```
git clone https://github.com/0xinfection/tidos-framework.git
cd tidos-framework/core/docker
docker build -t tidos .
```

To run TIDoS :

```
docker run --interactive --tty --rm tidos bash
tidos
```

#### Updating TIDoS :

To get the current version of TIDoS, move into the installation folder and perform `(sudo) git pull  #sudo if installed by install.py`. Alternatively, you can run the `fetch` command in tidconsole.

### Getting Started :-

To get started, you need to set your own `API KEYS` for various OSINT & Scanning and Enumeration purposes. To do so, open up `API_KEYS.py` under `files/` directory and set your own keys and access tokens for `SHODAN`, `CENSYS`, `FULL CONTACT`, `GOOGLE` and `WHATCMS`.

> __GOOD NEWS__:
>
> The latest release of TIDoS includes all API KEYS and ACCESS TOKENS for `SHODAN`, `CENSYS`, `FULL CONTACT`, `GOOGLE` and `WHATCMS` by default. I found these tokens on various repositories on GitHub itself. __You can now use all the modules__ which use the API KEYS. :)

#### Commands :-

```
__                                                    __                                                        
 !  attack    Attack specified target(s)              M
 :  clear     Clear terminal.                         :
 V  creds     Handle target credentials.              
 :  fetch     Check for and install updates.          :
 :  find      Search a module.                        :
    help      Show help message.                      :
    info      Show description of current module.     M
 :  intro     Display Intro.                          :
 :  leave     Leave module.                           M
    list      List all modules of a category.         :
 :  load      Load module.                            :
 :  netinfo   Show network information.               :
 :  opts      Show options of current module.         M
    phpsploit Load the phpsploit framework.           :
              (needs to be downloaded externally)
 :  processes Set number of processes in parallelis.  :
    q         Terminate TIDoS session.                :
 :  sessions  Interact with cached sessions.          :
 :  set       Set option value of module.             M
 :  tor       Pipe Attacks through the Tor Network.   :
    vicadd    Add Target to list.                     :
    vicdel    Delete Target from list.                :
    viclist   List all targets.                       :

  Avail. Cmds
    M needs loaded modvle
    V [! potentially] need loaded target(s)
```

### Flawless Features :-

TIDoS presently supports the following: `and more modules are under active development`

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
	+ ARP Scanner `NEW`

* __Vulnerability Analysis__

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
	+ Path Traversal `ENHANCED`
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
	    - (XMPP Protocol Bruteforce) `BROKEN:DEP`
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
- `net_info.py` - Displays information about your network. Accessible from 'netinfo' command.

### TIDoS In Action:

Lets see a demonstration of TIDoS in action:

[![asciicast](https://asciinema.org/a/359477.svg)](https://asciinema.org/a/359477)

### Version:
```
v2.0.1-5 [latest release] [#beta]
```

### Disclaimer:

TIDoS is provided as an offensive web application audit framework. It has built-in modules which can reveal potential misconfigurations and vulnerabilties in web applications which could possibly be exploited maliciously.

__THEREFORE, NEITHER THE AUTHOR NOR THE CONTRIBUTORS ARE RESPONSIBLE FOR ANY MISUSE OR DAMAGE DUE TO THIS TOOLKIT.__

