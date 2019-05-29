#!/usr/bin/env python

def misconfig(target):
    from core.build_menu import buildmenu
    module = 'Misconfigurations and Lower Priority Vulnerabilities'
    art=''
    for host in target:
        host.lvl1=module
    menu = { # '#' : ['module', 'description', 'function']
        '1':['iCORS','xxx','icors'],\
        '2':['Same Site Scripting','xxx','ssscript'],\
        '3':['Clickjack','xxx','clickjack'],\
        '4':['Zone Transfer','xxx','zone'],\
        '5':['Cookie Check','xxx','cookiecheck'],\
        '6':['Sec. Headers','xxx','headers'],\
        '7':['Cloudflare Misconfig','xxx','cloudflaremisc'],\
        '8':['HSTS Check','xxx','hsts'],\
        '9':['Cross Site Tracing','xxx','xsstrace'],\
        '10':['Telnet Enabled','xxx','netmisc'],\
        '11':['Email Spoof','xxx','mailspoof'],\
        '12':['Host Header Injection','xxx','hhi'],\
        '13':['Cookie Injection','xxx','sessionfix'],\
    }
    buildmenu(target,menu,module,art)          # build menu