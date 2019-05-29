#!/usr/bin/env python
from core.colors import color
def errorsqlsearch(target):
    print('This module is not yet available.')
    pass
# # coding: utf-8
# #!/usr/bin/env python

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author: @_tID
# #This script is a part of TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import mechanize
# from re import search, sub
# import cookielib
# import requests
# import time
# import urllib2
# import re
# import os
# import sys
# from re import *
# from urllib import *
# from core.Core.colors import *
# from time import sleep

# br = mechanize.Browser()

# cj = cookielib.LWPCookieJar()
# br.set_cookiejar(cj)

# params = []

# br.set_handle_equiv(True)
# br.set_handle_redirect(True)
# br.set_handle_referer(True)
# br.set_handle_robots(False)

# class UserAgent(FancyURLopener):
#     version = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'

# useragent = UserAgent()
# br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
# br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# ctr=0
# path_list = []
# payloads = []

# def errorsqlsearch(web):

#     os.system('clear')
#     print(R+'\n    ======================================')
#     print(R+'     S Q L i   H U N T E R (Auto Awesome)')
#     print(R+'    ======================================\n')
#     print(R+'           [E R R O R   B A S E D] \n')
#     with open('files/payload-db/errorsql_payloads.lst','r') as pay:
#         for payload in pay:
#             rem = payload.replace('\n','')
#             payloads.append(rem)
#     web0 = web.replace('https://','')
#     web0 = web.replace('http://','')
#     try:
#         with open('tmp/logs/'+web0+'-logs/'+web0+'-links.lst','r') as ro:
#             for r in ro:
#                 r = r.replace('\n','')
#                 path_list.append(r)
#     except IOError:
#         print(R+' [-] Path file not found!')
#         br.open(web)
#         for o in br.links():
#             path_list.append(o.base_url+'/'+o.url)
#         print(path_list)
#     for bugs in path_list:
#         ctr = 0
#         print(B+' [*] Testing '+C+str(bugs))
#         if '?' in str(bugs) and '=' in str(bugs):
#             getrq = requests.get(bugs, verify=False)
#             for p in payloads:
#                 bugs = bugs + str(p)
#                 print(B+" [*] Trying : "+C+ bugs)
#                 time.sleep(0.7)
#                 response = requests.get(bugs, verify=False)
#                 if 'error' in response.text or 'mysql' in response.text.lower():
#                     print('\n'+G+' [+] Vulnerable link detected: ' + web)
#                     print(R+' [*] Injecting Error SQLi payloads...')
#                     print(B+' [!] PoC : ' + str(bugs))
#                     print(R+" [!] Payload : " + O + p + '\033[0m')
#                     #print("\033[1m [!] Code Snippet : \n\033[0m" + response.content + '\n')
#                     ctr+= 1
#                     break
#         else:
#             print(GR+' [-] Link without parameter : '+B+'' + str(bugs))
#             time.sleep(0.2)
