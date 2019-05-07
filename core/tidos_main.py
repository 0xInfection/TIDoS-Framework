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
import subprocess
from random import randint
from os import path
from time import sleep
from logging import getLogger, ERROR
from multiprocessing import Process, Queue, current_process, Manager
import multiprocessing
getLogger("scapy.runtime").setLevel(ERROR)
warnings.filterwarnings("ignore")

# All module imports
from core.Core.inputin import *
from core.Core.banner import *
from core.Core.agree import *
from core.Core.loadstyle import *
from core.Core.bannerbelow import *
from core.Core.colors import *
from core.Core.build_menu import buildmenu
from core.Core.arts import *

# Global Variables
NUM_WORKERS = multiprocessing.cpu_count()   # You can hard code this if you do not have multiple processors
process_queue = multiprocessing.Queue()     # all processes are thrown here
done_queue = multiprocessing.Queue()        # all completed processes are placed here
manager = multiprocessing.Manager()         # this is a dictionary manager, useful for storing links and webscrapes
master_dict = manager.dict()                # the master dictionary. this needs passed from global scope for sharing across multi-processes
procs = []                                  # list for processes

menu = { # '#' : ['module', 'description', 'function']
        '1':['Reconnaissance & OSINT','(50 Modules)','footprint'],\
        '2':['Scanning & Enumeration','(16 Modules)','scanenum'],\
        '3':['Vulnerability Analysis','(37 Modules)','vuln'],\
        '4':['Exploitation (beta)','(1 Module)','exploits'],\
        '5':['Auxillary Modules','(4 Modules)','auxil']\
    }

def multProc(target_func, arg0):
    try:
        p = multiprocessing.Process(target=target_func, args=(arg0))
        procs.append(p)
        p.start()
    except Exception as e: # Global Error Handling Stuff
        print(RED+' [-] Unhandled runtime exception while execution...')
        print(RED+' [-] Exception Encountered: '+e.__str__())
        print(RED+' [-] Returning back to main menu...')
    return

def exit(exit):
    print(CYAN+' [+] Alvida, see ya!\n')
    sys.exit(0)
    return


def tidos_main(): # To be called by external

    try:
        agree()         # the agreement (to appear only at time of installation)
        loadstyle()     # some swag stuff :p
        banner()        # main banner
        bannerbelow()   # banner 2
        target = inputin() # take the website as input

    except Exception as e:
        print(RED+' [-] Exception encountered!')
        print(RED+' [-] Exception : '+str(e))
        sys.exit(1)

    print(PURPLE+' [+] Okay, so what to start with?') # lets start
    time.sleep(1)

    def tidosmain(target): # this is to be iterated repeatedly
        while True:
            try:
                buildmenu(target,menu,'Main Menu',main_menu_art)          # build main menu

            except KeyboardInterrupt: # Incase user wants to quit
                print(RED+"\n [-] " + color.UNDERLINE+ "User Interruption detected!"+color.END)
                time.sleep(0.4)
                print(CYAN+' [+] Alvida, see ya!\n')
                sys.exit(0)

            # except Exception as e: # Global Error Handling Stuff
            #     print(e)
            #     print(RED+' [-] Unhandled runtime exception while execution...')
            #     print(RED+' [-] Exception Encountered: '+e.__str__())
            #     print(RED+' [-] Returning back to main menu...')
            #     time.sleep(1)
            #     pass # (If user runs into a error, that would not quit this tool)

    tidosmain(target) # The true start of this program
