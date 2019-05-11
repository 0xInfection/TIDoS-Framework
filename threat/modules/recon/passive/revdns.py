#!/usr/bin/env python
import os
import time
import requests
from core.colors import color
links = []

def revdns(target):
    for t in target:
        site = t.name.replace('http://','').replace('https://','')
        print('[!] Looking Up for Reverse DNS Info...')
        print(' [~] Result: \n')
        text = requests.get('http://api.hackertarget.com/reversedns/?q=' + site)
        result = text.text.split(' ')
        if 'error' not in result and 'no' != result[0]:
            #res = result.splitlines()
            #for r in result:
            print(color.blue(' [+] Received : ')+color.yellow(result[0])+color.white(' => ')+color.blue('('+result[1].strip()+')'))

            #p = 'tmp/logs/'+web+'-logs/'+web+'-reverse-dns.lst'
            #open(p,'w+')
            #print(B+' [!] Saving links...')

            # for m in links:
            #     print(m)
            #     m = m + '\n'
            #     ile = open(p,"a")
            #     ile.write(m)
            #     ile.close()
            # pa = os.getcwd()
            # print(G+' [+] Links saved under '+pa+'/'+p+'!')
            # print('')

        else:
            print(color.red(' [-] No result found!'))


