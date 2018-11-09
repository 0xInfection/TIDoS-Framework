#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author: @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework

from __future__ import print_function
import os
import re
import sys
import time
import requests
sys.path.append('files/signature-db/waf-signatures/')
from core.Core.colors import *
from wafimpo import *
from time import sleep

wafs = ['Airlock','Anquanboa','Armor','Asm','AWS','Baidu','Barracuda','BetterWPSecurity','F5 BigIP','BinarySec','BlackDoS','Cisco ACE XML',
 'Cloudflare','Cloudfront','Comodo','Data Power','Deny All','Dot Defender','Edge Cast','Expression Engine','Forti Web','Hyper Guard','Incapsula',
 'Isa Server','Jiasule','Known Sec','Kona','ModSecurity','Net Continuum','Net Scaler','New Defense','NS Focus','Palo Alto','Profense', 'Radware',
'RequestValidation Mode','Safe3','SafeDog','Secure IIS','Secure Ngnix','Site Lock','Sonic Wall','Sophos','Sting Ray','Sucuri','Teros',
'Traffic Sheild','URL Scan','USPSes','Varnish','Wall Alarm','Web Knight','Yundun','Yunsuo']

def getReq0x00(web):

    print(O+' [!] Making the request...')
    req = requests.get(web)
    sleep(0.7)
    return req.headers,req.content

def detectWaf0x00(headers,content):

    waf0x00 = (
            airlock(headers,content),
            anquanboa(headers,content),
            armor(headers,content),
            asm(headers,content),
            aws(headers,content),
            baidu(headers,content),
            barracuda(headers,content),
            betterwpsecurity(headers,content),
            bigip(headers,content),
            binarysec(headers,content),
            blockdos(headers,content),
            ciscoacexml(headers,content),
            cloudflare(headers,content),
            cloudfront(headers,content),
            comodo(headers,content),
            datapower(headers,content),
            denyall(headers,content),
            dotdefender(headers,content),
            edgecast(headers,content),
            expressionengine(headers,content),
            fortiweb(headers,content),
            hyperguard(headers,content),
            incapsula(headers,content),
            isaserver(headers,content),
            jiasule(headers,content),
            knownsec(headers,content),
            kona(headers,content),
            modsecurity(headers,content),
            netcontinuum(headers,content),
            netscaler(headers,content),
            newdefend(headers,content),
            nsfocus(headers,content),
            paloalto(headers,content),
            profense(headers,content),
            radware(headers,content),
            requestvalidationmode(headers,content),
            safe3(headers,content),
            safedog(headers,content),
            secureiis(headers,content),
            senginx(headers,content),
            sitelock(headers,content),
            sonicwall(headers,content),
            sophos(headers,content),
            stingray(headers,content),
            sucuri(headers,content),
            teros(headers,content),
            trafficshield(headers,content),
            urlscan(headers,content),
            uspses(headers,content),
            varnish(headers,content),
            wallarm(headers,content),
            webknight(headers,content),
            yundun(headers,content),
            yunsuo(headers,content)
            )
    return waf0x00

def waf(web):

    check = 0x00
    print(GR+' [*] Loading module...')
    time.sleep(0.7)
    print(R+'\n    ===============================')
    print(R+'     W A F   E N U M E R A T I O N ')
    print(R+'    ===============================\n')
    time.sleep(0.7)
    print(GR+' [*] Testing the firewall/loadbalancer...')
    time.sleep(1)
    head, con = getReq0x00(web)
    waftypes = detectWaf0x00(head, con)
    for i in xrange(0,len(waftypes)):
        try:
            if waftypes[i] != None and waftypes[i] != '':
                print(GR+'\n [*] Response seems to be matching a WAF signature...')
                time.sleep(0.6)
                print(O+' [+] The website seems to be behind a WAF...')
                time.sleep(0.6)
                print(B+' [+] Firewall Detected : ' +C+waftypes[i])
                check = 0x01
                break

            else:
                print(B+'\r [+] Matching signatures for : '+C+wafs[i])
                time.sleep(0.1)

        except Exception as e:
            pass

    if check == 0x00:
        print(R+' [-] Generic detection failed to fingerprint WAF...')

    print(G+'\n [+] WAF Fingerprinting module completed!\n')
