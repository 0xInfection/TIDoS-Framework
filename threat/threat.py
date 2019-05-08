#!/usr/bin/env python
import sys
from core.build_menu import buildmenu

menu = { # '#' : ['module', 'description', 'function']
        '1':['Reconnaissance & OSINT','Description','recon'],\
        '2':['Scanning & Enumeration','Description','scanenum'],\
        '3':['Vulnerability Analysis','Description','vulnysis'],\
        '4':['Exploitation','Description','exploitation'],\
        '5':['Post Analysis','Description','post']\
    }

target=[]

class Target:
    def __init__(self,name,current_menu,last_menu,main_menu):
        self.name = name
        self.current_menu = current_menu
        self.last_menu = last_menu
        self.main_menu = main_menu

def threat():
    while True:
        try:
            host = 'www.example.com'# DEBUG: temp value
            current_menu = menu
            last_menu = menu
            target.append(Target(host,current_menu,last_menu,menu))
            buildmenu(target,menu,'Main Menu','')
        except KeyboardInterrupt:
            print("Keyboard interrupted")
        finally:
            sys.exit()

if __name__=='__main__':
    try:
        threat()
    except KeyboardInterrupt:
        print("Keyboard interrupted")
    finally:
        sys.exit()

