#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import requests as wrn
from core.methods.tor import session
import socket
import time
from core.Core.colors import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

wrn.packages.urllib3.disable_warnings(InsecureRequestWarning)

info = "Find out if the target site is harmful or not."
searchinfo = "Threat Intelligence Module"
properties = {}

flaglist = []

def usom(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'Usom threatlist...')
    try:
        print(GR+' [*] Making a reverse DNS query...')
        print(G+' [+] DNS : '+O+ip)
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get('https://www.usom.gov.tr/url-list.txt', verify=False, timeout=10).content
        for i in str(resp).splitlines():
            if ip in i:
                flag = True
                flaglist.append("usom")
        if flag == True:
            print(R+' [+] '+O+web+G+' is harmful and has been reported on Usom...')
        else:
            print(G+' [+] '+O+web+G+' is clean as per Usom...')

    except Exception:
        print(R+' [-] Request to usom.gov.tr timed out!')
        pass

def badip(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'Bad IPs threatlist...')
    try:
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get("https://www.badips.com/get/info/"+str(ip), verify=False, timeout=10).content
        print(O+' [*] Parsing raw-data...')
        time.sleep(0.7)
        res = json.dumps(resp)
        r = json.loads(res)
        if r['Listed'] == 'True':
            flag = True
        else:
            flag = False

        if flag == True:
            print(R+' [+] '+O+web+G+' is harmful and has been reported on badips.com...')
            print(G+' [+] Bad IP : '+O+r['suc'])
            print(G+" [+] Country : "+O+r['CountryCode'])
            print(G+" [+] Report number: "+O+str(r['ReporterCount']['sum']))
            print(G+" [+] Category: " +O+r['Categories'][0])
            flaglist.append("badips")
        else:
            print(G+' [+] '+O+web+G+' is clean as per badips.com...')

    except Exception:
        print(R+' [-] Request to badips.com timed out!')
        pass

def blocklistssh(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'BlockLists SSH threatlist...')
    try:
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get('https://lists.blocklist.de/lists/ssh.txt', verify=False, timeout=10).text
        print(C+' [!] Parsing raw data...')
        time.sleep(0.5)
        for i in resp.splitlines():
            if ip in i:
                flag = True
        if flag == True:
            print(R+' [+] '+O+web+G+' has been reported for attacks on SSH services...')
            flaglist.append("blocklists: ssh threatlist")
        else:
            print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

    except Exception:
        print(R+' [-] Request to BlockLists timed out!')
        pass

def blocklistmail(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'BlockLists Mail threatlist...')
    try:
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get('https://lists.blocklist.de/lists/mail.txt', verify=False, timeout=10).text
        print(C+' [!] Parsing raw data...')
        time.sleep(0.5)
        for i in resp.splitlines():
            if ip in i:
                flag = True
        if flag == True:
            print(R+' [+] '+O+web+G+' has been reported for attacks on SMTP services...')
            flaglist.append("blocklists: smtp threatlist")
        else:
            print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

    except Exception:
        print(R+' [-] Request to BlockLists timed out!')
        pass

def blocklistapache(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'BlockLists APACHE threatlist...')
    try:
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get('https://lists.blocklist.de/lists/apache.txt', verify=False, timeout=10).text
        print(C+' [!] Parsing raw data...')
        time.sleep(0.5)
        for i in resp.splitlines():
            if ip in i:
                flag = True
        if flag == True:
            print(R+' [+] '+O+web+G+' has been reported for attacks on Apache services...')
            flaglist.append("blocklists: apache threatlist")
        else:
            print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

    except Exception:
        print(R+' [-] Request to BlockLists timed out!')
        pass

def blocklistimap(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'BlockLists IMAP threatlist...')
    try:
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get('https://lists.blocklist.de/lists/imap.txt', verify=False, timeout=10).text
        print(C+' [!] Parsing raw data...')
        time.sleep(0.5)
        for i in resp.splitlines():
            if ip in i:
                flag = True
        if flag == True:
            print(R+' [+] '+O+web+G+' has been reported for attacks on IMAP services...')
            flaglist.append("blocklists: imap threatlist")
        else:
            print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

    except Exception:
        print(R+' [-] Request to BlockLists timed out!')
        pass

def blocklistpop3(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'BlockLists POP3 threatlist...')
    try:
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get('https://lists.blocklist.de/lists/pop3.txt', verify=False, timeout=10).text
        print(C+' [!] Parsing raw data...')
        time.sleep(0.5)
        for i in resp.splitlines():
            if ip in i:
                flag = True
        if flag == True:
            print(R+' [+] '+O+web+G+' has been reported for attacks on POP3 services...')
            flaglist.append("blocklists: pop3 threatlist")
        else:
            print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

    except Exception:
        print(R+' [-] Request to BlockLists timed out!')
        pass

