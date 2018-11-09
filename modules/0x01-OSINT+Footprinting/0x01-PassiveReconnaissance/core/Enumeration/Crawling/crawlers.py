#!/usr/bin/env python
# -*- coding : utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This script is a part of TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import sys
import platform
import os
import time
import random
import subprocess
from random import *
sys.path.append('modules/0x02-Scanning+Enumeration/0x02-WebCrawling/')

# Import stuff
from crawler1 import *
from crawler2 import *
from crawler3 import *
from core.Core.colors import *
from core.Enumeration.Crawling.crawlersban import *

def crawlers(web):

    time.sleep(0.3)
    print(' [!] Module Selected : Crawlers')
    time.sleep(0.4)
    crawlersban() # banner
    v = raw_input(O+' [#] TID :> ')

    if v.strip() == '1': # level 1 crawler
        print(B+' [!] Module Selected :'+C+' Crawler (Depth 1)')
        crawler1(web)
        time.sleep(1)
        crawlers(web)

    elif v.strip() == '2': # level 2 crawler
        print(B+' [!] Module Selected :'+C+' Crawler (Depth 2)')
        crawler2(web)
        time.sleep(1)
        crawlers(web)

    elif v.strip() == '3': # level 3 crawler
        print(B+' [!] Module Selected :'+C+' Crawler (Depth 3)')
        crawler3(web)
        time.sleep(1)
        crawlers(web)

    elif v.strip() == '99': # to go back
        print(GR+' [*] Going back...')
        time.sleep(0.5)
        os.system('clear')

    elif v.strip() == 'A':
        print(W+'\n [!] Module Automater Initialized...')
        sleep(0.5)
        print(B+' [*] Initializing Scan Type :'+C+' Crawler (Depth 1)')
        crawler1(web) # unleash level 1

        print(B+'\n [!] Scan Type Completed :'+C+' Crawler 1\n')
        sleep(0.5)
        print(B+' [!] Initializing Scan Type :'+C+' Crawler (Depth 2)')
        crawler2(web) # unleash level 2

        print(B+'\n [!] Scan Type Completed :'+C+' Crawler 2\n')
        sleep(0.5)
        print(B+' [!] Initializing Scan Type :'+C+' Crawler (Depth 3)')
        crawler3(web) # unleash level 3

        print(B+'\n [!] Scan Type Completed :'+C+' Crawler 3\n\n'+G+' [+] All modules successfully completed!')
        raw_input(GR+' [+] Press '+O+'Enter '+GR+'to continue...') # for the user to take a breadth :/
        crawlers(web) # get back to menu

    else:
        dope = ['You high dude?','Shit! Enter a valid option','Whoops! Thats not an option','Sorry! You just typed shit']
        print(' [-] '+dope[randint(0,3)]) # troll stuffs :p
        sleep(1)
        crawlers(web)
