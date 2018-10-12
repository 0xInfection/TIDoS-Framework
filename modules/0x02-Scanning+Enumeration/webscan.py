#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework

from __future__ import print_function
import socket
import sys
import json
import requests
import re
import time
from core.Core.colors import *

def webscan(web):

    try:
        print(R+'\n    ===========================================')
        print(R+'     W E B S E R V E R   E N U M E R A T I O N')
        print(R+'    ===========================================')
        print(O+' [This module will scan the whole CENSYS database for')
        print(O+'      collecting domain based IP Addresses and ')
        print(O+'           fingerprint them accordingly]\n')
        time.sleep(0.6)
        print(R+' [-] WARNING: Use this module with caution!')
        print(GR+' [*] Importing API Key...')
        try:
            from files.API_KEYS import CENSYS_UID, CENSYS_SECRET
        except IOError as ImportError:
            print(R+' [-] Error while importing key...')

        web = web.split('//')[1]
        print(O+' [!] Obtaining reverse DNS lookup...')
        time.sleep(0.7)
        ip = web
        print(G+' [+] Identified IP : '+O+str(ip))
        print(GR+' [*] Starting internet wide server scan...')
        if CENSYS_SECRET != '' and CENSYS_UID != '':

            print(G+' [+] Found Censys UID Key : '+O+CENSYS_UID)
            print(G+' [+] Found Censys Secret Token : '+O+CENSYS_SECRET)

            pages = float('inf')
            page = 1

            print(GR+' [*] Setting scan parameters...')
            while page <= pages:

                base_url = 'https://www.censys.io/api/v1'
                params = {'query' : ip, 'page' : page}
                res = requests.post(base_url + "/search/ipv4", json = params, auth = (CENSYS_UID, CENSYS_SECRET))
                payload = res.json()

                for r in payload['results']:

                    ip = r["ip"]
                    proto = r["protocols"]
                    proto = [p.split("/")[0] for p in proto]
                    proto.sort(key=float)
                    protoList = ','.join(map(str, proto))

                    print(B+' [+] IP : '+C+str(ip)+O+' - Protocols : '+str(protoList))

                    if '80' in protoList:
                        view(ip, base_url, CENSYS_UID, CENSYS_SECRET)

                pages = payload['metadata']['pages']
                page += 1

        else:
            print(R+' [-] CENSYS API TOKENs not set!')
            print(R+' [-] This module cannot be used!')

    except Exception as e:
        print(R+' [-] Unhandled Exception Encountered!')
        print(R+' [-] Error : '+str(e))

def view(server, ur, uid, sec):

    res = requests.get(ur + ("/view/ipv4/%s" % server), auth = (uid, sec))
    payload = res.json()

    try:
        if 'title' in payload['80']['http']['get'].keys():
            print(O+" [+] Title : "+GR+"%s" % payload['80']['http']['get']['title'])
        if 'server' in payload['80']['http']['get']['headers'].keys():
            print(C+" [+] Server : "+GR+"%s" % payload['80']['http']['get']['headers']['server'])

    except Exception as error:
        print(R+' [-] Exception : '+str(error))
