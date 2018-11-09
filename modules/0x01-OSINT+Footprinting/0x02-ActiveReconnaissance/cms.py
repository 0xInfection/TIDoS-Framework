#!/usr/bin/env python
# coding:  utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import mechanize
import re
from re import *
import cookielib
import requests
import json
import time
import builtwith
from time import sleep
from core.Core.colors import *
import urllib2
from urllib2 import urlparse

br = mechanize.Browser()

cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

def getcmslook(web):

    global found
    global dtect
    global wordpress
    web = web.split('//')[1]
    print(GR+' [*] Passive Fingerprinting CMS...')
    time.sleep(1)
    print(O+' [!] Setting priority to False...')
    wordpress = False
    dtect = False
    print(GR+' [*] Importing token...')
    from files.API_KEYS import WHATCMS_ACCESS_TOKEN
    print(B+' [+] Token detected : '+C+WHATCMS_ACCESS_TOKEN)
    request = requests.get('https://whatcms.org/APIEndpoint/Detect?url=' + web + '&key=' + WHATCMS_ACCESS_TOKEN, verify=False)
    response = json.loads(request.text)

    status = response['result']['code']

    if 'retry_in_seconds' in response:
        print(R+' [-] Outbound Query Exception!')
    else:
        if status == 200:
            dtect = True
            print(G+' [+] CMS Detected: ' +O+ response['result']['name']+'\n')
        else:
            dtect = False

def cmsenum(web):

    print(GR+' [*] Active Fingerprinting CMS...\n')
    resp = builtwith.parse(web)
    print(O+' [*] Parsing raw-data...')
    time.sleep(0.7)
    res = json.dumps(resp)
    r = json.loads(res)
    try:
        if "cms" in r:
            print(G+' [+] CMS Detected :'+O+' %s' % (r['cms']))
            dtect = True
            time.sleep(0.7)

    except Exception as e:
        print(R+' [-] Error while CMS Enumeration...')
        print(R+' [-] Exception : '+str(e))

def cms(web):

    print(R+'\n   =========================')
    print(R+'    C M S   D E T E C T O R')
    print(R+'   =========================\n')
    time.sleep(0.4)
    print(GR+' [*] Parsing the web URL... ')
    time.sleep(0.4)

    print(O+' [!] URL successfully parsed !')
    time.sleep(0.2)
    getcmslook(web)
    cmsenum(web)

    if dtect == False:
        print(R+" [-] "+O + domain+R + " doesn't seem to use a CMS")
