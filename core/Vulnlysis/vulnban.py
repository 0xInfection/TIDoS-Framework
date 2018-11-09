#!/usr/bin/env python
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import os, time
from core.Core.colors import *
from core.Core.arts import vulnban_art

def vulnban():

    time.sleep(0.3)
    os.system('clear')
    print(O+' [!] Module Selected : Vulnerability Analysis')
    print(vulnban_art)
    print(B+'   [1] '+C+' Basic Bugs & Misconfigurations'+W+' (Low Priority [P0x3-P0x4])')
    time.sleep(0.2)
    print(B+'   [2] '+C+' Critical Vulnerabilities '+W+'(High Priority [P0x1-P0x2])')
    time.sleep(0.2)
    print(B+'   [3] '+C+' Others '+W+'(Bruters)\n')
    time.sleep(0.2)
    print(B+'   [99] '+C+'Back\n')
    time.sleep(0.2)
