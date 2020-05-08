#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_____, ___
   '+ .;    
    , ;   
     .   
           
       .    
     .;.    
     .;  
      :  
      ,   
       

┌─[TIDoS]─[]
└──╼ VainlyStrain
"""


import sys
import requests
import subprocess
from urllib.request import urlopen
import core.variables as vars
from core.Core.colors import R, color


def presession():
    presess = requests.session()
    if vars.tor:
        presess.proxies['http'] = 'socks5h://localhost:9050'
        presess.proxies['https'] = 'socks5h://localhost:9050'
        presess.headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'
    return presess

def session():
    VaileSession = requests.session()
    VaileSession.proxies = {}

    VaileSession.headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'

    if vars.tor:
        VaileSession.proxies['http'] = 'socks5h://localhost:9050'
        VaileSession.proxies['https'] = 'socks5h://localhost:9050'
        torcheck()
    else:
        VaileSession.proxies['http'] = None
        VaileSession.proxies['https'] = None
        
    return VaileSession

def torpipe(controller):
    try:
        status = subprocess.check_output(['systemctl','status','tor'])
        #status = subprocess.check_output(['service','tor','status'])
        if "active (running)" in str(status):
            vars.tor = controller
            return True
        else:
            print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Tor service not running. Aborting..."+color.END)
            return False
    except subprocess.CalledProcessError:
        print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Tor service not installed or running. Aborting..."+color.END)
        return False

def initcheck():
    ipaddr = urlopen('http://ip.42.pl/raw').read()
    vars.initip = str(ipaddr).split("'")[1]

def torcheck():
    #try:
    s = presession()
    ipaddr = s.get('http://ip.42.pl/raw').text
    #ip = str(ipaddr).split("'")[1].strip()
    if vars.initip.strip() is not ipaddr:
        print(" [+] Successfully connected to Tor. IP {} > {}".format(vars.initip, ipaddr))
    else:
        print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Not connected to Tor: Attacker IP used: {}. Aborting.{}".format(ipaddr, color.END))
        sys.exit()
    #except:
    #    print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "IPcheck socket failure.")
    #    torcheck()