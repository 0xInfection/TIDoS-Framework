#!/usr/bin/env python
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import os
import sys
import platform
import time
from core.Core.agreement import *
from core.Core.colors import *

def agree():

    os.system('clear')
    if str(platform.system()) != "Linux":
        sys.exit(R+" [!] " + color.UNDERLINE + "\033[91m" + "You are not using a Linux Based OS! Linux is a must-have for this script!" + color.END)
    if not os.geteuid() == 0:
        sys.exit(" [!] " + color.UNDERLINE + "\033[91m" + "Must be run as root. :) " + color.END)
    if 'no' in open('agree').read():
        agreement()

        a1 = raw_input(O+' [0x00] '+G+'Do you agree to these terms and conditions? :> '+C)
        if a1.lower().startswith('y'):
            print(G+' [0x01] '+O+'Thats awesome! Move on...')
            time.sleep(3)
            FILE = open("agree","w")
            FILE.write('yes')
            FILE.close()

        else:
            print(O+' [0x0F] '+R+'You have to agree!')
            time.sleep(1)
            sys.exit(0)
