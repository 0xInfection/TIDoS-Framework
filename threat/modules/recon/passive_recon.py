#!/usr/bin/env python

def passive_recon(target):
    from core.build_menu import buildmenu
    menu = { # '#' : ['module', 'description', 'function']
        '1':['dig lookup','(DIG SCAN)','dig'],\
        '2':['WhoIS lookup','(Gather via Interaction)','whois'],\
        '3':['NPING','','nping'],\
        '4':['GeoIP Lookup','','getgeoip'],\
        '5':['DNS Lookup','','dnschk'],\
        '6':['Subdomain Scan','','subdom'],\
        '7':['Reverse DNS Lookup','','revdns'],\
        '8':['Subnet Enumeration','','subnet'],\
        '9':['Reverse IP Lookup','','revip'],\
        '10':['IP History','','iphistory'],\
        '11':['Page Links','','links'],\
        '12':['Google Search','','gsearch'],\
        '13':['Google Dorker','','googledorker'],\
        '14':['Wayback Machine','','webarchive'],\
        '15':['Hacked Email Check','','hackedmail'],\
        '16':['Mail to Domain','','mailtodom'],\
        '17':['Google Groups Enum','','googlegroups'],\
        '18':['Check Username','','checkuser'],\
        '19':['PasteBin Posts','','pastebin'],\
        '20':['LinkedIn Gathering','','linkedin'],\
        '21':['Google Plus Gathering','','googlenum'],\
        '22':['Public Contact Info','','getconinfo'],\
        '23':['CENSYS Gathering','','censysdom'],\
        '24':['Threat Intel Gathering','','threatintel'],\
    }
    buildmenu(target,menu,'Passive Reconnaissance & OSINT','')          # build menu