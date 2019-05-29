#!/usr/bin/env python

# menu 2

def scanenum(target):
    from core.build_menu import buildmenu
    for host in target:
        host.module = 'ScanANDEnum'
        host.lvl1 = 'Scanning & Enumeration'

    menu = { # '#' : ['module', 'description', 'function']
        '1':['Ping Sweep','(Scan a range of targets/IPs)','xxx'],\
        '2':['Port Scanning','(Various port scan types)','nmap_menu'],\
        '3':['Crawling','(Public and Brute Force methods)','photon_menu'],\
        '4':['Nikto Menu','(Web Server Vulnerability Scans Menu)','nikto_menu'],\
        # '5':['Windows Enumeration','(Windows Specific Enumeration)','windows_enum'],\
    }
    buildmenu(target,menu,'Scanning and Enumeration','')          # build menu