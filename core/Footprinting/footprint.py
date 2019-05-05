#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import os

# Get module imports
from core.Core.colors import *
from core.Core.arts import footprintban_art

def footprint(web):
    from core.Core.build_menu import buildmenu
    menu = { # module, [description, function]
        '1':['Passive Footprinting','(Open Source Intelligence)','passiveo'],\
        '2':['Active Reconnaissance ','(Gather via Interaction)','activeo'],\
        '3':['Information Disclosure','(Errors, Emails, etc)','infodisc'],\
    }
    
    print(BLUE+' [+] Module Selected : '+CYAN+'Footprinting')
    #os.system('clear')
    print(footprintban_art)            # display menu art
    buildmenu('footprint',menu)        # build menu