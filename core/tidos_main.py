#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import sys
import platform
import os
import time
import warnings
from random import randint
from os import path
from time import sleep
from logging import getLogger, ERROR
getLogger("scapy.runtime").setLevel(ERROR)
warnings.filterwarnings("ignore")

# All module imports
from core.Core.inputin import *
from core.Core.banner import *
from core.Core.dispmenu import *
from core.Core.agree import *
from core.Core.loadstyle import *
from core.Core.bannerbelow import *
from core.Auxillaries.auxil import *
from core.Core.colors import *
from core.Exploitation.exploits import *
from core.Footprinting.footprint import *
from core.Enumeration.scanenum import *
from core.Vulnlysis.vuln import *

def tidos_main(): # To be called by external

    try:
        agree() # the agreement (to appear only at time of installation)
        loadstyle() # some swag stuff :p
        banner() # main banner
        bannerbelow() # banner 2
        web = inputin() # take the website as input
    except Exception as e:
        print(R+' [-] Exception encountered!')
        print(R+' [-] Exception : '+str(e))
        sys.exit(1)

    print(P+' [+] Okay, so what to start with?') # lets start
    time.sleep(1)
    def tidosmain(web): # this is to be iterated repeatedly

        while True:
            try:
                os.system('clear')
                dispmenu() # displaying the options
                zop = raw_input(''+GR+' [#] \033[1;4mTID\033[0m'+GR+' :> ' + color.END)
                zap = zop.strip()

                if zap == '1': # 1 - OSINT + Recon

                    print(G+"\n [+] Module loaded : Reconnaissance")
                    footprint(web)

                elif zap == '2': # 2 - Scanning + Enumeration

                    print(G+'\n [+] Module loaded : Scanning & Enumeration')
                    scanenum(web)

                elif zap == '3': # 3 - Vulnerability Analysis

                    print(G+'\n [+] Module loaded : Vulnerability Analysis')
                    vuln(web)

                elif zap == '4': # Exploitation

                    print(G+'\n [+] Module loaded : Exploits Castle')
                    exploits(web)

                elif zap == '5': # Auxillary modules

                    print(G+'\n [+] Module loaded : Auxillaries')
                    auxil(web)

                elif zap == '99': # Say Goodbye!

                    print(R+'\n [-] Exiting...')
                    time.sleep(0.6)
                    print(O+' [+] Goodluck mate, Alvida!\n')
                    sys.exit(0)

                else: # Troll for not selecting right option :p

                    dope = ['You high dude?', 'Sorry fam! You just typed shit']
                    print(R+' [-] ' + dope[randint(0,1)])
                    time.sleep(0.5)
                    pass

            except KeyboardInterrupt: # Incase user wants to quit

                print(R+"\n [-] " + color.UNDERLINE+ "User Interruption detected!"+color.END)
                time.sleep(0.4)
                print(C+' [+] Alvida, see ya!\n')
                sys.exit(0)

            except Exception as e: # Global Error Handling Stuff
                print(R+' [-] Unhandled runtime exception while execution...')
                print(R+' [-] Exception Encountered: '+e.__str__())
                print(R+' [-] Returning back to main menu...')
                time.sleep(1)
                pass # (If user runs into a error, that would not quit this tool)

    tidosmain(web) # The true start of this program
