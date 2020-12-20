#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework


import time
import sys, platform
import os
import urllib.request
try:
    from google import search
except Exception:
    from googlesearch import search
from time import sleep
from core.Core.colors import *

info = "Simple Google Search."
searchinfo = "Google Search"
properties = {}

def googleSearch():

    try:
        time.sleep(0.4)
        #print(R+'\n   ===========================')
        print(R+'\n    G O O G L E   S E A R C H')
        print(R+'   ---<>----<>----<>----<>----\n')
                    
        lol = input(O+ " [§] QUERY :> " + color.END)
        time.sleep(0.8)
        m = input(C+' [§] Search limit (not recommended above 30) :> ')
        print(C+ " [!] Below are the list of websites with info on '" +lol+ "'")
        x = search(lol, tld='com', lang='es', stop=int(m))
        for url in x:
            print(O+"   [!] Site Found :>"+C+color.TR3+C+G + url+C+color.TR2+C)
            q = open('.google-cookie','w')
            q.close()
    except urllib.error.HTTPError:
        print(R+' [-] You have used google many times.')
        print(R+' [-] Service temporarily unavailable.')

def attack(web):
    web = web.fullurl
    googleSearch()
