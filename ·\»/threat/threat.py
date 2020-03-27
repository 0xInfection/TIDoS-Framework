#!/usr/bin/env python
import re
import sys
from core.colors import color
from multiprocessing import Queue

# menu 1

menu = { # '#' : ['module', 'description', 'function']
        '1':['Reconnaissance & OSINT','Passive/Active Recon & Information Disclosure','recon'],\
        '2':['Scanning & Enumeration','Port Scanning and Directory Enumeration','scanenum'],\
        '3':['Vulnerability Analysis','Check for bugs, misconfigs, crit vulns, and bruters','vulnysis'],\
        '4':['Exploitation','Exploit Modules','exploitation'],\
        '5':['Auxillary Modules','Auxillary Modules','aux'],\
        '6':['Database', 'Access Stored Results', 'db_menu'],\
        '7':['Settings','View/Change Settings','settings'],\
    }

processes=[]
target=[]
tasks_to_accomplish = Queue()
tasks_that_are_done = Queue()
database = './database/tidos.db'

class Target:
    def __init__(self,name,current_menu,last_menu,main_menu,ip):
        self.name = name
        self.current_menu = current_menu
        self.last_menu = last_menu
        self.main_menu = main_menu
        self.settings_menu=''
        self.lvl1 = ''
        self.lvl2 = ''
        self.lvl3 = ''
        self.module = ''
        self.description = ''
        self.ip = ip
        self.port = ''
        self.cmd_options = {}
        self.nmap = ''
        self.lvl = 0
        self.last_lvl=0
        self.database = database
        self.option = ''
        self.dork=''
        self.help = ''
        self.options_list = ''
        self.options_str = ''
        self.cmd_str = ''
        self.usernames=[]
        self.emails=[]
        self.website = ''
        self.run_file = ''

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

def threat():
    valid_ip_regex = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    valid_host_regex = r'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$'
    host_valid = False
    while True:
        try:
            while(host_valid is False):
                temp = input('\n[#] Input Host/IP (ie: 192.168.10.1):> ')# DEBUG: temp value
                if '//' in temp:
                    host=temp.replace('http://','').replace('https://','')
                else:
                    host=temp
                if(host.lower() == 'exit' or host.lower() == 'q'):
                    sys.exit()
                elif(re.match(valid_host_regex, host) or re.match(valid_ip_regex, host)):
                    host_valid =True
                    current_menu = menu
                    last_menu = menu
                    ip = host
                    target.append(Target(temp,current_menu,last_menu,menu,ip))
                    buildmenu(target,menu,'Main Menu','')
                else:
                    print(color.red("Invalid Host Address, try again: "))
                    host_valid = False
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

