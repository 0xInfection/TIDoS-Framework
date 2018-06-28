#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework  

import time
import os
from colors import *

def webbugsban():

    os.system('clear')
    print C+'''
\033[1;34m
   ______________________________________________________
  |  \033[1;37mTIDoS Dialog  (v2.1.0)                \033[1;33m[-] [口] [×]  \033[1;34m|
  | ---------------------------------------------------- |
\033[1;36m  |                                                      |
  |  \033[1;33mTIDoS has detected that you want to hunt for bugs! \033[1;36m |
  |   \033[1;33mDo you wish to continue?                          \033[1;36m |
  |                                                      |
  |     \033[1;37m.----------.   .----------.    .----------.      \033[1;36m|  
  |     \033[1;37m|    Yes   \033[1;37m|   |    No    \033[1;37m|    |   Maybe  \033[1;37m|      \033[1;36m|
  |     \033[1;37m'----------'   '----------'    '----------'     \033[1;36m |
  |______________________________________________________|

'''

    print O+'  [1]'+GR+' Insecure Cross Origin Resource Sharing'
    time.sleep(0.1)
    print O+'  [2]'+GR+' Same Site Scripting'
    time.sleep(0.1)
    print O+'  [3]'+GR+' Clickjackable Vulnerabilities '
    time.sleep(0.1)
    print O+'  [4]'+GR+' Zone Transfer Vulnerabilities'
    time.sleep(0.1)
    print O+'  [5]'+GR+' Missing HTTPOnly/Secure Flags on Cookies '
    time.sleep(0.1)
    print O+'  [6]'+GR+' Security Headers Analysis '
    time.sleep(0.1)
    print O+'  [7]'+GR+' Cloudflare Misconfiguration (Get Real IP) '
    time.sleep(0.1)
    print O+'  [8]'+GR+' HTTP High Transport Security Usage '
    time.sleep(0.1)
    print O+'  [9]'+GR+' Cross-Site Tracing (Port Based)'
    time.sleep(0.1)
    print O+'  [10]'+GR+' Network Security Misconfig. (Telnet Enabled)'
    time.sleep(0.1)
    print O+'  [11]'+GR+' Spoofable Emails (Missing SPF & DMARC Records)\n '
    time.sleep(0.1)
    print O+'  [A]'+GR+' Load all the modules 1 by 1\n'
    time.sleep(0.1)
    print O+'  [99]'+GR+' Back\n'
