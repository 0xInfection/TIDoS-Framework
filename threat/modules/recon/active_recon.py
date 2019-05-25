#!/usr/bin/env python

def active_recon(target):
    from core.build_menu import buildmenu
    module = 'Active Reconnaissance'
    art=''
    for host in target:
        host.lvl1=module
    menu = { # '#' : ['module', 'description', 'function']
        # '1':['Ping/NPing Enumeration','xxx','piwebenum'],\
        # '2':['Grab HTTP Headers','xxx','grabhead'],\
        # '3':['HTTP Allowed Methods','xxx','httpmethods'],\
        '4':['robots.txt/sitemap.xml Hunt','Checks for public site data','robot'],\
        # '5':['Scrape Comments','xxx','commentssrc'],\
        # '6':['Traceroute','xxx','traceroute'],\
        # '7':['DNS Hosts','xxx','sharedns'],\
        # '8':['SSL Certificate','xxx','sslcert'],\
        # '9':['CMS Detection','xxx','cms'],\
        # '10':['Apache Status','xxx','apachestat'],\
        # '11':['WebDAV HTTP Enumeration','xxx','dav'],\
        # '12':['PHPInfo Enumeration','xxx','phpinfo'],\
        # '13':['Server Detection','xxx','serverdetect'],\
        '14':['Alternate Sites','Check for alternate sites based on browser','altsites'],\
        # '15':['File Bruteforcers','xxx','filebrute'],\
    }
    buildmenu(target,menu,module,art)          # build menu