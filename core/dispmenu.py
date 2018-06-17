#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework 

import time
from colors import *

def dispmenu():
	
	print ''+O+'\n Choose from the options below :\n'
	time.sleep(0.2)
	print ''+B+' [1] \033[1;36mReconnaissance'
	time.sleep(0.1)
	print ''+B+' [2] \033[1;36mScanning & Enumeration'
	time.sleep(0.1)
	print ''+B+' [3] \033[1;36mVulnerability Analysis'
	time.sleep(0.1)
	print ''+B+' [4] \033[1;36mExploitation (beta)\n'
	time.sleep(0.1)
	print ''+B+'\n [99] \033[1;36mSay "alvida"! (Exit TIDoS)\n'
	time.sleep(0.1)
