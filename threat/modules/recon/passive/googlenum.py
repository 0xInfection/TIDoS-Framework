#!/usr/bin/env python
from core.colors import color
def googlenum(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author : @_tID
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import requests
# import time
# import json
# import urllib2
# from core.Core.colors import *

# def googlenum(web):

#     print(R+'\n    =================================')
#     print(R+'     G O O G L E   G A T H E R I N G ')
#     print(R+'    =================================\n')
#     try:
#         print(GR+' [*] Importing API Token...')
#         time.sleep(0.7)
#         from files.API_KEYS import GOOGLE_API_TOKEN
#         if GOOGLE_API_TOKEN != '':
#             maxr = '50'
#             print(GR+' [*] Fetching maximum 50 results...')
#             print(O+' [!] Parsing website address...')
#             time.sleep(0.6)
#             web = web.replace('http://','')
#             web = web.replace('https://','')
#             print(GR+' [*] Making the request...')
#             try:
#                 resp = requests.get('https://www.googleapis.com/plus/v1/people?query='+web+'&key='
#                         +GOOGLE_API_TOKEN+'&maxResults='+maxr).text
#             except requests.exceptions:
#                 print(R+' [-] Access Forbidden (403)...')
#             print(O+' [!] Parsing raw-data...')
#             time.sleep(1)
#             r = json.loads(resp)
#             ctr = 1
#             print(GR+' [*] Fetching data...')
#             if "items" in r:
#                 for p in r["items"]:
#                     ctr+=1
#                     time.sleep(0.8)
#                     print(G+'\n [+] Info about Profile '+O+str(ctr)+' ...')
#                     if 'kind' in p:
#                         print(B+' [+] Kind : '+C+p['kind'])
#                     time.sleep(0.05)
#                     if 'etag' in p:
#                         print(B+' [+] E-Tag : '+C+p['etag'])
#                     time.sleep(0.05)
#                     if 'objectType' in p:
#                         print(B+' [+] Object Type : '+C+p['objectType'])
#                     time.sleep(0.05)
#                     if 'id' in p:
#                         print(B+' [+] ID : '+C+p['id'])
#                     time.sleep(0.05)
#                     if 'displayName' in p:
#                         print(B+' [+] Display Name : '+C+p['displayName'])
#                     time.sleep(0.05)
#                     if 'url' in p:
#                         print(B+' [+] Link : '+C+p['url'])
#                     time.sleep(0.05)

#             print(O+' [+] Google Enumeration Completed!')

#         else:
#             print(R+' [-] Google API Token Key not set... This modules cannot be used!')

#     except IOError:
#         print(R+' [-] Google API Token Key not set... This modules cannot be used!')
