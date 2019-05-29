#!/usr/bin/env python

def critical(target):
    from core.build_menu import buildmenu
    module = 'Critical Vulnerabilities'
    art=''
    for host in target:
        host.lvl1=module
    menu = { # '#' : ['module', 'description', 'function']
        '1':['LFI','xxx','lfi'],\
        '2':['RFI','xxx','rfi'],\
        '3':['RCE','xxx','rce'],\
        '4':['Path Traversal','xxx','pathtrav'],\
        '5':['CSRF','xxx','csrf'],\
        '6':['XSS','xxx','xss'],\
        '7':['SQLi','xxx','sqli'],\
        '8':['LDAP Injection','xxx','ldap'],\
        '9':['HTML Code Injection','xxx','htmli'],\
        '10':['HTTP Response Splitting','xxx','crlf'],\
        '11':['PHP Code Injection','xxx','phpi'],\
        '12':['XPATH Injection','xxx','xpathi'],\
        '13':['Shellshock','xxx','shellshock'],\
        '14':['Apache Struts Shock','xxx','strutsshock'],\
        '15':['URL Validation','xxx','redirect'],\
        '16':['Subdomain Takeover','xxx','subdomover'],\
    }
    buildmenu(target,menu,module,art)          # build menu