#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework

from __future__ import print_function
try:
    from google import search
except:
    from googlesearch import search
import time
import urllib2
from random import randint
from time import sleep
from colors import *

def getposts(web):

    site = str(web)
    def clear_cookie():
        fo = open(".google-cookie", "w")
        fo.close()


    def google_it (dork):
        clear_cookie()
        for title in search(dork, stop=30):
            print(B+' [!] Profile Found :> '+C+title)
            time.sleep(0.5)

    try:
        print(GR+" [*] Finding LinkedIn Employees ...\n")
        google_it("site:linkedin.com employees "+site+"")
        print(O+' [!] Pausing to avoid captcha...')
        time.sleep(10)

        print(GR+' [*] Finding Linkedin company profiles...\n')
        google_it("site:linkedin.com comapany "+site+"")

    except urllib2.HTTPError as err:
        if err.code == 503:
            print(R+' [-] Captcha appeared...\n')
            pass

def linkedin(web):

    print(GR+' [*] Loading module...')
    time.sleep(0.6)
    print(R+'\n    =====================================')
    print(R+'     L I N K E D I N   G A T H E R I N G')
    print(R+'    =====================================\n')
    getposts(web)