def blocklistftp(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'BlockLists FTP threatlist...')
    try:
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get('https://lists.blocklist.de/lists/ftp.txt', verify=False, timeout=10).text
        print(C+' [!] Parsing raw data...')
        time.sleep(0.5)
        for i in resp.splitlines():
            if ip in i:
                flag = True
        if flag == True:
            print(R+' [+] '+O+web+G+' has been reported for attacks on FTP services...')
            flaglist.append("blocklists: ftp threatlist")
        else:
            print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

    except Exception:
        print(R+' [-] Request to BlockLists timed out!')
        pass

def blocklistsip(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'BlockLists SIP & VoIP threatlist...')
    try:
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get('https://lists.blocklist.de/lists/sip.txt', verify=False, timeout=10).text
        print(C+' [!] Parsing raw data...')
        time.sleep(0.5)
        for i in resp.splitlines():
            if ip in i:
                flag = True
        if flag == True:
            print(R+' [+] '+O+web+G+' has been reported for attacks on SIP, VoIP services...')
            flaglist.append("blocklists: sip threatlist")
        else:
            print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

    except Exception:
        print(R+' [-] Request to BlockLists timed out!')
        pass

def blocklistbots(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'BlockLists Bots threatlist...')
    try:
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get('https://lists.blocklist.de/lists/bots.txt', verify=False, timeout=10).text
        print(C+' [!] Parsing raw data...')
        time.sleep(0.5)
        for i in resp.splitlines():
            if ip in i:
                flag = True
        if flag == True:
            print(R+' [+] '+O+web+G+' has been reported for attacks as HTTPD Bots, BAD Bots...')
            flaglist.append("blocklists: bots threatlist")
        else:
            print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

    except Exception:
        print(R+' [-] Request to BlockLists timed out!')
        pass

def blocklistirc(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'BlockLists IRC threatlist...')
    try:
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get('https://lists.blocklist.de/lists/ircbot.txt', verify=False, timeout=10).text
        print(C+' [!] Parsing raw data...')
        time.sleep(0.5)
        for i in resp.splitlines():
            if ip in i:
                flag = True
        if flag == True:
            print(R+' [+] '+O+web+G+' has been reported for attacks as IRC Bot...')
            flaglist.append("blocklists: irc threatlist")
        else:
            print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

    except Exception:
        print(R+' [-] Request to BlockLists timed out!')
        pass

def blockliststrong(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'BlockLists Strong threatlist...')
    try:
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get('https://lists.blocklist.de/lists/strongips.txt', verify=False, timeout=10).text
        print(C+' [!] Parsing raw data...')
        time.sleep(0.5)
        for i in resp.splitlines():
            if ip in i:
                flag = True
        if flag == True:
            print(R+' [+] '+O+web+G+' has been reported for attacks as Strong IPs...')
            flaglist.append("blocklists: strongips threatlist")
        else:
            print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

    except Exception:
        print(R+' [-] Request to BlockLists timed out!')
        pass

def blocklistbrute(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'BlockLists Bruteforce Login IPs threatlist...')
    try:
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get('https://lists.blocklist.de/lists/bruteforcelogin.txt', verify=False, timeout=10).text
        print(C+' [!] Parsing raw data...')
        time.sleep(0.5)
        for i in resp.splitlines():
            if ip in i:
                flag = True
        if flag == True:
            print(R+' [+] '+O+web+G+' has been reported for attacks via Bruteforce on services...')
            flaglist.append("blocklists: brute threatlist")
        else:
            print(G+' [+] '+O+web+G+' is clean as per BlockLists...')

    except Exception:
        print(R+' [-] Request to BlockLists timed out!')
        pass

def emergethreats(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'Emerging Threats latest threatlist...')
    try:
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get('http://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt', verify=False, timeout=10).text
        print(C+' [!] Parsing raw data...')
        time.sleep(0.5)
        for i in resp.splitlines():
            if ip in i:
                flag = True
        if flag == True:
            print(R+' [+] '+O+web+G+' is harmful and has been reported on Emerging Threats...')
            flaglist.append("emerging threats")
        else:
            print(G+' [+] '+O+web+G+' is clean as per Emerging Threats...')

    except Exception:
        print(R+' [-] Request to Emerging Threats timed out!')
        pass

def emergecompro(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'Emerging Threats comrpmised IPs threatlist...')
    try:
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get('http://rules.emergingthreats.net/blockrules/compromised-ips.txt', verify=False, timeout=10).text
        print(C+' [!] Parsing raw data...')
        time.sleep(0.5)
        for i in resp.splitlines():
            if ip in i:
                flag = True
        if flag == True:
            print(R+' [+] '+O+web+G+' is harmful and has been reported on Emerging Threats...')
            flaglist.append("emerging threats: compromised ips")
        else:
            print(G+' [+] '+O+web+G+' is clean as per Emerging Threats...')

    except Exception:
        print(R+' [-] Request to Emerging Threats timed out!')
        pass

