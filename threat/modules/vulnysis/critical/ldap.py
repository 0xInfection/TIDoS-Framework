#!/usr/bin/env python
from core.colors import color
def ldap(target):
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
# import sys
# import time
# import requests
# sys.path.append('files/signature-db/')
# from core.Core.colors import *
# from ldaperror_signatures import ldap_errors
# from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# def getFile0x00(fi):

#     global payloads
#     payloads = []
#     print(GR+' [*] Importing payloads...')
#     time.sleep(0.7)
#     with open(fi,'r') as payl:
#         for pay in payl:
#             c = pay.replace('\n','')
#             payloads.append(c)
#     print(G+' [+] Loaded '+O+str(len(payloads))+G+' payloads...')

# def check0x00(web000, headers):

#     print(GR+' [*] Starting enumeration...')
#     time.sleep(0.7)
#     for payload in payloads:
#         gotcha = False
#         print(B+'\n [+] Using Payload : '+C+payload)
#         web0x00 = web000 + payload
#         print(O+' [+] Url : '+C+web0x00)
#         print(GR+' [*] Making the request...')
#         try:
#             req = requests.get(web0x00, headers=headers, allow_redirects=False, timeout=7, verify=False).text
#             print(O+' [!] Searching through error database...')
#             for err in ldap_errors:
#                 if err.lower() in req.lower():
#                     print(G+' [+] Possible LDAP Injection Found : '+O+web0x00)
#                     gotcha=True
#                     print(O+' [+] Response : ')
#                     print(P+req)
#                 else:
#                     pass

#             if gotcha == False:
#                 print(R+' [-] No error reflection found in response!')
#                 time.sleep(0.4)
#                 print(R+' [-] Payload '+O+payload+R+' not working!')
#                 pass

#         except Exception as e:
#             print(R+' [-] Query Exception : '+str(e))

# def ldap(web):

#     print(GR+' [*] Loading module...')
#     time.sleep(0.5)
#     print(R+'\n     =============================')
#     print(R+'      L D A P   I N J E C T I O N')
#     print(R+'     =============================\n')
#     try:
#         web0 = raw_input(O+' [#] Parameter path to test (eg. /lmao.php?foo=bar) :> ')
#         if "?" in web0 and '=' in web0:
#             if web0.startswith('/'):
#                 m = raw_input(GR+'\n [!] Your path starts with "/".\n [#] Do you mean root directory? (Y/n) :> ')
#                 if m.lower() == 'y':
#                     web00 = web + web0
#                 elif m.lower() == 'n':
#                     web00 = web + web0
#                 else:
#                     print(R+' [-] U mad?')
#             else:
#                 web00 = web + '/' + web0
#         print(B+' [+] Parameterised Url : '+C+web00)

#         input_cookie = raw_input("\n [*] Enter cookies if needed (Enter if none) :> ")
#         print(GR+' [*] Setting headers...')
#         time.sleep(0.6)
#         gen_headers =    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
#                           'Accept-Language':'en-US;',
#                           'Accept-Encoding': 'gzip, deflate',
#                           'Accept': 'text/html,application/xhtml+xml,application/xml;',
#                           'Connection':'close'}

#         if(len(input_cookie) > 0):
#             gen_headers['Cookie'] = input_cookie
#         print(O+' [#] Enter the payloads file '+R+'(Default: files/payload-db/ldap_payloads.lst)...')
#         fi = raw_input(O+' [#] Your input (Press Enter for default) :> ')
#         if fi == '':
#             fi = 'files/payload-db/ldap_payloads.lst'
#             getFile0x00(fi)
#         else:
#             if os.path.exists(fi) == True:
#                 print(G+' [+] File under '+fi+' found!')
#                 getFile0x00(fi)
#             else:
#                 print(R+' [-] Invalid input... Using default...')
#                 fi = 'files/payload-db/ldap_payloads.lst'
#                 getFile0x00(fi)
#         print(O+' [!] Parsing url...')
#         time.sleep(0.7)
#         web000 = web00.split('=')[0] + '='
#         check0x00(web000, gen_headers)

#     except KeyboardInterrupt:
#         print(R+' [-] Aborting module...')
#         pass
#     except Exception as e:
#         print(R+' [-] Exception : '+str(e))
#     print(G+'\n [+] LDAP Injection module completed!\n')
