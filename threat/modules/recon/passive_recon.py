#!/usr/bin/env python

# menu 3

def passive_recon(target):
    from core.build_menu import buildmenu
    module = 'Passive Reconnaissance & OSINT'
    art=''
    for host in target:
        host.lvl1=module
    menu = { # '#' : ['module', 'description', 'function']
        '1':['HackerTarget','(Run all HackerTarget.com passive checks)','hackertarget'],\
        '2':['dig lookup','(DIG SCAN)','dig'],\
        '3':['WhoIS lookup','(Gather via Interaction)','whois'],\
        '4':['NPING','(NPING Target)','nping'],\
        '5':['GeoIP Lookup','(Geographic IP Lookup)','getgeoip'],\
        '6':['Reverse DNS Lookup','(Reverse DNS Lookup)','revdns'],\
        '7':['Subnet Enumeration','(Enumerate subnets)','subnet'],\
        '8':['Reverse IP Lookup','(Reverse IP Lookup)','revip'],\
        '9':['IP History','(Lookup previous IP addresses)','iphistory'],\
        '10':['Google Search','(Google Search)','gsearch'],\
        '11':['Check Username','(Check 160+ social media sites for username)','checkuser'],\
        '12':['LinkedIn Gathering','(Lookup LinkedIn Profiles)','linkedin'],\
        '13':['Public Contact Info','(all fullcontact.com information)','getconinfo'],\
        '14':['CENSYS Gathering','(Gather CENSYS data if API not used up)','censysdom'],\
        # '5':['DNS Lookup','','dnschk'],\
        # '6':['Subdomain Scan','','subdom'],\
        # '11':['Page Links','','links'],\
        # '13':['Google Dorker','','googledorker'],\
        # '14':['Wayback Machine','','webarchive'],\
        # '15':['Hacked Email Check','','hackedmail'],\
        # '16':['Mail to Domain','','mailtodom'],\
        # '17':['Google Groups Enum','','googlegroups'],\
        # '19':['PasteBin Posts','','pastebin'],\
        # '21':['Google Plus Gathering','','googlenum'],\
        # '24':['Threat Intel Gathering','','threatintel'],\
    }
    buildmenu(target,menu,module,art)          # build menu