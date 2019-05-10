#!/usr/bin/env python

def scanenum(target):
    from core.build_menu import buildmenu
    menu = { # '#' : ['module', 'description', 'function']
        '1':['Ping Sweep','(Scan a range of targets/IPs)','xxx'],\
        '2':['Port Scanning','(Various port scan types)','xxx'],\
        '3':['Crawling','(Public and Brute Force methods)','xxx'],\
    }
    buildmenu(target,menu,'Scanning and Enumeration','')          # build menu