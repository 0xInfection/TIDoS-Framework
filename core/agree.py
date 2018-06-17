#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import os
import sys
import platform
import time
from agreement import *
from colors import *

def agree():

	os.system('clear')
	if str(platform.system()) != "Linux":
	    sys.exit(""+R+"[!] " + color.UNDERLINE + "\033[91m" + "You are not using a Linux Based OS! Linux is a must-have for this script!" + color.END)
	if not os.geteuid() == 0:
	    sys.exit(""+R+"[!] " + color.UNDERLINE + "\033[91m" + "Must be run as root. :) " + color.END)
	if 'no' in open('agree.txt').read():
	    agreement()

	    agree = raw_input(''+G+color.BOLD+ 'Do you agree to these terms and conditions? :> ' + color.END)
	    if agree == "yes":
		print ('[!] '+G+ color.BOLD+'Awesome !!! Now drift ahead...' + color.END)
		time.sleep(3)
		FILE = open("agree.txt","w")
		FILE.write('yes')
		FILE.close()
	    elif agree == "y":
		print ('[!] '+G+ color.BOLD+'Awesome !!! Now drift ahead...' + color.END)
		time.sleep(3)
		FILE = open("agree.txt","w")
		FILE.write('yes')
		FILE.close()
	    elif agree == "Y":
		print ('[!] '+G+ color.BOLD+'Awesome !!! Now Drift Ahead...' + color.END)
		time.sleep(3)
		FILE = open("agree.txt","w")
		FILE.write('yes')
		FILE.close()
	    else:
		print (''+R+color.BOLD+'[!] You have to agree!' + color.END)
		time.sleep(1)
		sys.exit()
