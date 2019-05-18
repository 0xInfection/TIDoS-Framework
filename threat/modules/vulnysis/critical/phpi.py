#!/usr/bin/env python
from core.colors import color
def phpi(target):
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
# import sys
# import requests
# import time
# from re import search
# from core.Core.colors import *
# from random import choice
# from string import uppercase, lowercase
# from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# payloads = []

# def genRandStr0x00(n):
#     return ''.join([choice(uppercase+lowercase) for o in xrange(0,int(n))]) # fetch random string

# def check0x00(web0x00, pay, gen_headers):

#     try:
#         hunt = 0x00
#         print(GR+' [*] Making the request...')
#         rq = requests.get(web0x00, headers=gen_headers, allow_redirects=False, verify=False)
#         c = rq.content
#         print(O+' [!] Analysing responses...')
#         time.sleep(0.7)
#         if search(r"root\:\/bin\/bash|"+pay,c): # regex for vuln
#             hunt = 0x01
#             print(G+' [+] Potential PHP Code Injection Flaw discovered!')
#             print(GR+' [*] Injecting payloads...')
#             time.sleep(0.4)
#             print(B+' [+] Vulnerable Link : '+C+web0x00)
#             print(B+' [+] Payload : '+C+pay)
#             print(O+' [+] Response : \033[0m\n')
#             print(c)
#         else:
#             print(R+' [-] Payload '+O+pay+R+' unsuccessful...')
#             print(R+' [-] No successful code injection at : '+O+web0x00)

#     except Exception as e:
#         print(R+' [-] Exception encountered!')
#         print(R+' [-] Error : '+str(e))

# def getFile0x00():

#     try:
#         print(GR+' [*] Importing filepath...')
#         print(O+' [#] Enter path to file (default: files/payload-db/php_payloads.lst)...')
#         w = raw_input(O+' [#] Your input (Press Enter if default) :> '+C)
#         if w == '':
#             fi = 'files/payload-db/php_payloads.lst'
#             print(GR+' [*] Importing payloads...')
#             with open(fi,'r') as q0:
#                 for q in q0:
#                     q = q.strip('\n')
#                     m = q.replace('drake', genRandStr0x00(30)) # replace with a random string
#                     payloads.append(m)
#         else:
#             fi = w
#             if os.path.exists(fi) == True:
#                 print(G+' [+] File '+fi+' found...')
#                 print(GR+' [*] Importing payloads...')
#                 with open(fi,'r') as q0:
#                     for q in q0:
#                         q = q.strip('\n')
#                         m = q.replace('drake', genRandStr0x00(30))
#                         payloads.append(m)

#     except IOError:
#         print(R+' [-] File path '+O+fi+R+' not found!')

# def phpi(web):

#     print(GR+' [*] Loading module...')
#     time.sleep(0.5)
#     print(R+'\n    =====================================')
#     print(R+'     P H P   C O D E   I N J E C T I O N')
#     print(R+'    =====================================\n')

#     gen_headers =    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
#                       'Accept-Language':'en-US;',
#                       'Accept-Encoding': 'gzip, deflate',
#                       'Accept': 'text/php, application/xhtml+xml, application/xml;', # important -> text/php
#                       'Connection':'close'}

#     print(GR+' [*] Initiating '+R+'Parameter Based Check...')
#     param = raw_input(O+' [#] Scope parameter (eg. /vuln/page.php?q=lmao) :> ')
#     if param.startswith('/') == False:
#         param = '/' + param
#     getFile0x00() # get the file with payloads
#     web0 = web + param
#     web00 = web0.split('=')[0] + '=' # picking up url till parameter
#     try:
#         for pay in payloads:
#             print(GR+'\n [*] Setting parameters...')
#             web0x00 = web00 + pay
#             print(C+' [+] Using payload : '+B+str(pay))
#             print(B+' [+] Using !nfected Url : '+GR+str(web0x00)) # display whats going on
#             check0x00(web0x00, pay, gen_headers) # check the outupt of the fuzz

#     except Exception as e: # if error
#         print(R+' [-] Unexpected Exception Encountered!')
#         print(R+' [-] Exception : '+str(e))

#     print(G+'\n [+] PHPi Module Completed!')
