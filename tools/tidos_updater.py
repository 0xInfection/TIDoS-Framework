#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import time
import os
import requests
from colors import *

def updater():

    print R+'   ==============='
    print R+'    U P D A T E R'
    print R+'   ===============\n'
    time.sleep(0.4)
    print(GR+' [*] Looking up for the latest version...')
    time.sleep(0.4)
    text = requests.get('https://raw.githubusercontent.com/theInfectedDrake/TIDoS-Framework/master/doc/Version_Num').text
    result = str(text)
    m = open('doc/Version_Num','r').read()
    print C+' [!] The version on GitHub is : '+B+result
    print B+' [!] The version you have is : '+C+m
    if Version == result :
	print O+' [!] An update is available to version '+result
	mn = raw_input(O+' [#] Update? (Y/n) :> ')
	if mn == 'Y':
		print GR+' [*] Updating...'
		os.system('git pull')
	else:
		print R+' [-] Okay... Not updated!'

    else:
	print G+' [!] You are using the latest version of this framework!'

updater()
