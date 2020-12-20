#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import time
import os
import re
import sys
import tld
import socket
from core.methods.tor import session
from time import sleep
from bs4 import BeautifulSoup
from tld import get_tld
from core.Core.colors import *

sublist = []
flist = []
found = []
total = []

info = ""
searchinfo = ""
properties = {}

def subdombrute(web):

    try:
        try:
            print(GR+' [*] Importing wordlist path to be bruteforced... "files/subdomains.lst"')
            with open('files/fuzz-db/subdomain_paths.lst','r') as lol:
                for path in lol:
                    a = path.strip("\n")
                    sublist.append(a)
        except IOError:
            print(R+' [-] Wordlist not found!')

    except Exception as f:
        print(R+' [-] Exception : '+str(f))

    global found
    if 'http://' in web:
        web = web.replace('http://','')
    elif 'https://' in web:
        web = web.replace('https://','')
    else:
        pass

    if len(sublist) > 0:
        for m in sublist:
            furl = str(m) + '.' + str(web)
            flist.append(furl)

    if flist:
        time.sleep(0.5)
        print(R+'\n      B R U T E F O R C E R')
        print(R+'     ---<>----<>----<>----<>\n')

        print(GR+' [*] Bruteforcing for possible subdomains...')
        for url in flist:
            if 'http://' in url:
                url = url.replace('http://','')
            elif 'https://' in url:
                url = url.replace('https://','')
            else:
                pass
            try:
                ip = socket.gethostbyname(url)
                print(G+'\n [!] Subdomain Found : '+O+url+P+' ['+str(ip)+']')
                found.append(url)
            except Exception:
                sys.stdout.write(B+'\r [*] Checking : '+C+url)
                sys.stdout.flush()
    else:
        print(R+' [-] No wordlist found under tmp/.')
        print(R+' [-] Fatal Exception!')
    return found

def outer(web):
    requests = session()
    global final
    final = []
    wew = []
    time.sleep(0.4)
    print(R+'\n    A P I   R E T R I E V E R  ')
    print(R+'   ---<>----<>----<>----<>----')

    print(GR + color.BOLD + ' [!] Retriving subdomains...')
    time.sleep(0.4)
    print(""+ GR + color.BOLD + " [~] Result: "+ color.END)
    dom = 'http://' + web
    text = requests.get('http://api.hackertarget.com/hostsearch/?q=' + dom).text
    result = str(text)
    while 'error' not in result:
        print(G + result)
        mopo = result.splitlines()
        for mo in mopo:
            ro = mo.split(',')[0]
            print(G+' [+] Received : '+ro)
            final.append(str(ro))

def report(web, found, final):

    print(R+'\n   R E P O R T')
    print(R+'  ---<>----<>--\n')

    if ((len(found) > 0) or (len(final) > 0)):
        print(O+' [!] Subdomains found for '+G+web)
        print(C+'  |')
        for m in found:
            print(C+ '  +-- ' +GR+ m)
            total.append(m)
        for p in final:
            if p not in found:
                print(C+ '  +-- '+GR+p)
                total.append(p)

    else:
        print(R+' [-] No Subdomains found for ' + O+web)
    print('\n')
    return total

def subdom0x00(web):

    global fileo

    if 'http' in web:
        web = web.replace('http://','')
        web = web.replace('https://','')
    webb = web
    if "@" in web:
        webb = web.split("@")[1]
    try:
        fileo = 'tmp/'+webb+'-subdomains.lst'
        p = open(fileo,'w+')
        p.close
        print(R+'\n    S U B D O M A I N   G A T H E R E R')
        print(R+'   ---<>----<>----<>----<>----<>----<>--\n')
        time.sleep(0.7)
        print(B+' [*] Initializing Step [1]...')
        subdombrute(web)
        print(G+'\n [+] Module [1] Bruteforce Completed!\n')
        print(B+' [*] Initializing Step [2]...')
        outer(web)
        print(G+' [+] Module [2] API Retriever Completed!\n')
        acc = report(web, found, final)
        print(O+' [*] Writing found subdomains to a file...')
        if acc:
            miv = open(fileo,'a')
            for pwn in acc:
                vul = str(pwn) + '\n'
                
                miv.write(vul)
            miv.close()
        print(G+' [+] Done!')

    except Exception as e:
        print(R+' [-] Exception encountered!')
        print(R+' [-] Error : '+str(e))
