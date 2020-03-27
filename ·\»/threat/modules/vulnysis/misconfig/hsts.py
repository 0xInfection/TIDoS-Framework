#!/usr/bin/env python
from core.colors import color
def hsts(target):
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
# import sys
# from core.Core.colors import *

# def check0x00(headers):
#     flag = False
#     for head in headers:
#         if 'Strict-Transport-Security'.lower() in head.lower():
#             print(O+' [!] Reflection in response headers found...')
#             flag = True
#     if flag:
#         print(G+' [+] Seems like the website uses strong HSTS...')
#         time.sleep(0.6)
#         print(G+' [+] HSTS Presence Confirmed!')
#     else:
#         print(GR+' [!] HTTP Strict Transport Security Header not found in response headers!')
#         print(O+' [-] Websites uses complete SSL throughout website.')
#         print(R+' [-] However, it does not seem to use HSTS.\n')

# def getHeaders0x00(web):
#     print(O+' [*] Configuring headers...')
#     time.sleep(0.5)
#     gen_headers =    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
#                       'Accept-Language':'en-US;',
#                       'Accept-Encoding': 'gzip, deflate',
#                       'Accept': 'text/html,application/xhtml+xml,application/xml;',
#                       'Connection':'close'}
#     cook = raw_input(C+" [*] Got any cookies? [just Enter if none] :> ")
#     if cook:
#         gen_headers['Cookie'] = cook
#     print(GR+' [*] Making the request...')
#     time.sleep(0.6)
#     req = requests.get(web, headers=gen_headers, timeout=5, verify=True)
#     h = req.headers
#     return h

# def hsts(web):
#     print(GR+' [*] Loading module...')
#     time.sleep(0.5)
#     print(R+'\n    ================================')
#     print(R+'     HTTP STRICT TRANSPORT SECURITY')
#     print(R+'    ================================\n')
#     if 'https' in web:
#         check0x00(getHeaders0x00(web))
#     else:
#         print(R+' [-] No SSL/TLS detected...')
#         m = raw_input(O+' [#] Force SSL/TLS (y/N) :> ')
#         if m == 'y' or m == 'Y':
#             print(GR+' [*] Using revamped SSL...')
#             o = 'https://' + web.replace('http://','')
#             check0x00(getHeaders0x00(web))
#         elif m == 'n' or m == 'N':
#             print(GR+' [-] Skipping module...')

