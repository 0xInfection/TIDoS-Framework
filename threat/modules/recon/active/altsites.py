#!/usr/bin/env python
from core.colors import color
from database.database_module import save_data
import inspect

import os
import time
import requests
import hashlib

md5s = {}
responses = {}

def altsites(target):
    from core.build_menu import buildmenu
    for host in target:
        host.lvl2=inspect.stack()[0][3]
        host.lvl3=''
        if '//' in host.name:
            site = host.name
        else:
            site = 'https://'+host.name
        print(color.green(' [*] Setting User-Agents...'))
        time.sleep(0.7)
        user_agents = {
                'Chrome on Windows 8.1' : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36',
                'Safari on iOS'         : 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4',
                'IE6 on Windows XP'     : 'Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
                'Googlebot'             : 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
                }

        print(color.green('\n [*] Preparing for series of requests...'))
        for name, agent in user_agents.items():
            print(color.blue(' [+] Using User-Agent : ')+name)
            print(color.green(' [+] UA Value : ')+color.yellow(agent))
            headers = {'User-Agent' : agent}
            print(color.green(' [*] Making the request...'))
            req = requests.get(site, headers=headers, allow_redirects=True, verify=True)
            responses[name] = req

        print(color.yellow('\n [!] Comparing base value standards...'))
        time.sleep(0.5)
        for name, response in responses.items():
            print(color.blue(' [+] User-Agent : ')+name)
            print(color.green(' [+] Response : ')+color.yellow(str(response)))
            md5s[name] = hashlib.md5(response.text.encode('utf-8')).hexdigest()

        print(color.yellow('\n [!] Matching hexdigest signatures...'))
        for name, md5 in md5s.items():
            print(color.blue('\n [+] User-Agent : ')+name)
            print(color.green(' [+] Hex-Digest : ')+color.yellow(str(md5)))
            if name != 'Chrome on Windows 8.1':
                if md5 != md5s['Chrome on Windows 8.1']:
                    print(color.green(' [+] ')+color.yellow(str(name))+color.green(' differs fromk baseline!'))
                else:
                    print(color.red(' [-] No alternative site found via User-Agent spoofing:')+ str(md5))
        print(color.green('\n [+] Alternate Site Discovery Completed!\n'))
