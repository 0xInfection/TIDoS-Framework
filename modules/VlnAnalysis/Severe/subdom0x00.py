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
import socket
#import requests
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
            print(GR+' [*] Importing wordlist path to be bruteforced... '+O+'"files/fuzz-db/subdomain_paths.lst"')
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
        print(R+' [-] Fatal Exception!')
        print(R+' [-] No wordlist found under '+O+'files/fuzz-db/.')
    return found

def outer(web):
    requests = session()
    global final
    final = []
    wew = []
    time.sleep(0.4)
    print(R+'\n    A P I   R E T R I E V E R  ')
    print(R+'   ---<>----<>----<>----<>----')

    print(GR+' [!] Retriving subdomains...')
    time.sleep(0.4)
    print(GR+" [~] Result: ")
    text = requests.get('http://api.hackertarget.com/hostsearch/?q=' + web).text
    result = str(text)
    if 'error' not in result:
        mopo = result.splitlines()
        for mo in mopo:
            print(G+' [+] Received : '+O+mo.split(',')[0].strip()+P+' ['+mo.split(',')[1].strip()+']')
            final.append(str(mo.split(',')[0].strip()))

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

    if web.startswith('http'):
        web = web.replace('http://','')
        web = web.replace('https://','')
    try:
        webb = web
        if "@" in web:
            webb = web.split("@")[1]
        fileo = 'tmp/logs/'+webb+'-logs/'+webb+'-subdomains.lst'
        p = open(fileo,'w+')
        p.close
        print(R+'\n    S U B D O M A I N   G A T H E R E R')
        print(R+'   ---<>----<>----<>----<>----<>----<>--\n')
        time.sleep(0.7)
        print(B+' [*] Initializing Step [1] Bruteforce...')
        subdombrute(web)
        print(G+'\n [+] Module [1] Bruteforce Completed!\n')
        print(B+' [*] Initializing Step [2] API Retriever...')
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

def attack(web):
    web = web.fullurl
    subdom0x00(web)
