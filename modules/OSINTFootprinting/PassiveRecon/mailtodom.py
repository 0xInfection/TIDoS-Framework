#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os
import sys
import requests as wrn
from core.methods.tor import session
import re
import time
from core.Core.colors import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

wrn.packages.urllib3.disable_warnings(InsecureRequestWarning)

info = "This module tries to find the domain for a given email address."
searchinfo = "Find domain from email"
properties = {}

def getRes0x00():
    requests = session()
    email = input(C+' [§] Enter the email :> '+R)
    if '@' in email and '.' in email:
        pass
    else:
        email = input(C+' [§] Enter a valid email :> '+R)

    print(GR+' [*] Setting headers... (behaving as a browser)...')
    time.sleep(0.7)
    headers =   {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
                 'Accept-Language':'en-US;',
                 'Accept-Encoding': 'gzip, deflate',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;',
                 'Connection':'close'}
    print(P+' [!] Making the no-verify request...'+C)
    time.sleep(0.5)
    url = "https://whoisology.com/search_ajax/search?action=email&value="+email+"&page=1&section=admin"
    result = ''
    try:
        result = requests.get(url, headers=headers, verify=False, timeout=10).content
        if result != '':
            regex = re.compile('whoisology\.com\/(.*?)">')
            stuff = regex.findall(result)
            if len(stuff) > 0:
                for line in stuff:
                    if line.strip() != '':
                        if '.' in line:
                            print(O+' [+] Received Domain :'+C+color.TR3+C+G+line+C+color.TR2+C)
            else:
                print(R+ " [-] Empty domain result for email : "+O+email+C)
    except Exception:
        print(R+" [-] Can't reach url...")
        print(R+' [-] Request timed out!')

def mailtodom():
    time.sleep(0.6)
    #print(R+'\n    ===============================')
    #print(R+'     E M A I L   T O   D O M A I N ')
    #print(R+'    ===============================\n')
    from core.methods.print import posintpas
    posintpas("email to domain")
    time.sleep(0.7)
    getRes0x00()

def attack(web):
    mailtodom()
