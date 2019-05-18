#!/usr/bin/env python

def other(target):
    from core.build_menu import buildmenu
    module = 'Misconfigurations and Lower Priority Vulnerabilities'
    art=''
    for host in target:
        host.lvl1=module
    menu = { # '#' : ['module', 'description', 'function']
        '1':['FTP Brute','xxx','ftpbrute'],\
        '2':['SSH Brute','xxx','sshbrute'],\
        '3':['SQL Brute','xxx','sqlbrute'],\
        '4':['POP 3/2 Brute','xxx','popbrute'],\
        '5':['SMTP Brute','xxx','smtpbrute'],\
        '6':['TELNET Brute','xxx','telnetbrute'],\
        '7':['XMPP Brute','xxx','xmppbrute'],\
    }
    buildmenu(target,menu,module,art)          # build menu