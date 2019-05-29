#!/usr/bin/env python
from core.Core.arts import scanenumban_art

def scanenum(web):
    from core.Core.build_menu import buildmenu
    menu = { # '#' : ['module', 'description', 'function']
        '1':['WAF Analysis','(Web Application Firewall)','waf'],\
        '2':['Port Scanning','','portscan'],\
        '3':['Interactive NMap','','nmapmain'],\
        '4':['WebTech Fingerprinting','','webtech'],\
        '5':['SSL Enumeration','','ssltlsscan'],\
        '6':['OS Fingerprinting','','osdetect'],\
        '7':['Banner Grab','','bannergrab'],
        '8':['IP Crawler','','webscan'],
        '9':['Web Crawlers','','crawlers'],
    }
    buildmenu(web,menu,'Scanning and Enumeration',scanenumban_art)          # build menu