#!/usr/bin/env python2
# -*- coding : utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This script is a part of TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import os
import time

def scanenumban1():

    os.system('clear')
    time.sleep(0.5)
    print """

\033[1;31m
	===========================================
	 S C A N N I N G  &  E N U M E R A T I O N
	===========================================\033[1;33m

 Choose from the following options:

\033[1;34m [1] \033[1;36mRemote Server WAF Fingerprinting
\033[1;34m [2] \033[1;36mPort Scanning and Enumeration (includes several types of scans)
\033[1;34m [3] \033[1;36mInteractive Scanning with NMap (preloaded modules)
\033[1;34m [4] \033[1;36mFingerprint Web Technologies (front-end) 
\033[1;34m [5] \033[1;36mLet loose Crawlers on the target
 
\033[1;34m [A] \033[1;36mAutomate all one by one on target

\033[1;34m [99] \033[1;36mBack

"""
