#!/usr/bin/env python
import sys
from multiprocessing import Queue

# menu 1

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
    def __init__(self,name,current_menu,last_menu,main_menu,ip):
        self.name = name
        self.current_menu = current_menu
        self.last_menu = last_menu
        self.main_menu = main_menu
        self.lvl1 = ''
        self.lvl2 = ''
        self.lvl3 = ''
        self.module = ''
        self.description = ''
        self.ip = ip
        self.port = ''
        self.cmd_options = {}
    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

def threat():
    while True:
        try:
            host = input('\nInput host/IP\n')# DEBUG: temp value
            current_menu = menu
            last_menu = menu
            ip = host
            target.append(Target(host,current_menu,last_menu,menu,ip))
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

