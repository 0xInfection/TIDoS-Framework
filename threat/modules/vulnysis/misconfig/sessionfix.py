#!/usr/bin/env python
from core.colors import color
def sessionfix(target):
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
# import time
# import requests
# from core.Core.colors import *

# def sessionfix(url):

#     print(R+'\n   =================================')
#     print(R+'    S E S S I O N   F I X A T I O N')
#     print(R+'   =================================\n')
#     print(GR+' [*] Making the request...')
#     coo = raw_input(O+' [#] Got any cookies? [Just Enter if None] :> ')
#     if coo:
#         req = requests.get(url, cookies=coo, verify=True, timeout=7)
#     else:
#         req = requests.get(url, verify=True, timeout=7)
#     if req.cookies:
#         print(G+' [+] Found cookie reflecting in headers...')
#         print(B+' [+] Initial cookie state: '+C, req.cookies, '\n')
#         user = raw_input(O+' [#] Enter authentication username :> '+C)
#         upass = raw_input(O+' [#] Enter password :> '+C)
#         print(GR+' [*] Trying POST request with authentication...')
#         cookie_req = requests.post(url, cookies=req.cookies, auth=(user, upass), timeout=7)
#         print(B+' [+] Authenticated cookie state:'+C, cookie_req.cookies)
#         if req.cookies == cookie_req.cookies:
#             print(G+' [+] Site seems to be vulnerable...')
#             print(G+' [+] Site is vulnerable to session fixation vulnerability!')
#         else:
#             print(O+' [!] Cookie values do not match...')
#             print(R+' [-] Target not vulnerable to session fixation!')
#     else:
#         print(R+' [-] No basic cookie support!')
#         print(R+' [-] Target not vulnerable to session fixation!')
#     print(G+' [+] Session Fixation Module Completed!\n')
