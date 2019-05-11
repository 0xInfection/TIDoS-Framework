#!/usr/bin/env python
import requests
#import os
from core.colors import color
links = []

def revip(target):
    for t in target:
        site = t.name.replace('http://','').replace('https://','')
        print(' [!] Looking Up for Reverse IP Info...')
        print(' [~] Result : \n')
        text = requests.get('http://api.hackertarget.com/reverseiplookup/?q=' + site).text
        result = str(text)
        res = result.splitlines()
        if 'error' not in result:
            for r in res:
                print(color.yellow(' [+] Site :> ')+ color.green(r))
                #links.append(r)

                # p = 'tmp/logs/'+web+'-logs/'+str(web)+'-reverse-ip.lst'
                # open(p,'w+')
                # print(B+' [!] Saving links...')
                # time.sleep(1)
                # for m in links:
                #     m = m + '\n'
                #     ile = open(p,"a")
                #     ile.write(m)
                #     ile.close()
                # pa = os.getcwd()
                # print(G+' [+] Links saved under '+pa+'/'+p+'!')
                # print('')

        elif 'error' in result:
            print(color.red(' [-] Outbound Query Exception!'))

