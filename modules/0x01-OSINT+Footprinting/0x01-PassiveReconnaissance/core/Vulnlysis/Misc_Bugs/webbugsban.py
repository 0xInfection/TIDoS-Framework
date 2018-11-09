#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import time
import os
from core.Core.colors import *
from core.Core.arts import bugsban_art

def webbugsban():

    os.system('clear')
    print(bugsban_art)
    print(O+'  [1]'+GR+' Insecure Cross Origin Resource Sharing'+W+' (Absolute)')
    time.sleep(0.1)
    print(O+'  [2]'+GR+' Same Site Scripting'+W+' (Sub-Domains Based)')
    time.sleep(0.1)
    print(O+'  [3]'+GR+' Clickjackable Vulnerabilities '+W+'(Framable Response)')
    time.sleep(0.1)
    print(O+'  [4]'+GR+' Zone Transfer Vulnerabilities'+W+' (DNS Based)')
    time.sleep(0.1)
    print(O+'  [5]'+GR+' Security on Cookies '+W+'(HTTPOnly & Secure Flags)')
    time.sleep(0.1)
    print(O+'  [6]'+GR+' Security Headers Analysis '+W+'(Absolute)')
    time.sleep(0.1)
    print(O+'  [7]'+GR+' Cloudflare Misconfiguration '+W+'(Get Real IP) ')
    time.sleep(0.1)
    print(O+'  [8]'+GR+' HTTP Strict Transport Security Usage ')
    time.sleep(0.1)
    print(O+'  [9]'+GR+' Cross-Site Tracing '+W+'(Port Based)')
    time.sleep(0.1)
    print(O+'  [10]'+GR+' Network Security Misconfig. '+W+'(Telnet Port Based)')
    time.sleep(0.1)
    print(O+'  [11]'+GR+' Spoofable Emails '+W+'(Missing SPF & DMARC Records) ')
    time.sleep(0.1)
    print(O+'  [12]'+GR+' Host Header Injection '+W+'(Port Based) ')
    time.sleep(0.1)
    print(O+'  [13]'+GR+' Cookie Injection '+W+'(Session Fixation)\n ')
    time.sleep(0.1)
    print(O+'  [A]'+GR+' Load all the modules 1 by 1\n')
    time.sleep(0.1)
    print(O+'  [99]'+GR+' Back\n')
