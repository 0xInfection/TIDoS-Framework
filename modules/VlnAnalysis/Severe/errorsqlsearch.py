# coding: utf-8
#!/usr/bin/env python3

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This script is a part of TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import core.lib.mechanize as mechanize
from re import search, sub
import http.cookiejar
#import requests
import time
import urllib.request
import re
import os
import sys
from re import *
from urllib.request import *
from core.Core.colors import *
from core.methods.tor import session
from core.variables import tor
from time import sleep

from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

br = mechanize.Browser()

cj = http.cookiejar.LWPCookieJar()
br.set_cookiejar(cj)
torproxies = {'http':'socks5h://localhost:9050', 'https':'socks5h://localhost:9050'}
if tor:
    br.set_proxies(torproxies)
    
params = []

br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

class UserAgent(FancyURLopener):
    version = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'

useragent = UserAgent()
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

ctr=0
path_list = []
payloads = []

info = ""
searchinfo = ""
properties = {}

def errorsqlsearch(web):
    global name
    name = targetname(web)
    global lvl2
    lvl2 = "sqli"
    global module
    module = "VulnAnalysis"
    global lvl1
    lvl1 = "Critical Vulnerabilities"
    global lvl3
    lvl3 = "errorsqli"
    os.system('clear')
    #print(R+'\n    ======================================')
    print(R+'\n     S Q L i   H U N T E R (Auto Awesome)')
    print(R+'    ---<>----<>----<>----<>----<>----<>---\n')
                 
    print(R+'           [E R R O R   B A S E D] \n')
    with open('files/payload-db/errorsql_payloads.lst','r') as pay:
        for payload in pay:
            rem = payload.replace('\n','')
            payloads.append(rem)
    web0 = web.replace('https://','')
    web0 = web.replace('http://','')
    try:
        with open('tmp/logs/'+web0+'-logs/'+web0+'-links.lst','r') as ro:
            for r in ro:
                r = r.replace('\n','')
                path_list.append(r)
    except IOError:
        print(R+' [-] Path file not found!')
        br.open(web)
        for o in br.links():
            path_list.append(o.base_url+'/'+o.url)
        print(path_list)
    requests = session()
    success = []
    for bugs in path_list:
        spays = []
        ctr = 0
        print(B+' [*] Testing '+C+str(bugs))
        if '?' in str(bugs) and '=' in str(bugs):
            getrq = requests.get(bugs, verify=False)
            for p in payloads:
                bugs = bugs + str(p)
                print(B+" [*] Trying : "+C+ bugs)
                time.sleep(0.7)
                response = requests.get(bugs, verify=False)
                if 'error' in response.text or 'mysql' in response.text.lower():
                    print('\n'+G+' [+] Vulnerable link detected: ' + web)
                    print(R+' [*] Injecting Error SQLi payloads...')
                    print(B+' [!] PoC : ' + str(bugs))
                    spays.append(str(bugs))
                    print(R+" [!] Payload : " + O + p + '\033[0m')
                    #print("\033[1m [!] Code Snippet : \n\033[0m" + response.content + '\n')
                    ctr+= 1
                    break
            success += spays
        else:
            print(GR+' [-] Link without parameter : '+B+'' + str(bugs))
            time.sleep(0.2)
    if success:
        data = "SQLi Vulnerability (auto) found! PoCs: " + str(success)
    else:
        data = "(auto) no payload succeeded."
    save_data(database, module, lvl1, lvl2, lvl3, name, data)

def attack(web):
    web = web.fullurl
    errorsqlsearch(web)
