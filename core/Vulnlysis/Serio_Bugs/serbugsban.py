#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import time
from core.Core.colors import *
import os
from core.Core.arts import bugsban_art

def serbugsban():

    time.sleep(0.5)
    os.system('clear')
    print(bugsban_art)
    print(B+'  [1]'+C+' Local File Inclusion'+W+' (Root Directories)')
    time.sleep(0.1)
    print(B+'  [2]'+C+' Remote File Inclusion'+W+' (Executable Scripts)')
    time.sleep(0.1)
    print(B+'  [3]'+C+' OS Command Injection'+W+' (Windows & Linux)')
    time.sleep(0.1)
    print(B+'  [4]'+C+' Path Traversal '+W+'(Sensitive Paths)')
    time.sleep(0.1)
    print(B+'  [5]'+C+' Cross-Site Request Forgery '+W+'(Absolute)')
    time.sleep(0.1)
    print(B+'  [6]'+C+' Cross-Site Scripting '+W+'(Absolute)')
    time.sleep(0.1)
    print(B+'  [7]'+C+' SQL Injection '+W+'(Error & Blind Based)')
    time.sleep(0.1)
    print(B+'  [8]'+C+' LDAP Entity Injection '+W+'(Error Enumeration)')
    time.sleep(0.1)
    print(B+'  [9]'+C+' HTML Code Injection '+W+'(Tag Based)')
    time.sleep(0.1)
    print(B+'  [10]'+C+' HTTP Response Splitting '+W+'(CRLF Injection)')
    time.sleep(0.1)
    print(B+'  [11]'+C+' PHP Code Injection '+W+'(Windows + Linux)')
    time.sleep(0.1)
    print(B+'  [12]'+C+' XPATH Injection '+W+'(Blind and Error Based)')
    time.sleep(0.1)
    print(B+'  [13]'+C+' Shellshock Vulnerabilities'+W+' (Bash RCE)')
    time.sleep(0.1)
    print(B+'  [14]'+C+' Apache Struts Shock'+W+' (Apache RCE)')
    time.sleep(0.1)
    print(B+'  [15]'+C+' Unvalidated URL Redirects'+W+' (Open Redirects)')
    time.sleep(0.1)
    print(B+'  [16]'+C+' Sub-domain Takeover'+W+' (50+ Services)\n')
    time.sleep(0.1)
    print(B+'  [A]'+C+' Load all the modules 1 by 1\n')
    time.sleep(0.1)
    print(B+'  [99]'+C+' Back\n')
