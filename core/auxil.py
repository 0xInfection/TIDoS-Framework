#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import sys
import os
import time
import subprocess
import random
from random import randint
from subprocess import call
sys.path.append('modules/AuxilMods/')
from auxilban import *
from encodeall import *
from brutemods import *

def auxil(web):

    print ''
    time.sleep(0.3)
    print W+'\n [*] Type Selected : Auxillaries...\n'
    auxilban()
    v = raw_input(GR+'  [#] \033[1;4mTID\033[0m'+GR+' :> ' + color.END)
    print ''
    if v == '1':
	print ' [!] Type Selected : Bruteforce Modules'
	brutemods(web)
	print '\n\n'
	auxil(web)

    elif v == '2':
	print ' [!] Type Selected : Encode Strings'
	encodeall()
	print '\n\n'
	auxil(web)

    elif v == '99':
	print GR+' [*] Going back!'
	time.sleep(0.7)
	os.system('clear')

    else:
	dope = ['You high dude?','Shit! Enter a valid option','Whoops! Thats not an option','Sorry! You just typed shit']
	print dope[randint(0,3)]
	time.sleep(0.7)
	os.system('clear')
	auxil(web)
