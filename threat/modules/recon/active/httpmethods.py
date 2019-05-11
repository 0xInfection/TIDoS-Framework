#!/usr/bin/env python
from core.colors import color
def httpmethods(target):
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
# import httplib
# import time
# from core.Core.colors import *

# def httpmethods(web):

#     try:
#         print(R+'\n    =========================')
#         print(R+'     H T T P   M E T H O D S ')
#         print(R+'    =========================\n')

#         print(GR+' [*] Parsing Url...')
#         time.sleep(0.7)
#         web = web.replace('https://','')
#         web = web.replace('http://','')
#         print(O+' [!] Making the connection...')
#         conn = httplib.HTTPConnection(web)
#         conn.request('OPTIONS','/')
#         response = conn.getresponse()
#         q = str(response.getheader('allow'))
#         if 'None' not in q:
#             print(G+' [+] The following HTTP methods are allowed...')
#             methods = q.split(',')
#             for method in methods:
#                 print(O+'     '+method)
#         else:
#             print(R+' [-] HTTP Method Options Request Unsuccessful...')

#     except Exception as e:
#         print(R+' [-] Exception Encountered!')
#         print(R+' [-] Error : '+str(e))
