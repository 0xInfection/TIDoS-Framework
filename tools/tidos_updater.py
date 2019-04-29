#!/usr/bin/env python
#-*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Updater of TIDoS Framework
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import time
import os
import sys
import requests
sys.path.append('../doc/')
from colors import *

def updater():

    print(R+'\n   ===============')
    print(R+'    U P D A T E R')
    print(R+'   ===============\n')
    time.sleep(0.4)
    print(GR+' [*] Looking up for the latest version...')
    time.sleep(0.4)
    text = requests.get('https://raw.githubusercontent.com/0xInfection/TIDoS-Framework/master/doc/Version_Num').text
    result = str(text)
    m = open('../doc/Version_Num','r').read()
    print(C+' [!] The version on GitHub is : '+B+result.replace('\n',''))
    print(B+' [!] The version you have is : '+C+m)
    if m != result :
        print(O+' [!] An update is available to version '+result)
        mn = raw_input(O+' [#] Update? '+R+'(Y/n) :> '+O)
        current_path = os.getcwd().split('/')
        folder = current_path[-1] # current directory name
        path = '/'.join(current_path) # current directory path
        if mn == 'Y' or mn == 'y':
            print(GR+' [*] Updating...\n')
            os.system('git clone --quiet https://github.com/0xInfection/TIDoS-Framework %s' % (folder))
            os.system('cp -r %s/%s/* %s && rm -r %s/%s/ 2>/dev/null' % (path, folder, path, path, folder))
        elif mn == 'n' or mn == 'N':
            print(R+' [-] Okay... Not updated!\n')
        else:
            print(R+'\n [-] U mad dude?\n')
            time.sleep(0.7)
    else:
        print(G+' [!] You are using the latest version of this framework!')
    quit()

updater()
