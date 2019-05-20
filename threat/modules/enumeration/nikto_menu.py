#!/usr/bin/env python

import subprocess

def nikto_menu(target):
    print('NIKTO MENU')
    from core.build_menu import buildmenu

    menu = { # '#' : ['module', 'description', 'function']
        '1':['Ping Sweep','(Scan a range of targets/IPs)','xxx'],\
        '2':['Port Scanning','(Various port scan types)','nmap_menu'],\
        '3':['Crawling','(Public and Brute Force methods)','xxx'],\
        '4':['Nikto Menu','(Web Server Vulnerability Scans Menu)','nikto_menu'],\
        '5':['Windows Enumeration','(Windows Specific Enumeration)','windows_enum'],\
    }

    # ports = input('\n[#] List Ports to Scan (e.g. 80,443):> ')
    ports = '80, 443'
    # print('PORTS', ports.replace(' ',''))
    # ports_list = ports.replace(' ','')




    for host in target:
        print('NIKTO MENU HOST', dict(host))
        host.help = 'Nikto'
    #     host.lvl2 = 'Nikto'

    #     nikto_cmd_dict = host.cmd_options
    #     print('CMD OPTIONS DICT', nikto_cmd_dict)
        print('NIKTO MENU HOST', dict(host))





    buildmenu(target,menu,'Nikto Scan Configuration','')          # build menu