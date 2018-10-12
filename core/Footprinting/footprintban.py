#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework

from __future__ import print_function
import os, time
from colors import *
from core.Core.arts import footprintban_art

def footprintban():

    time.sleep(0.5)
    os.system('clear')
    print(G+' [!] Module Loaded : Reconnaissance\n')
    print(footprintban_art)
    print("""
Choose from the following options:

\033[1;34m [1] \033[1;36mPassive Footprinting \033[1;0m(Open Source Intelligence)
\033[1;34m [2] \033[1;36mActive Reconnaissance \033[1;0m(Gather via Interaction)
\033[1;34m [3] \033[1;36mInformation Disclosure \033[1;0m(Errors, Emails, etc)

\033[1;34m [99] \033[1;36mBack
""")
