#!/usr/bin/env python
import socket
import requests
import time
from files.API_KEYS import SHODAN_API_KEY
from core.colors import color
import inspect
import os

def honeypot(target):
    from core.build_menu import buildmenu
    from files.API_KEYS import SHODAN_API_KEY
    for host in target:
        host.lvl2=inspect.stack()[0][3]
        host.lvl3=''    
        print(' [*] Configuring API request...')
        try:
            if SHODAN_API_KEY != '':
                print(color.green(' [+] Key Found : ')+color.yellow(SHODAN_API_KEY))
                if '//' in host.name:
                    web = host.ip.split('//')[1]
                ip = socket.gethostbyname(web)
                honey = "https://api.shodan.io/labs/honeyscore/"+ip+"?key="+SHODAN_API_KEY
                req = requests.get(honey).text
                read = float(req)
                if read < 5.0:
                    print(color.green(' [+] Target does not seem to be a potential Honeypot...'))
                    print(color.green(' [+] Honey Score : '+color.yellow(str(read*100)+'%')))

                else:
                    print(color.red(' [-] Potential Honeypot Detected!'))
                    print(color.red(' [+] Honey Score : '+color.yellow(str(read*100)+'%')))
            else:
                print(color.red(' [-] Shodan API key not set!'))
                print(color.red(' [-] Cannot use this module!'))
                time.sleep(1)
                os.system('clear')
                buildmenu(target,target[0].main_menu,'Main Menu','')
        except EOFError as e:
            # print(color.red(' [-] Shodan API key not set!'))
            # print(color.red(' [-] Cannot use this module!'))
            return
