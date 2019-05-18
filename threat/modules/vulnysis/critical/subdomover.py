#!/usr/bin/env python
from core.colors import color
def subdomover(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author: @_tID
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import re
# import os
# import sys
# import time
# import urllib3
# import urlparse
# import requests
# from core.Core.colors import *
# from subdom0x00 import subdom0x00
# from signatures import services
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# def getReq0x00(url):

#     print(GR+' [*] Setting headers...')
#     headers = {
#                     'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
#                     'Accept-Language':'en-US;',
#                     'Accept-Encoding': 'gzip, deflate',
#                     'Accept': 'text/html,application/xhtml+xml,application/xml;',
#                     'Connection':'close'
#             }

#     try:
#         print(O+' [!] Making the no-verify request...')
#         req = requests.get(url=url, headers=headers, timeout=7, allow_redirects=False, verify=False)
#         return req.status_code,req.content

#     except Exception as e:
#         print(R+' [-] Exception : '+str(e))
#         pass

#     return None, None

# def check0x00(status,content):

#     code = ""
#     error = ""

#     print(GR+' [*] Searching through signatures...')
#     time.sleep(0.7)
#     for service in services:
#         values = services[service]

#         for value in values:
#             stfu = services[service][value]
#             if value == 'error':
#                 error = stfu
#             if value == 'code':
#                 code = stfu

#         if re.search(code,str(status),re.I) and re.search(error,str(content),re.I):
#             return service,error

#     return None, None

# def subdomover(web):

#     print(R+'\n    =====================================')
#     print(R+'     S U B D O M A I N   T A K E O V E R ')
#     print(R+'    =====================================\n')

#     time.sleep(0.6)
#     print(O+' Choose from the folowing:\n')
#     print(B+'  [1] '+C+'Single Subdomain '+W+'(Manual)')
#     print(B+'  [2] '+C+'All Subdomains '+W+'(Automated)')
#     v = raw_input(O+'\n [#] Enter type :> '+GR)

#     if v.strip() == '1':

#         su = raw_input(C+' [#] Enter the subdomain :> '+GR)
#         if su.startswith('http'):
#             pass
#         else:
#             su = 'http://'+su
#         time.sleep(0.7)
#         print(O+' [!] Starting enumeration...')
#         time.sleep(0.8)
#         print(R+' [+] Target Locked : '+O+su)
#         status,content = getReq0x00(su)
#         service,error = check0x00(status,content)
#         print(B+' [!] Error : '+C+str(error))
#         print(B+' [!] Service Status : '+C+str(status))
#         print(GR+' [*] Analysing vulnerability...')
#         if service and error:
#             time.sleep(0.5)
#             print(G+' [+] Potential subdomain takeover was found!')
#             print(G+' [+] Service Identified : '+O+str(service))
#         else:
#             time.sleep(0.5)
#             print(R+' [-] No subdomain takeover possible for '+O+su)

#     elif v.strip() == '2':

#         print(C+' [*] Starting enumeration...')
#         time.sleep(0.5)
#         web0 = web.replace('http://','')
#         web0 = web.replace('https://','')
#         if not os.path.exists('tmp/logs/'+web0+'-logs/'):
#             os.makedirs('tmp/logs/'+web0+'-logs/')

#         try:
#             print(GR+' [+] Searching for subdomains file...')
#             if os.path.exists('tmp/logs/'+web0+'-logs/'+web0+'-subdomains.lst'):
#                 pass
#             else:
#                 print(R+' [-] Subdomains file not found!')
#                 print(GR+' [*] Initializing sub-domain gathering...')
#                 subdom0x00(web)

#         except Exception as e:
#             print(R+' [-] Exception occured!')
#             print(R+' [-] Error : '+str(e))

#         with open('tmp/logs/'+web0+'-logs/'+web0+'-subdomains.lst') as sub_domain_list:
#             for sub_domain in sub_domain_list:
#                 print(GR+' [*] Parsing sub-domain...')
#                 sub_domain = sub_domain.replace('\n','')
#                 if sub_domain.startswith('http'):
#                     pass
#                 else:
#                     if 'http://' in web:
#                         sub_domain = 'http://' + sub_domain
#                     elif 'https://' in web:
#                         sub_domain = 'https://' + sub_domain

#                 print(O+'\n [+] Target Url :> '+C+sub_domain)
#                 status,content = getReq0x00(sub_domain)
#                 service,error = check0x00(status,content)
#                 print(B+' [!] Error : '+C+str(error))
#                 print(B+' [!] Service Status : '+C+str(status))
#                 print(GR+' [*] Analysing vulnerability...')
#                 if service and error:
#                     time.sleep(0.5)
#                     print(G+' [+] Potential subdomain takeover was found!')
#                     print(G+' [+] Service Identified : '+O+str(service))
#                 else:
#                     time.sleep(0.5)
#                     print(R+' [-] No subdomain takeover possible for '+O+sub_domain)

#     else:
#         print(W+' [-] U high dude?')
#         time.sleep(1)

#     print(G+' [+] Subdomain takeover module completed!')
