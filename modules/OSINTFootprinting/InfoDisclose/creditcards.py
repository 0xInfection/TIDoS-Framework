#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/VainlyStrain/TIDoS


import re
import sys
sys.path.append('files/signaturedb/')
import lxml
import time
import requests as wrn
from core.methods.tor import session
from core.Core.colors import *
urls = []
links = []
found = 0x00
from bs4 import BeautifulSoup
from files.signaturedb.infodisc_signatures import EXPRESS_CARD_SIGNATURE
from files.signaturedb.infodisc_signatures import VISA_MASTERCARD_SIGNATURE
from files.signaturedb.infodisc_signatures import MASTERCARD_SIGNATURE, DISCOVER_CARD_SIGNATURE
from files.signaturedb.infodisc_signatures import VISA_SIGNATURE, AMEX_CARD_SIGNATURE
from requests.packages.urllib3.exceptions import InsecureRequestWarning
wrn.packages.urllib3.disable_warnings(InsecureRequestWarning)

info = "This module tries to find credit cards disclosed in the target's source code."
searchinfo = "Credit Card hunter"
properties = {}

def credit0x00(url):
    requests = session()
    print(C+' [+] Importing credit card signatures...')
    time.sleep(0.5)
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
            print("\n"+O+" [+] Scraping Page:"+C+color.TR3+C+G+uurl+C+color.TR2+C)
            req = requests.get(uurl).text
            check0x00(req)

    except:
        print(R+' [-] Outbound Query Exception...')

    if found == 0x00:
        print(R+' [-] No Credit Cards found disclosed in plaintext in source code!')

    print(G+' [+] Scraping Done!'+C+color.TR2+C)


def check0x00(req):

    try:
        append_name = ' '.join(req.encode('utf-8')).strip()
    except UnicodeDecodeError:
        append_name = ' '.join(req.decode('utf-8')).strip()
    print(C+' [!] Reading response...')
    print(GR+' [*] Searching for credit cards...')
    AMEX = re.match(AMEX_CARD_SIGNATURE, append_name)
    VISA = re.match(VISA_SIGNATURE, append_name)
    MASTERCARD = re.match(MASTERCARD_SIGNATURE, append_name)
    DISCOVER = re.match(DISCOVER_CARD_SIGNATURE, append_name)
    EXPRESS = re.match(EXPRESS_CARD_SIGNATURE, append_name)
    VISA_MASTERCARD = re.match(VISA_MASTERCARD_SIGNATURE, append_name)
    print(C+' [!] Matching signatures...')

    try:
        if EXPRESS.group():
            print(G+" [+] Website has American Express Cards!"+C+color.TR2+C)
            print(O+' [!] Card :' + C+color.TR3+C+G+EXPRESS.group()+C+color.TR2+C)
            found = 0x01

    except:
        pass

    try:
        if VISA_MASTERCARD.group():
            print(G+" [+] Website has a Visa-Master Card!"+C+color.TR2+C)
            print(O+' [!] Card :' +C+color.TR3+C+G+VISA_MASTERCARD.group()+C+color.TR2+C)
            found = 0x01

    except:
        pass

    try:
        if MASTERCARD.group():
            print(G+" [+] Website has a Master Card!"+C+color.TR2+C)
            print(O+' [!] Card :' + C+color.TR3+C+G+MASTERCARD.group()+C+color.TR2+C)
            found = 0x01

    except:
        pass

    try:
        if VISA.group():
            print(G+" [+] Website has a VISA card!"+C+color.TR2+C)
            print(O+' [!] Card :' + C+color.TR3+C+G+VISA.group()+C+color.TR2+C)
            found = 0x01

    except:
        pass

    try:
        if AMEX.group():
            print(G+" [+] Website has a AMEX card!"+C+color.TR2+C)
            print(O+' [!] Card :' + C+color.TR3+C+G+AMEX.group()+C+color.TR2+C)
            found = 0x01

    except:
        pass

    try:
        if DISCOVER.group():
            print(G+" [+] Website has a DISCOVER card!"+C+color.TR2+C)
            print(O+' [!] Card : ' + C+color.TR3+C+G+DISCOVER.group()+C+color.TR2+C)
            found = 0x01

    except:
        pass

def creditcards(web):

    print(GR+' [*] Initiating module...')
    time.sleep(0.5)
    #print(R+'\n     ========================')
    #print(R+'      CREDIT CARD DISCLOSURE')
    #print(R+'     ========================\n')
    from core.methods.print import pleak
    pleak("Credit card disclosure")
    credit0x00(web)

def attack(web):
    web = web.fullurl
    creditcards(web)