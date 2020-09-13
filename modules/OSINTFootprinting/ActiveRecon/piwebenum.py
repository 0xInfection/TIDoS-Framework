#!/usr/bin/env python3
# coding:  utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import os, time
from core.methods.tor import session
from time import sleep
from core.Core.colors import *
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "Ping/NPing Enumeration."
searchinfo = "(N)Ping Enumeration"
properties = {}

def piwebenum(web):
    name = targetname(web)
    lvl2 = "piwebenum"
    module = "ReconANDOSINT"
    lvl1 = "Active Reconnaissance"
    lvl3 = ""
    requests = session()
    time.sleep(0.4)
    web = web.split('//')[1]
    #print(R+'\n   =============================================')
    #print(R+'    P I N G / N P I N G   E N U M E R A T I O N')
    #print(R+'   =============================================\n')
    from core.methods.print import posintact
    posintact("(n)ping enumeration") 
    print(GR + ' [!] Pinging website...')
    time.sleep(0.5)
    print(C+' [*] Using adaptative ping and debug mode with count 5...')
    time.sleep(0.4)
    print(GR+' [!] Press Ctrl+C to stop\n'+color.END)
    os.system('ping -D -c 5 '+ web)
    print('')
    time.sleep(0.6)
    print(C+' [*] Trying NPing (NMap Ping)...')
    print(C+" [~] Result: \n")
    print('')
    text = requests.get('http://api.hackertarget.com/nping/?q=' + web).text
    nping = str(text)
    print(color.END+ nping +C+'\n')
    save_data(database, module, lvl1, lvl2, lvl3, name, nping)

def attack(web):
    web = web.fullurl
    piwebenum(web)