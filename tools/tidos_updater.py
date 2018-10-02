#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Updater of TIDoS Framework
#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

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
    text = requests.get('https://raw.githubusercontent.com/theInfectedDrake/TIDoS-Framework/master/doc/Version_Num').text
    result = str(text)
    m = open('../doc/Version_Num','r').read()
    print(C+' [!] The version on GitHub is : '+B+result.replace('\n',''))
    print(B+' [!] The version you have is : '+C+m)
    if m != result :
	print(O+' [!] An update is available to version '+result)
	mn = raw_input(O+' [#] Update? '+R+'(Y/n) :> '+O)
	if mn == 'Y' or mn == 'y':
		print(GR+' [*] Updating...\n')
		p = open('../doc/Version_Num','w')
		p.write(result.replace('\n',''))
		p.close()
		os.system('cd .. && git add . && git commit -m "Did stuff" && git pull && git update-index --assume-unchanged tools/tidos_updater.py && git commit -m "Merged"')
	elif mn == 'n' or mn == 'N':
		print(R+' [-] Okay... Not updated!\n')
	else:
		print(R+'\n [-] U mad dude?\n')
		time.sleep(0.7)
    else:
	print(G+' [!] You are using the latest version of this framework!')

updater()
