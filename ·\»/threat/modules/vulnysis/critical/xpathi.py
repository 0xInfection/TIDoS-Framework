#!/usr/bin/env python
from core.colors import color
def xpathi(target):
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
# import requests
# import time
# sys.path.append('files/signature-db/')
# from core.Core.colors import *
# from xpatherror_signatures import xpath_errors
# from random import choice
# from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# payloads = []
# hunt = 0x00

# def check0x00(web0x00, pay, gen_headers):

#     try:
#         print(GR+' [*] Making the request...')
#         rq = requests.get(web0x00, headers=gen_headers, allow_redirects=False, verify=False)
#         c = rq.content
#         print(O+' [!] Analysing responses...')
#         time.sleep(0.7)
#         for sign in xpath_errors:
#             if re.search(sign, c, re.I):
#                 hunt = 0x01
#                 print(G+' [+] Potential XPATH Code Injection Flaw discovered!')
#                 print(GR+' [*] Injecting payloads...')
#                 time.sleep(0.4)
#                 print(B+' [+] Vulnerable Link : '+C+web0x00)
#                 print(B+' [+] Payload : '+C+pay)
#                 print(O+' [+] Response : \033[0m\n')
#                 print(c)
#             else:
#                 print(R+' [-] Payload '+O+pay+R+' unsuccessful...')
#                 print(R+' [-] No successful code injection at : '+O+web0x00)

#     except Exception as e:
#         print(R+' [-] Exception encountered!')
#         print(R+' [-] Error : '+str(e))

# def getFile0x00():

#     try:
#         print(O+' [#] Enter path to file (default: files/payload-db/xpath_payloads.lst)...')
#         w = raw_input(O+' [#] Your input (Press Enter if default) :> '+C)
#         if w == '':
#             fi = 'files/payload-db/xpath_payloads.lst'
#             print(GR+' [*] Importing payloads...')
#             with open(fi,'r') as q0:
#                 for q in q0:
#                     q = q.strip('\n')
#                     payloads.append(q)
#         else:
#             fi = w
#             if os.path.exists(fi) == True:
#                 print(G+' [+] File '+fi+' found...')
#                 print(GR+' [*] Importing payloads...')
#                 with open(fi,'r') as q0:
#                     for q in q0:
#                         q = q.strip('\n')
#                         payloads.append(q)
#     except IOError:
#         print(R+' [-] File path '+O+fi+R+' not found!')

# def xpathi(web):

#     print(GR+' [*] Loading module...')
#     time.sleep(0.5)
#     print(R+'\n    ===============================')
#     print(R+'     X P A T H   I N J E C T I O N')
#     print(R+'    ===============================\n')

#     gen_headers =    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
#                       'Accept-Language':'en-US;',
#                       'Accept-Encoding': 'gzip, deflate',
#                       'Accept': 'text/php,application/xhtml+xml,application/xml;',
#                       'Connection':'close'}

#     print(GR+' [*] Initiating '+R+'Parameter Based Check...')
#     param = raw_input(O+' [#] Parameter Path (eg. /vuln/page.php?q=input) :> ')
#     if param.startswith('/') == False:
#         param = '/' + param
#     print(GR+' [*] Importing filepath...')
#     getFile0x00()
#     web0 = web + param
#     web00 = web0.split('=')[0] + '='
#     try:
#         for pay in payloads:
#             print(GR+'\n [*] Setting parameters...')
#             web0x00 = web00 + pay
#             print(C+' [+] Using payload : '+B+str(pay))
#             print(B+' [+] Using !nfected Url : '+GR+str(web0x00))
#             check0x00(web0x00, pay, gen_headers)

#     except Exception as e:
#         print(R+' [-] Unexpected Exception Encountered!')
#         print(R+' [-] Exception : '+str(e))

#     if hunt == 0x00:
#         print(R+' [-] No vulnerabilities found!')

#     print(G+'\n [+] XPATHi Module Completed!\n')
