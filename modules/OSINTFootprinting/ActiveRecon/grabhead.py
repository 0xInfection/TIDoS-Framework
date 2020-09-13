#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import urllib.request
import time
import sys
from time import sleep
from core.Core.colors import *
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "HTTP Header Grabber."
searchinfo = "HTTP Header Grabber"
properties = {}

def grabhead(web):
    name = targetname(web)
    lvl2 = "grabhead"
    module = "ReconANDOSINT"
    lvl1 = "Active Reconnaissance"
    lvl3 = ""
    time.sleep(0.4)
    #print(R+'\n      ==================================')
    #print(R+'      G R A B   H T T P   H E A D E R S')
    #print(R+'     ===================================\n')
    from core.methods.print import posintact
    posintact("grab http headers") 
    print(GR + color.BOLD + ' [*] Grabbing HTTP Headers...')
    time.sleep(0.4)
    web = web.rstrip()
    try:
        headerwhole = str(urllib.request.urlopen(web).info())
        header = headerwhole.splitlines()
        print('')
        for m in header:
            n = m.split(':')
            print('  '+C+n[0]+': '+C+n[1])
        print('')
        save_data(database, module, lvl1, lvl2, lvl3, name, headerwhole)
    except urllib.error.HTTPError as e:
        print(R+' [-] '+e.__str__())

def attack(web):
    web = web.fullurl
    grabhead(web)