#!/usr/bin/env python

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import os
import time
from core.Core.colors import *

def loadstyle():

    os.system('clear')
    red_bold = R
    reset = W
    loading = "Loading the TIDoS Framework..."
    action = 0
    while action < 1:
        for i,char in enumerate(loading):
            if i == 0:
                print("%s%s%s%s" %(red_bold,char.upper(),reset,loading[1:]))
            elif i == 1:
                old_loading = loading[0].lower()
                print("%s%s%s%s%s" %(old_loading,red_bold,char.upper(),reset,loading[2:]))
            elif i == i:
                old_loading = loading[-0:i].lower()
                print("%s%s%s%s%s" %(old_loading,red_bold,char.upper(),reset,loading[i+1:]))
            os.system('clear')
        action += 1
