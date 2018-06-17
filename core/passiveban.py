#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 


import time
from colors import *

def passiveban():

    time.sleep(0.4)
    print G+'     +-----------------+'
    print G+'     |  '+O+'PASSIVE RECON  '+G+'|'
    print G+'     +-----------------+'
    time.sleep(0.6)
    print ''
    print B+'      [1] '+C+'Ping Check (Using external APi)'+W
    time.sleep(0.1)
    print B+'      [2] '+C+'WhoIS Lookup (Get domain info)'+W
    time.sleep(0.1)
    print B+'      [3] '+C+'GeoIP Lookup (Pinpoint Server Location)'+W
    time.sleep(0.1)
    print B+'      [4]'+C+' DNS Configuration Lookup'+W
    time.sleep(0.1)
    print B+'      [5]'+C+' Gather Subdomains (Only indexed visible ones)'+W
    time.sleep(0.1)
    print B+'      [6]'+C+' Reverse DNS Configuration Lookup '+W
    time.sleep(0.1)
    print B+'      [7]'+C+' Reverse IP Lookup (Find hosts on same server)'+W
    time.sleep(0.1)
    print B+'      [8]'+C+' Gather All Links from WebPage'+W
    time.sleep(0.1)
    print B+'      [9]'+C+' Google Search (Search your own Query or Dork)'+W
    time.sleep(0.1)
    print B+'      [10] '+C+'Google Dorking (Multiple Modules)'+W+'\n'
    time.sleep(0.1)
    print B+'      [A] '+C+'Test all modules against the target 1 by 1\n'
    time.sleep(0.1)
    print B+'      [99] '+C+'Back'+W+'\n'
    time.sleep(0.3)

