#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

from __future__ import print_function
import time
import os
from colors import *
from core.Core.arts import auxilban_art

def auxilban():

    os.system('clear')
    print(" [!] Module Selected : Auxillary Modules\n")
    time.sleep(0.4)
    print(auxilban_art)
    time.sleep(0.3)
    print('')
    print(B+'     [1]'+C+' Generate Hashes from Strings'+W+'(4 Types) ')
    time.sleep(0.1)
    print(B+'     [2]'+C+' Encode Payload or Strings'+W+' (7 Types)')
    time.sleep(0.1)
    print(B+'     [3]'+C+' Extract Metadata from Images'+W+' (EXIF Data)')
    time.sleep(0.1)
    print(B+'     [4]'+C+' HoneyPot Probability'+W+' (ShodanLabs HoneyScore)\n')
    time.sleep(0.1)
    print(B+'     [99]'+C+' Back\n') 

