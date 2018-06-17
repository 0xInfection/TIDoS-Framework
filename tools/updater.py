#!/usr/bin/env python2
#-*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import urllib, urllib2, requests, time
from time import sleep
from colors import *

def updater():

    print R+'    U P D A T E R'
    print R+'   ===============\n'
    Version = 'v2.1.0'
    time.sleep(0.4)
    print(GR+' [*] Looking up for the latest version...')
    time.sleep(0.4)
    text = requests.get('https://raw.githubusercontent.com/the-Infected-Drake/TIDoS-Framework/master/doc/Version_Num').text
    result = str(text)
    print C+' [!] The version on GitHub is : '+result
    print B+' [!] The version you have is : '+Version
    if Version == result :
	print O+' [!] An update is available to version '+result
	print GR+' [!] Please download the latest version and run the install file...'
    else:
	print G+' [!] You are using the latest version of this framework!'