def binarydefense(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'Binary Defense threatlist...')
    try:
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get('http://www.binarydefense.com/banlist.txt', verify=False, timeout=10).text
        print(C+' [!] Parsing raw data...')
        time.sleep(0.5)
        for i in resp.splitlines():
            if ip in i:
                flag = True
        if flag == True:
            print(R+' [+] '+O+web+G+' has a banned IP and has been reported on Binary Defense...')
            flaglist.append("binary defense")
        else:
            print(G+' [+] '+O+web+G+' is clean as per Binary Defense...')

    except Exception:
        print(R+' [-] Request to Binary Defense timed out!')
        pass

def openphish(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'openphish.com threatlist...')
    try:
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get('https://openphish.com/feed.txt', verify=False, timeout=10).text
        print(C+' [!] Parsing raw data...')
        time.sleep(0.5)
        for i in resp.splitlines():
            if ip in i:
                flag = True
        if flag == True:
            print(R+' [+] '+O+web+G+' is a harmful phishing site and has been reported on Open Phish...')
            flaglist.append("openphish")
        else:
            print(G+' [+] '+O+web+G+' is clean as per Open Phish...')

    except Exception:
        print(R+' [-] Request to Open Phish timed out!')
        pass

def zeustracker(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'zeustracker.com threatlist...')
    try:
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get('https://zeustracker.abuse.ch/blocklist.php?download=badips', verify=False, timeout=10).text
        print(C+' [!] Parsing raw data...')
        time.sleep(0.5)
        for i in resp.splitlines():
            if ip in i:
                flag = True
                break
        if flag == True:
            print(R+' [+] '+O+web+G+' is a harmful phishing site and has been reported on Zeus Tracker...')
            flaglist.append("zeustracker")
        else:
            print(G+' [+] '+O+web+G+' is clean as per Zeus Tracker...')

    except Exception:
        print(R+' [-] Request to zeustracker.com timed out!')
        pass

def projecthoneypot(web,ip):
    requests = session()
    print(O+'\n [!] Checking on '+G+'Project HoneyPot threatlist...')
    try:
        flag= False
        print(GR+' [*] Making the request...')
        resp = requests.get('https://www.projecthoneypot.org/list_of_ips.php', verify=False, timeout=10).text
        if str(ip) in resp:
            flag = True

        if flag == True:
            print(R+' [+] '+O+web+G+' is a harmful site and has been reported on Project HoneyPot...')
            flaglist.append("project honeypot")
        else:
            print(G+' [+] '+O+web+G+' is clean as per Project HoneyPot...')

    except Exception:
        print(R+' [-] Request to projecthoneypot.com timed out!')
        pass

def threatintel(web):
    name = targetname(web)
    module = "ReconANDOSINT"
    lvl1 = "Passive Reconnaissance & OSINT"
    lvl3=''
    lvl2=inspect.stack()[0][3]
    time.sleep(0.7)
    #print(R+'\n    =======================================')
    #print(R+'     T H R E A T   I N T E L L I G E N C E')
    #print(R+'    =======================================\n')
    from core.methods.print import posintpas
    posintpas("threat intelligence")
    print(O+' [Data in these threatlists is the latest data')
    print(O+'            not older than a week!]\n')
    print(C+' [!] Parsing Url..')
    time.sleep(0.7)
    web = web.replace('https://','')
    web = web.replace('http://','')
    if "@" in web:
        web = web.split("@")[1]
    print(O+' [!] Getting host information...')
    time.sleep(0.8)
    ip = socket.gethostbyname(web)
    print(G+' [+] DNS : '+O+str(ip))
    print(C+' [!] Loading up modules...')
    time.sleep(0.7)
    print(GR+' [*] Starting gathering...')
    usom(web,ip)
    badip(web,ip)
    blocklistssh(web,ip)
    blocklistmail(web,ip)
    blocklistsip(web,ip)
    blocklistftp(web,ip)
    blocklistpop3(web,ip)
    blocklistirc(web,ip)
    blocklistimap(web,ip)
    blocklistbots(web,ip)
    blockliststrong(web,ip)
    blocklistapache(web,ip)
    blocklistbrute(web,ip)
    emergethreats(web,ip)
    emergecompro(web,ip)
    binarydefense(web,ip)
    openphish(web,ip)
    zeustracker(web,ip)
    projecthoneypot(web,ip)
    if flaglist:
        data = web + " appeared as a threat on the following lists: " + str(flaglist)
    else:
        data = web + " seems to be clean."
    save_data(database, module, lvl1, lvl2, lvl3, name, data)
    print(G+' [+] Done!')

def attack(web):
    web = web.fullurl
    threatintel(web)
