#!/usr/bin/env python
from core.colors import color
def xss(target):
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
# import os
# import re
# import sys
# import time
# import requests
# from core.Core.colors import *
# import sre_constants
# from time import sleep

# global pay, poly
# poly = []
# pay = []

# def auto0x00(web):

#     def xsscookie0x00(web):

#         print(R+'\n    =======================')
#         print(R+'     X S S  (Cookie Based)')
#         print(R+'    =======================\n')

#         sleep(0.5)
#         session = requests.Session()
#         req = session.get(web)
#         if session.cookies:
#             print(G+' [+] This website supports session cookies...')
#             for j in pay:
#                 i = r'%s' % j
#                 print(B+" [*] Trying Payload : "+C+ i)
#                 time.sleep(0.7)
#                 for cookie in session.cookies:
#                     cookie.value += i
#                     print(O+' [+] Using '+R+'!nfected'+O+' cookie : '+GR+cookie.value)
#                     r = session.get(web)
#                     if i in r.text:
#                         poc = C+" [+] PoC : " +O+ cookie.name + " : " +GR+ cookie.value
#                         print(G+" [+] Cookie Based XSS Detected! ")
#                         print(poc)
#                         print(P+' [+] Code : '+W+str(r.text)+'\n')
#         else:
#             print(R+' [-] No support for cookies...')
#             time.sleep(0.5)
#             print(R+' [-] Cookie based injection not possible...')

#     def xssuser0x00(web):

#         print(R+'\n    ===========================')
#         print(R+'     X S S  (User-Agent Based)')
#         print(R+'    ===========================\n')

#         for j in pay:
#             i = r'%s' % j
#             print(B+' [*] Using payload : '+C+i)
#             time.sleep(0.7)
#             user_agent = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux ' +
#                           'x86_64; rv:39.0)'}
#             user_agent['User-agent'] += i
#             req = requests.get(web, headers=user_agent)
#             print(O+' [*] Using '+R+'!nfected'+O+' UA : '+GR+user_agent['User-agent'])
#             flag = u' '.join(req.text).encode('utf-8').strip()
#             if i in req.content:
#                 print(G+'\n [!] Cross Site Scripting (User-Agent Based) Detected!')
#                 print(R+' [!] User-Agent : '+O+user_agent['User-agent'])
#                 print(W+color.BOLD+' [+] Code: '+W)
#                 print(str(req.content)+'\n')

#     def xssref0x00(web):

#         print(R+'\n    ===========================')
#         print(R+'     X S S  (Referrer Based)')
#         print(R+'    ===========================\n')

#         for j in pay:
#             i = r'%s' % j
#             print(B+' [*] Using payload : '+C+i)
#             time.sleep(0.7)
#             user_agent = {'Referer': 'http://' + 'xssing.pwn'}
#             user_agent['Referer'] += i
#             req = requests.get(web, headers=user_agent)
#             print(O+' [*] Using '+R+'!nfected'+O+' UA : '+GR+user_agent['Referer'])
#             flag = u' '.join(req.text).encode('utf-8').strip()
#             if i in req.content:
#                 print(G+'\n [!] Cross Site Scripting (User-Agent Based) Detected!')
#                 print(R+' [!] User-Agent : '+O+user_agent['Referer'])
#                 print(W+color.BOLD+' [+] Code: '+W)
#                 print(str(req.content)+'\n')

#     print(P+' [!] Enter an option :\n')
#     print(B+'   [1] '+C+'Cookie Value Based XSS')
#     print(B+'   [2] '+C+'User-Agent Value Based XSS')
#     print(B+'   [3] '+C+'Referrer Value Based XSS\n')
#     q = raw_input(O+' [#] TID :> ')
#     if q == '3':
#         print(GR+' [*] Launching Referrer Based Module...')
#         xssref0x00(web)
#     elif q == '2':
#         print(GR+' [*] Launching User-Agent Based Module...')
#         xssuser0x00(web)
#     elif q == '1':
#         print(GR+' [*] Launching Cookie-Based Module...')
#         xsscookie0x00(web)

# def xsspoly0x00(li):

