#!/usr/bin/env python
import sys

from multiprocessing import Queue

menu = { # '#' : ['module', 'description', 'function']
        '1':['Reconnaissance & OSINT','Description','recon'],\
        '2':['Scanning & Enumeration','Description','scanenum'],\
        '3':['Vulnerability Analysis','Description','vulnysis'],\
        '4':['Exploitation','Description','exploitation'],\
        '5':['Post Analysis','Description','post']\
    }

processes=[]
target=[]
tasks_to_accomplish = Queue()
tasks_that_are_done = Queue()

class Target:
    def __init__(self,name,current_menu,last_menu,main_menu):
        self.name = name
        self.current_menu = current_menu
        self.last_menu = last_menu
        self.main_menu = main_menu
        self.module=''
        self.description=''
        self.ip=''

def threat():
    while True:
        try:
            host = '1.1.1.1'# DEBUG: temp value
            current_menu = menu
            last_menu = menu
            target.append(Target(host,current_menu,last_menu,menu))
            buildmenu(target,menu,'Main Menu','')
        except KeyboardInterrupt:
            print("Keyboard interrupted")
        finally:
            sys.exit()

if __name__=='__main__':
    from core.build_menu import buildmenu
    try:
        threat()
    except KeyboardInterrupt:
        print("Keyboard interrupted")
    finally:
        sys.exit()

