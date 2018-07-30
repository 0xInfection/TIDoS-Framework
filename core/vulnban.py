#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import os, time
from colors import *

def vulnban():

    time.sleep(0.3)
    os.system('clear')
    print O+' [!] Module Selected : Vulnerability Analysis'
    print R+"""
                     .....
	       .:noONNNNNNNOon:.
	    .:NNNNNNNmddddNNNNNNN:.
          :NNNNmy+:.   +   .:+ymNNNN:
         NNNNy:`       +       `:yNNNN
       NNNNy.                     -!NNNN
      NNNN/            +            \NNNN
     NNNm-         .:#####:.         -mNNN      \033[1;37m[0x00] \033[1;33mV U L N E R A B I L I T Y \033[1;31m
    :NNN+         #    +    #         +NNN:	
    NNNm         #     +     #         mNNN 	              \033[1;33mE N U M E R A T I O N\033[1;31m \033[1;37m[0x00]
    NNNh+++    ++#+++++++++++#++    +++hNNN
    NNNm         #     +     #         mNNN
    :NNN+         #    +    #         +NNN:       
     NNNm-         *:#####:*         -mNNN
      NNNN\            +            /NNNN
       NNNNy.                     -yNNNN
         NNNNy:`       +       `:yNNNN"
          :NNNNmy+:.   +   .:+ymNNNN:
	    *:NNNNNNNmddddNNNNNNNN*
	       *:!NNNNNNNNNNN!:*
                    '''*'''

"""
    print B+'   [1] '+C+' Basic Bugs & Misconfigurations'+W+' (Low Priority [P0x3-P0x4])'
    time.sleep(0.2)
    print B+'   [2] '+C+' Critical Vulnerabilities '+W+'(High Priority [P0x1-P0x2])'
    time.sleep(0.2)
    print B+'   [3] '+C+' Others '+W+'(Bruters)\n'
    time.sleep(0.2)
    print B+'   [99] '+C+'Back\n'
    time.sleep(0.2)

