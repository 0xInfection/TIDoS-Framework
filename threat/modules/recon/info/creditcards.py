#!/usr/bin/env python
from core.colors import color
from database.database_module import save_data
import inspect
import re
import sys
import lxml
import time
import requests
from bs4 import BeautifulSoup
sys.path.append('files/signature-db/')
from infodisc_signatures import EXPRESS_CARD_SIGNATURE
from infodisc_signatures import VISA_MASTERCARD_SIGNATURE
from infodisc_signatures import MASTERCARD_SIGNATURE, DISCOVER_CARD_SIGNATURE
from infodisc_signatures import VISA_SIGNATURE, AMEX_CARD_SIGNATURE
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


urls = []
links = []
found = 0x00

def credit0x00(host):
    print(color.green(' [+] Importing credit card signatures...'))
    links = [host.name]
    if '//' in host.name:
        site = host.name.split('//')[1]
    else:
        site=host.name
    for link in links:
        print(' [*] Scraping Page: '+color.yellow(site))
        req = requests.get(link).text
        check0x00(req)
    soup = BeautifulSoup(req,'lxml')
    #site='https://'+site
    for line in soup.find_all('a', href=True):
        newline = line['href']
        try:
            if newline[:4] == "http":
                if site in newline:
                    urls.append(str(newline))
            elif newline[:1] == "/":
                combline = site+newline
                urls.append(str(combline))
        except:
            print(color.red(' [-] Unhandled Exception Occured!'))
    try:
        for uurl in urls:
            print(color.green("\n [+] Scraping Page: "+color.yellow(uurl)))
            req = requests.get(uurl).text
            check0x00(req)
    except Exception as e: #requests.exceptions:
        print(color.red(' [-] Outbound Query Exception...'))
    if found == 0x00:
        print(color.red(' [-] No Credit Cards found disclosed in plaintext in source code!'))
    print(color.green(' [+] Scraping Done!'))


def check0x00(req):
    try:
        append_name = ' '.join(str(req.encode('utf-8')).strip())
    except UnicodeDecodeError:
        append_name = ' '.join(str(req.decode('utf-8')).strip())
    print(color.yellow(' [!] Reading response...'))
    print(color.green(' [*] Searching for credit cards...'))
    AMEX = re.match(AMEX_CARD_SIGNATURE, append_name)
    VISA = re.match(VISA_SIGNATURE, append_name)
    MASTERCARD = re.match(MASTERCARD_SIGNATURE, append_name)
    DISCOVER = re.match(DISCOVER_CARD_SIGNATURE, append_name)
    EXPRESS = re.match(EXPRESS_CARD_SIGNATURE, append_name)
    VISA_MASTERCARD = re.match(VISA_MASTERCARD_SIGNATURE, append_name)
    print(color.yellow(' [!] Matching signatures...'))
    try:
        if EXPRESS.group():
            print(color.green(" [+] Website has American Express Cards!"))
            print(color.yellow(' [!] Card : ') + color.green(EXPRESS.group()))
            found = 0x01
    except:
        pass
    try:
        if VISA_MASTERCARD.group():
            print(color.green(" [+] Website has a Visa-Master Card!"))
            print(color.yellow(' [!] Card : ') + color.green(VISA_MASTERCARD.group()))
            found = 0x01
    except:
        pass
    try:
        if MASTERCARD.group():
            print(color.green(" [+] Website has a Master Card!"))
            print(color.yellow(' [!] Card : ') + color.green(MASTERCARD.group()))
            found = 0x01
    except:
        pass
    try:
        if VISA.group():
            print(color.green(" [+] Website has a VISA card!"))
            print(color.yellow(' [!] Card : ') + color.green(VISA.group()))
            found = 0x01
    except:
        pass
    try:
        if AMEX.group():
            print(color.green(" [+] Website has a AMEX card!"))
            print(color.yellow(' [!] Card : ') + color.green(AMEX.group()))
            found = 0x01
    except:
        pass
    try:
        if DISCOVER.group():
            print(color.green(" [+] Website has a DISCOVER card!"))
            print(color.yellow(' [!] Card : ') + color.green(DISCOVER.group()))
            found = 0x01
    except:
        pass
    return

def creditcards(target):
    from core.build_menu import buildmenu
    for host in target:
        host.lvl2=inspect.stack()[0][3]
        host.lvl3=''
        credit0x00(host)
    try:
        input(color.blue(' [#] Press')+color.red(' Enter ')+color.blue('to continue... \n'))
        buildmenu(target,target[0].main_menu,'Main Menu','')
    except EOFError as e:  
        buildmenu(target,target[0].main_menu,'Main Menu','')
    return
