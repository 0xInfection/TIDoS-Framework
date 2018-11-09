#!/usr/bin/env python

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import os
import time
import random
from random import *
from core.Vulnlysis.vulnban import *
from core.Vulnlysis.Misc_Bugs.webbugs import *
from core.Vulnlysis.Oth_Bugs.othbugs import *
from core.Vulnlysis.Serio_Bugs.serbugs import *
from core.Core.colors import *

def vuln(web):

    print(B+' [+] Module Loaded : '+C+'Vulnerability Analysis')
    vulnban()
    v = raw_input(''+O+' \033[4mTID\033[1;0m '+GR+':> ' + color.END)
    print('\n')

    if v.strip() == '1':
        webbugs(web)

    elif v.strip() == '2':
        serbugs(web)

    elif v.strip() == '3':
        othbugs(web)

    elif v.strip() == '99':
        print('[!] Back')
        time.sleep(0.7)
        os.system('clear')

    else:
        dope = ['You high dude?','Hey there! Enter a valid option','Whoops! Thats not an option','Sorry fam! You just typed shit']
        print(dope[randint(0,3)])
        time.sleep(0.7)
        os.system('clear')
        vulnban()
        vuln(web)
