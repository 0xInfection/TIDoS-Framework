#!/usr/bin/env python
from core.colors import color
def openredirect(target):
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
# import time
# import requests
# from core.Core.colors import *
# from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# payloads = []

# def check0x00(web, headers):

#     print(GR+' [*] Configuring payloads with Url...')
#     web000 = web.split('=')[0] + '='
#     for pay in payloads:
#         web0x0 = web000 + pay
#         print(B+'\n [!] Using payload : '+C+pay+' ...')
#         print(GR+' [+] Url : '+C+web0x0+' ...')
#         print(O+' [*] Making the no-verify request...')
#         time.sleep(0.1)
#         req = requests.get(web0x0, headers=headers, allow_redirects=True, timeout=7, verify=False)
#         stat = str(req.status_code)
#         if stat == '302':
#             print(O+' [+] HTTP 302 Response '+GR+'(Found)!\n '+G+' [+] Confirm open-redirection vulnerability at : '+C+web0x0)
#         elif stat == '301':
#             print(O+' [+] HTTP 301 Response! '+GR+'(Moved Permanently)!\n '+G+' [+] Potential open-redirection vulnerability at : '+C+web0x0)
#         elif stat == '307':
#             print(O+' [+] HTTP 307 Response! '+GR+'(Temporary Redirect)!\n '+G+' [+] Potential open-redirection vulnerability at : '+C+web0x0)
#         elif stat == '400':
#             print(R+' [-] HTTP 400 Response '+GR+'(Bad Request)!')
#         elif stat == '403':
#             print(R+' [-] HTTP 403 Response '+GR+'(Forbidden)!')
#         elif stat == '404':
#             print(R+' [-] HTTP 404 Response '+GR+'(Not Found)!')
#         elif stat == '405':
#             print(R+' [-] HTTP 405 Response '+GR+'(Method Not Allowed)!')
#         elif stat == '406':
#             print(R+' [-] HTTP 406 Response '+GR+'(Not Acceptable)!')
#         elif stat == '408':
#             print(R+' [-] HTTP 408 Response '+GR+'(Timeout)!')
#         elif stat == '500':
#             print(O+' [-] HTTP 500 Response '+GR+'(Internal Error)! Server could not handle request!')
#             print(G+' [+] Potential Vulnerability at : '+C+web0x0)
#         elif stat == '502':
#             print(O+' [-] HTTP 502 Response '+GR+'(Internal Error)! Server could not handle request!')
#             print(G+' [+] Potential Vulnerability at : '+C+web0x0)
#         elif stat == '503':
#             print(O+' [-] HTTP 503 Response '+GR+'(Internal Error)! Server could not handle request!')
#             print(G+' [+] Potential Vulnerability at : '+C+web0x0)
#         elif stat == '200':
#             print(R+' [-] HTTP 200 Response '+GR+'(OK)!')
#             print(G+' [+] Redirection confirmation page at : '+O+web0x0)
#         elif stat == '202':
#             print(R+' [-] HTTP 202 Response '+GR+'(Accepted)!')
#             print(G+' [+] Redirection confirmation page at : '+O+web0x0)
#         elif stat == '204':
#             print(R+' [-] HTTP 204 Response '+GR+'(No Content)!')
#             print(G+' [+] Redirection confirmation page at : '+O+web0x0)
#         elif stat == '203':
#             print(R+' [-] HTTP 203 Response '+GR+'(Non-Authoritative Content)!')
#             print(G+' [+] Redirection confirmation page at : '+O+web0x0)
#         elif stat == '429':
#             print(R+' [-] The site has an active rate limiting enabled!')
#             time.sleep(0.7)
#             print(R+' [-] Server blocking requests... Exiting module...')
#             break
#         else:
#             print(R+' [-] Interesting HTTP Response : '+O+stat)

# def getPayloads0x00(fi):
#     try:
#         print(GR+' [*] Importing payloads from '+O+fi+'...')
#         time.sleep(1)
#         with open(fi,'r') as f0:
#             for f in f0:
#                 f = f.strip('\n')
#                 payloads.append(f)
#         print(G+' [+] '+O+str(len(payloads))+G+' Payloads Loaded!')

#     except ImportError:
#         print(R+' [-] Unable to import payloads!')
#         print(R+' [-] File does not exist!')

# def openredirect(web):

#     print(GR+' [*] Loading module...')
#     time.sleep(0.6)
#     print(R+'\n    ===========================================')
#     print(R+'     O P E N   R E D I R E C T   C H E C K E R')
#     print(R+'    ===========================================\n')

#     try:
#         param = raw_input(O+' [#] Scope parameter to test (eg. /redirect.php?site=foo) :> ')
#         if '?' in param and '=' in param:
#             if param.startswith('/'):
#                 m = raw_input(GR+'\n [!] Your path starts with "/".\n [#] Do you mean root directory? (Y/n) :> ')
#                 if m == 'y':
#                     web00 = web + param
#                 elif m == 'n':
#                     web00 = web + param
#                 else:
#                     print(R+' [-] U mad?')
#             else:
#                 web00 = web + '/' + param
#         else:
#             print(R+' [-] Your input does not match a parameter...')
#             param = raw_input(O+' [#] Enter paramter to test :> ')

#         print(GR+' [*] Configuring relative headers...')
#         time.sleep(0.8)
#         gen_headers =    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
#                           'Accept-Language':'en-US;',
#                           'Accept-Encoding': 'gzip, deflate',
#                           'Accept': 'text/html,application/xhtml+xml,application/xml;',
#                           'Connection':'close'}

#         print(O+' [!] Enter path to payload file '+R+'(Default: files/payload-db/openredirect_payloads.lst)')
#         fi = raw_input(O+' [#] Your input (Press Enter if default) :> ')
#         if fi == '':
#             fi = 'files/payload-db/openredirect_payloads.lst'
#             getPayloads0x00(fi)
#         else:
#             if os.path.exists(fi) == True:
#                 print(G+' [+] File found under '+fi)
#                 getPayloads0x00(fi)
#             else:
#                 print(R+' [-] File not found... Using default payload...')
#                 fi = 'files/payload-db/openredirect_payloads.lst'
#                 getPayloads0x00(fi)
#         input_cookie = raw_input("\n [#] Got any cookies? [just enter if none] :> ")
#         if(len(input_cookie) > 0):
#             gen_headers['Cookie'] = input_cookie
#         check0x00(web00, gen_headers)

#     except KeyboardInterrupt:
#         print(R+' [-] User Interruption Detected!')
#         pass
