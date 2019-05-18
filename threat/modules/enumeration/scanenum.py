#!/usr/bin/env python

# menu 2

def scanenum(target):
    from core.build_menu import buildmenu
    print('MENU 2')
    # print('TARGET', dict(target[0]))
    # nikto_options = {
    #     '-h': target[0].ip,
    #     '-p': target[0].port
    # }
    # print(nikto_options)
    # target[0].cmd_options.append(nikto_options)

    menu = { # '#' : ['module', 'description', 'function']
        '1':['Ping Sweep','(Scan a range of targets/IPs)','xxx'],\
        '2':['Port Scanning','(Various port scan types)','nmap_menu'],\
        '3':['Crawling','(Public and Brute Force methods)','xxx'],\
        '4':['Nikto','(Web Server Vulnerability Scans)','nikto'],\
        '5':['Windows Enumeration','(Windows Specific Enumeration)','windows_enum'],\
    }
    buildmenu(target,menu,'Scanning and Enumeration','')          # build menu