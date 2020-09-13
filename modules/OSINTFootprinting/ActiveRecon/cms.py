#!/usr/bin/env python3
# coding:  utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import core.lib.mechanize as mechanize
import re
from re import *
import http.cookiejar
import requests as wrn
from core.methods.tor import session
from core.variables import tor
import json
import time
import builtwith
from time import sleep
from core.Core.colors import *
import urllib.request
from urllib.request import urlparse
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module tries to determine if the target is running a CMS."
searchinfo = "CMS Detector"
properties = {}

br = mechanize.Browser()

cj = http.cookiejar.LWPCookieJar()
br.set_cookiejar(cj)

torproxies = {'http':'socks5h://localhost:9050', 'https':'socks5h://localhost:9050'}
if tor:
    br.set_proxies(torproxies)

br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
wrn.packages.urllib3.disable_warnings(InsecureRequestWarning)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

def getcmslook(web, name):
    requests = session()
    global found
    global dtect
    web = web.split('//')[1]
    print(GR+' [*] Passive Fingerprinting CMS...')
    time.sleep(1)
    print(C+' [!] Setting priority to False...')
    dtect = False
    print(GR+' [*] Importing token...')
    try:
        from files.API_KEYS import WHATCMS_ACCESS_TOKEN
        print(O+' [+] Token detected :'+C+color.TR3+C+G+WHATCMS_ACCESS_TOKEN+C+color.TR2+C)
        request = requests.get('https://whatcms.org/APIEndpoint/Detect?url=' + web + '&key=' + WHATCMS_ACCESS_TOKEN, verify=False)
        response = json.loads(request.text)
        status = response['result']['code']
        if 'retry' in response:
            print(R+' [-] Outbound Query Exception!')
        else:
            if status == 200:
                dtect = True
                print(O+' [+] CMS Detected:' +C+color.TR3+C+G+ response['result']['name']+C+color.TR2+C+'\n')
                save_data(database, module, lvl1, lvl2, lvl3, name, response['result']['name'])
            else:
                dtect = False
    except ImportError:
        print(R+' [-] No API Token detected. Skipping first module...')
        time.sleep(0.4)

def cmsenum(web, name):

    print(GR+' [*] Active Fingerprinting CMS...\n')
    resp = builtwith.parse(web)
    print(C+' [*] Parsing raw-data...')
    time.sleep(0.7)
    res = json.dumps(resp)
    r = json.loads(res)
    try:
        if "cms" in r:
            print(O+' [+] CMS Detected :'+C+color.TR3+C+G+'%s' % (r['cms'])+C+color.TR2+C)
            dtect = True
            save_data(database, module, lvl1, lvl2, lvl3, name, str(r['cms']))
            time.sleep(0.7)

    except Exception as e:
        print(R+' [-] Error while CMS Enumeration...')
        print(R+' [-] Exception : '+str(e))

def cms(web):
    global lvl1, lvl2, lvl3, module
    lvl2 = "cms"
    module = "ReconANDOSINT"
    lvl1 = "Active Reconnaissance"
    lvl3 = ""
    name = targetname(web)
    #print(R+'\n   =========================')
    #print(R+'    C M S   D E T E C T O R')
    #print(R+'   =========================\n')
    from core.methods.print import posintact
    posintact("cms detector") 
    time.sleep(0.4)
    print(GR+' [*] Parsing the web URL... ')
    time.sleep(0.4)
    print(C+' [!] Initiating Content Management System Detection!')
    getcmslook(web, name)
    cmsenum(web, name)
    if dtect == False:
        print(R+" [-] "+O+web+R + " doesn't seem to use a CMS")
        save_data(database, module, lvl1, lvl2, lvl3, name, "No CMS detected.")
    print(G+' [+] CMS Detection Module Completed!'+C+color.TR2+C)

def attack(web):
    web = web.fullurl
    cms(web)