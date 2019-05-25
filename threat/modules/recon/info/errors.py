#!/usr/bin/env python
from core.colors import color
from database.database_module import save_data
import inspect
import re
import sys
sys.path.append('files/signature-db/')
import time
import requests
from re import search
from bs4 import BeautifulSoup
from commonerror_signatures import patterns

urls = []
links = []
found = 0x00

def check0x00(content,url):

    for pattern in patterns:
        print(color.blue(' [!] Finding ')+pattern+' ...')
        time.sleep(0.005)
        if search(pattern, content):
            print(color.green(' [!] Possible error at ')+color.yellow(url))
            print(color.green(" [+] Found : \"%s\" at %s" % (pattern,url)))
            found = 0x01

def request(url):

    time.sleep(0.5)
    links = [url]
    if '//' in url:
        po = url.split('//')[1]
    for w in links:
        print(color.green(' [*] Scraping Page: ')+color.yellow(url))
        req = requests.get(w).text
        check0x00(req, url)

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
            print(color.red(' [-] Unhandled Exception Occured!'))

    try:
        for uurl in urls:
            print(color.green("\n [+] Scraping Page: ")+color.yellow(uurl))
            req = requests.get(uurl).text
            check0x00(req, url)

    except Exception as e:
        print(color.red(' [-] Outbound Query Exception...'))

    if found == 0x00:
        print(color.red('\n [-] No Errors found in Source Code!\n'))

    print(color.green(' [+] Scraping Done!'))

def errors(target):
    from core.build_menu import buildmenu
    for host in target:
        host.lvl2=inspect.stack()[0][3]
        host.lvl3=''
        request(host.name)
