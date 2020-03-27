#!/usr/bin/env python

def info_disclosure(target):
    from core.build_menu import buildmenu
    module = 'Information Disclosure'
    art=''
    for host in target:
        host.lvl1=module
    menu = { # '#' : ['module', 'description', 'function']
        '1':['Credit Card Enumeration','(If disclosed in plain text)','creditcards'],\
        # '2':['Extract All Emails','(Absolute)','emailext'],\
        '2':['Enumerate Errors + FPD','(Includes Full Path Disclosure)','errors'],\
        # '4':['Internal IP disclosure','(Find out any leaks of internal IP addresses)','internalip'],\
        # '5':['Extract out all Phone Numbers','(If plaintext disclosure)','phone'],\
        # '6':['Extract out all Social Security Numbers','(US Based)','ssn']
    }
    buildmenu(target,menu,module,art)          # build menu