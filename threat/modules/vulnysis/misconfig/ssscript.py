#!/usr/bin/env python
from core.colors import color
def ssscript(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # coding:  utf-8

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author: 0xInfection (@_tID)
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import os
# import requests
# import time
# import sys
# import subprocess
# sys.path.append('files/')
# from core.Core.colors import *
# from subdom0x00 import *

# def ssscript(web):

#     vuln = []
#     novuln = []
#     web = web.replace('https://','')
#     web = web.replace('http://','')
#     print(R+'\n   =======================================')
#     print(R+'    S A M E - S I T E   S C R I P T I N G')
#     print(R+'   =======================================\n')
#     time.sleep(0.5)
#     try:
#         if os.path.exists('files/'+web+'-subdomains.lst') == True:
#             pass
#         else:
#             print(O+' [*] Gathering subdomains...')
#             print(GR+' [*] Initializing subdomain gathering...')
#             subdom0x00(web)
#     except:
#         print(R+' [-] Exception occured!')

#     os.system('mv '+web+'-subdomains.lst tmp/')
#     print(R+'\n    =========================')
#     print(R+'     S - S - S   T E S T E R')
#     print(R+'    =========================\n')
#     try:
#         with open('tmp/'+web+'-subdomains.lst','r') as dom:
#             for m in dom:
#                 m = m.replace('\n','')
#                 print(C+' [*] Running tests on '+GR+m+C+' for Same-Site Scripting...')
#                 time.sleep(1.5)
#                 try:
#                     mp = socket.gethostbyname(m)
#                     if '127.0.0.1' in mp or '0.0.0.0' in mp:
#                         time.sleep(0.7)
#                         print(G+' [+] This website is vulnerable to Same Site Scripting!')
#                         vuln.append(web)
#                     else:
#                         time.sleep(0.7)
#                         print(R+' [-] '+O+m+R+' is immune to Same-Site Scripting!')
#                         novuln.append(web)

#                 except socket.gaierror:
#                     time.sleep(0.7)
#                     pass
#     except Exception as e:
#         print(R+' [-] Error occured while processing module')
#         print(R+' [-] Error : '+str(e))
#         pass
