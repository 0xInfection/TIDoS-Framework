#!/usr/bin/env python
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework

from __future__ import print_function
import sys
import os
import time
import subprocess
import random
from random import randint
from subprocess import call
sys.path.append('modules/0x05-Auxillaries+PF6/')
from encodeall import *
from honeypot import *
from hashes import *
from imgext import *
from core.Auxillaries.auxilban import *

def auxil(web):

    auxilban()
    print('')
    time.sleep(0.3)
    v = raw_input(GR+'  [#] \033[1;4mTID\033[0m'+GR+' :> ' + color.END)
    print('')
    if v == '1':
        print(' [!] Type Selected : Generate Hashes')
        hashes()
        print('\n\n')
        raw_input(O+' [+] Press '+GR+'Enter'+O+' to Continue...')
        auxilban()
        auxil(web)

    elif v == '2':
        print(' [!] Type Selected : Encode Strings')
        encodeall()
        print('\n\n')
        raw_input(O+' [+] Press '+GR+'Enter'+O+' to Continue...')
        auxilban()
        auxil(web)

    elif v == '3':
        print(' [!] Type Selected : Extract Metadata')
        imgext()
        print('\n\n')
        raw_input(O+' [+] Press '+GR+'Enter'+O+' to Continue...')
        auxilban()
        auxil(web)

    elif v == '4':
        print(' [!] Type Selected : Honeypot Detector')
        honeypot()
        print('\n\n')
        raw_input(O+' [+] Press '+GR+'Enter'+O+' to Continue...')
        auxilban()
        auxil(web)

    elif v == '99':
        print(GR+' [*] Going back!')
        time.sleep(0.7)
        os.system('clear')

    else:
        dope = ['You high dude?','Shit! Enter a valid option','Whoops! Thats not an option','Sorry! You just typed shit']
        print(dope[randint(0,3)])
        time.sleep(0.7)
        os.system('clear')
        auxilban()
        auxil(web)