#     yay = 0x00
#     print(R+'\n    ==========================')
#     print(R+'     X S S  (Polyglot Fuzzer)')
#     print(R+'    ==========================\n')
#     try:
#         with open('files/payload-db/polyglot_payloads.lst','r') as payloads:
#             for payload in payloads:
#                 payload = payload.replace('\n','')
#                 poy = r'%s' % (payload)
#                 poly.append(poy)
#         print(G+' [+] '+O+str(len(pay))+G+' polyglots loaded!')
#         sleep(0.7)
#         if '?' in str(li) and '=' in str(li):
#             for p in poly:
#                 bugged = li + str(p)
#                 print(B+"\n [*] Trying : "+C+bugged)
#                 time.sleep(0.7)
#                 print(GR+' [*] Making the request...')
#                 resp = requests.get(bugged)
#                 print(O+' [!] Matching payload signatures...')
#                 try:
#                     if p in resp.text:
#                         yay = 0x01
#                         print('\n'+G+' [+] Vulnerable link detected : ' + bugged)
#                         print(GR+' [*] Injecting payloads...')
#                         print(B+' [!] PoC : ' + str(bugged))
#                         print(R+" [!] Payload : " + O + p + '\033[0m')
#                         print("\033[1m [!] Code Snippet :\n \033[0m" + str(response) + '\n')
#                     else:
#                         print(R+' [-] No successful payload reflection...')
#                         print(R+' [-] Payload '+O+p+R+' unsuccessful...')
#                 except sre_constants.error:
#                     pass

#             if yay != 0x01:
#                 print(R+' [-] No successful polyglots found!')

#     except KeyboardInterrupt:
#         print(R+' [+] Polyglot Payloads File does not exist!')

# def manual0x00(web):

#     yay = 0x00
#     print(R+'\n    ======================')
#     print(R+'     X S S  (Manual Mode)')
#     print(R+'    ======================\n')
#     bug = raw_input(O+' [#] Injectable Endpoint'+R+' (eg. /xss/search.php?q=drake)'+O+' :> ')
#     bugs = web + bug.split('=')[0] + '='
#     print(O+' [!] Using Url : '+GR+bugs)
#     if '?' in str(bugs) and '=' in str(bugs):
#         for p in pay:
#             bugged = bugs + str(p)
#             print(B+"\n [*] Trying : "+C+bugged)
#             time.sleep(0.2)
#             print(GR+' [*] Making the request...')
#             response = requests.get(bugged)
#             print(O+' [!] Matching payload signatures...')
#             try:
#                 if p in response.text:
#                     yay = 0x01
#                     print(G+' [+] Vulnerable link detected : ' + bugged)
#                     print(GR+' [*] Injecting payloads...')
#                     print(B+' [!] PoC : ' + str(bugged))
#                     print(R+" [!] Payload : " + O + p + '\033[0m')
#                     print("\033[1m [!] Code Snippet :\n \033[0m" + str(response) + '\n')
#                 else:
#                     print(R+' [-] No successful payload reflection...')
#                     print(R+' [-] Payload '+O+p+R+' unsuccessful...')

#             except sre_constants.error:
#                 pass
#         if yay != 0x01:
#             print(P+'\n [-] No successful payloads found!')
#             x = raw_input(O+' [#] Test Polyglots? (Y/n) :> ')
#             if x == 'Y' or x == 'y':
#                 print(GR+' [*] Proceeding fuzzing with polyglots...')
#                 xsspoly0x00(bugs)
#             elif x == 'n' or x == 'N':
#                 print(C+' [+] Okay!')
#             else:
#                 print(GR+' [-] U high dude?')

#     else:
#         print(R+' [-] Enter an URL with scope parameter...')
#         manual0x00(web)

# def xss(web):

#     while True:
#         print(GR+' [*] Loading module XSS...')
#         sleep(0.6)
#         if web.endswith('/'):
#             web = web[:-1]
#         print(R+'\n    =========================================')
#         print(R+'     C R O S S   S I T E   S C R I P T I N G')
#         print(R+'    =========================================\n')
#         print(GR+' [*] Importing payloads...')
#         sleep(0.8)
#         try:
#             with open('files/payload-db/xss_payloads.lst','r') as payloads:
#                 for payload in payloads:
#                     payload = payload.replace('\n','')
#                     pi = r'%s' % (payload)  # Converting to a raw string
#                     pay.append(pi)
#             print(G+' [+] '+O+str(len(pay))+G+' payloads loaded!')
#             sleep(0.7)
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

#     print(G+' [+] XSS Module Completed!\n')

