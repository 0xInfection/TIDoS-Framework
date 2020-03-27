#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/VainlyStrain/TIDoS


import urllib.request
import time
import sys
from time import sleep
from core.Core.colors import *

info = "HTTP Header Grabber."
searchinfo = "HTTP Header Grabber"
properties = {}

def grabhead(web):
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
        header = str(urllib.request.urlopen(web).info()).splitlines()
        print('')
        for m in header:
            n = m.split(':')
            print('  '+C+n[0]+': '+C+n[1])
        print('')
    except urllib.error.HTTPError as e:
        print(R+' [-] '+e.__str__())

def attack(web):
    web = web.fullurl
    grabhead(web)