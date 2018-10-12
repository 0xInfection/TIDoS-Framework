#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework

from __future__ import print_function
import os
import time

# Get module imports
from core.Core.colors import *
from footprintban import *
from Info_Disc.infodisc import *
from Active_Recon.activeo import *
from Passive_Recon.passiveo import *

def footprint(web):

    print(B+' [+] Module Selected : '+C+'Footprinting')
    footprintban() # banner
    m = raw_input(O+' [#] \033[1;4mTID\033[0m'+GR+' :> ' + color.END)
    print('')

    if m.strip() == '1':
        passiveo(web) # passive recon module
        print('\n')
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        footprint(web)

    elif m.strip() == '2':
        activeo(web) # active recon module
        print('\n')
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        footprint(web)

    elif m.strip() == '3':
        infodisc(web) # information disclosure modules
        print('\n')
        raw_input(O+' [#] Press '+GR+'Enter'+O+' to continue...')
        footprint(web)

    elif m.strip() == '99': # get back to main module
        print(' [+] Back!')

    else:

        print('')
        dope = [' [*] You high dude?',' [*] Hey there! Enter a valid option',' [*] Whoops! Thats not an option',' [*] Sorry fam! You just typed shit'] # troll stuff :p
        print(dope[randint(0,3)])
        time.sleep(0.5)
        footprint(web)
