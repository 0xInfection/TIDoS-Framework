#!/usr/bin/env python

# menu 3

def passive_recon(target):
    from core.build_menu import buildmenu
    module = 'Passive Reconnaissance & OSINT'
    art=''
    for host in target:
        host.lvl1=module
    menu = { # '#' : ['module', 'description', 'function']
        '1':['dig lookup','(DIG SCAN)','dig'],\
        '2':['WhoIS lookup','(Gather via Interaction)','whois'],\
        '3':['NPING','(NPING Target)','nping'],\
        '4':['GeoIP Lookup','','getgeoip'],\
        '5':['DNS Lookup','','dnschk'],\
        '6':['Subdomain Scan','','subdom'],\
        '7':['Reverse DNS Lookup','(Reverse DNS Lookup)','revdns'],\
        '8':['Subnet Enumeration','(Enumerate subnets)','subnet'],\
        '9':['Reverse IP Lookup','(Reverse IP Lookup)','revip'],\
        '10':['IP History','(Lookup previous IP addresses)','iphistory'],\
        '11':['Page Links','','links'],\
        '12':['Google Search','(Google Search)','gsearch'],\
        '13':['Google Dorker','','googledorker'],\
        '14':['Wayback Machine','','webarchive'],\
        '15':['Hacked Email Check','','hackedmail'],\
        '16':['Mail to Domain','','mailtodom'],\
        '17':['Google Groups Enum','','googlegroups'],\
        '18':['Check Username','','checkuser'],\
        '19':['PasteBin Posts','','pastebin'],\
        '20':['LinkedIn Gathering','(Lookup LinkedIn Profiles)','linkedin'],\
        '21':['Google Plus Gathering','','googlenum'],\
        '22':['Public Contact Info','','getconinfo'],\
        '23':['CENSYS Gathering','','censysdom'],\
        '24':['Threat Intel Gathering','','threatintel'],\
    }
    buildmenu(target,menu,module,art)          # build menu