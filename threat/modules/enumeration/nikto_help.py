#!/usr/bin/env python

import subprocess

def nikto_help(target):
    print('NIKTO HELP')
    from core.build_menu import buildmenu

    nikto_help = subprocess('nikto -H', shell=True)

    # menu = { # '#' : ['module', 'description', 'function']
    #     '1':['Ping Sweep','(Scan a range of targets/IPs)','xxx'],\
    #     '2':['Port Scanning','(Various port scan types)','nmap_menu'],\
    #     '3':['Crawling','(Public and Brute Force methods)','xxx'],\
    #     '4':['Nikto Menu','(Web Server Vulnerability Scans Menu)','nikto_menu'],\
    #     '5':['Windows Enumeration','(Windows Specific Enumeration)','windows_enum'],\
    #     'B':['Back','(Nikto Help Page)',subprocess.run('nikto -H', shell=True)],\
    # }

    print(" " + color.custom('[B] Back',bold=True,white=True,bg_red=True)+'\n')

    # for host in target:
    #     print('NIKTO MENU HOST', dict(host))
    #     host.lvl2 = 'Nikto'

    #     nikto_cmd_dict = host.cmd_options
    #     print('CMD OPTIONS DICT', nikto_cmd_dict)

    buildmenu(target,target[0].last_menu,'','')          # build menu