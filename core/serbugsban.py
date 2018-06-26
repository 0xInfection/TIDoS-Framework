#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/the-Infected-Drake/TIDoS-Framework  

import time
from colors import *
import os

def serbugsban():

    time.sleep(0.5)
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

    print B+'  [1]'+C+' Local File Intrusion'
    time.sleep(0.1)
    print B+'  [2]'+C+' Remote File Intrusion'
    time.sleep(0.1)
    print B+'  [3]'+C+' Remote Command Execution'
    time.sleep(0.1)
    print B+'  [4]'+C+' Path Traversal (Sensitive Paths) '
    time.sleep(0.1)
    print B+'  [5]'+C+' Cross-Site Request Forgery '
    time.sleep(0.1)
#    print B+'  [6]'+C+' Cross-Site Scripting '
#    time.sleep(0.1)
    print B+'  [7]'+C+' SQL Injection '
    time.sleep(0.1)
    print B+'  [8]'+C+' HTTP Response Splitting '
    time.sleep(0.1)
    print B+'  [9]'+C+' Host Header Injection '
    time.sleep(0.1)
    print B+'  [10]'+C+' Shellshock Vulnerabilities'
    time.sleep(0.1)
    print B+'  [11]'+C+' Unvalidated Redirects\n'
    time.sleep(0.1)
    print B+'  [A]'+C+' Load all the modules 1 by 1\n'
    time.sleep(0.1)
    print B+'  [99]'+C+' Back\n'

