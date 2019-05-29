#!/usr/bin/env python
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import re
import sys
sys.path.append('files/signature-db/')
import lxml
import time
import requests
from core.Core.colors import *
urls = []
links = []
found = 0x00
from bs4 import BeautifulSoup
from infodisc_signatures import EXPRESS_CARD_SIGNATURE
from infodisc_signatures import VISA_MASTERCARD_SIGNATURE
from infodisc_signatures import MASTERCARD_SIGNATURE, DISCOVER_CARD_SIGNATURE
from infodisc_signatures import VISA_SIGNATURE, AMEX_CARD_SIGNATURE
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def credit0x00(url):

    print(G+' [+] Importing credit card signatures...')
    links = [url]
    po = url.split('//')[1]
    for w in links:
        print(GR+' [*] Scraping Page: '+O+url)
        req = requests.get(w).text
        check0x00(req)

    soup = BeautifulSoup(req,'lxml')
    for line in soup.find_all('a', href=True):
        newline = line['href']
        try:
            if newline[:4] == "http":
                if po in newline:
                    urls.append(str(newline))
            elif newline[:1] == "/":
                combline = url+newline
                urls.append(str(combline))
        except:
            print(R+' [-] Unhandled Exception Occured!')

    try:
        for uurl in urls:
            print(G+"\n [+] Scraping Page: "+O+uurl)
            req = requests.get(uurl).text
            check0x00(req)

    except requests.exceptions:
        print(R+' [-] Outbound Query Exception...')

    if found == 0x00:
        print(R+' [-] No Credit Cards found disclosed in plaintext in source code!')

    print(G+' [+] Scraping Done!')


def check0x00(req):

    try:
        append_name = ' '.join(req.encode('utf-8')).strip()
    except UnicodeDecodeError:
        append_name = ' '.join(req.decode('utf-8')).strip()
    print(O+' [!] Reading response...')
    print(GR+' [*] Searching for credit cards...')
    AMEX = re.match(AMEX_CARD_SIGNATURE, append_name)
    VISA = re.match(VISA_SIGNATURE, append_name)
    MASTERCARD = re.match(MASTERCARD_SIGNATURE, append_name)
    DISCOVER = re.match(DISCOVER_CARD_SIGNATURE, append_name)
    EXPRESS = re.match(EXPRESS_CARD_SIGNATURE, append_name)
    VISA_MASTERCARD = re.match(VISA_MASTERCARD_SIGNATURE, append_name)
    print(O+' [!] Matching signatures...')

    try:
        if EXPRESS.group():
            print(G+" [+] Website has American Express Cards!")
            print(O+' [!] Card : ' + GR+EXPRESS.group())
            found = 0x01

    except:
        pass

    try:
        if VISA_MASTERCARD.group():
            print(G+" [+] Website has a Visa-Master Card!")
            print(O+' [!] Card : ' + GR+VISA_MASTERCARD.group())
            found = 0x01

    except:
        pass

    try:
        if MASTERCARD.group():
            print(G+" [+] Website has a Master Card!")
            print(O+' [!] Card : ' + GR+MASTERCARD.group())
            found = 0x01

    except:
        pass

    try:
        if VISA.group():
            print(G+" [+] Website has a VISA card!")
            print(O+' [!] Card : ' + GR+VISA.group())
            found = 0x01

    except:
        pass

    try:
        if AMEX.group():
            print(G+" [+] Website has a AMEX card!")
            print(O+' [!] Card : ' + GR+AMEX.group())
            found = 0x01

    except:
        pass

    try:
        if DISCOVER.group():
            print(G+" [+] Website has a DISCOVER card!")
            print(O+' [!] Card : ' + GR+DISCOVER.group())
            found = 0x01

    except:
        pass

def creditcards(web):
    print('web_link'+web)
    print(GR+' [*] Initiating module...')
    time.sleep(0.5)
    print(R+'\n     ========================')
    print(R+'      CREDIT CARD DISCLOSURE')
    print(R+'     ========================\n')
    credit0x00(web)
