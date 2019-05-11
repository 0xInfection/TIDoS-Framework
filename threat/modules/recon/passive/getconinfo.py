#!/usr/bin/env python
from core.colors import color
def getconinfo(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # coding: utf-8

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author : @_tID
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import requests
# import time
# from core.Core.colors import *

# def getconinfo(domain):

#     print(R+'\n    =======================================')
#     print(R+'     D O M A I N   C O N T A C T   I N F O')
#     print(R+'    =======================================\n')
#     time.sleep(0.6)
#     print(GR+' [*] Importing API Key...')
#     try:
#         from files.API_KEYS import FULLCONTACT_API_KEY
#     except (IOError, ImportError):
#         print(R+' [-] Error while importing key...')

#     try:

#         if FULLCONTACT_API_KEY != '':
#             print(G+' [+] Found API Key : '+O+FULLCONTACT_API_KEY)
#             base_url = 'https://api.fullcontact.com/v2/company/lookup.json'
#             print(GR+' [*] Looking up info...')
#             time.sleep(0.7)
#             payload = {'domain':domain, 'apiKey':FULLCONTACT_API_KEY}
#             resp = requests.get(base_url, params=payload)

#             if resp.status_code == 200:

#                 print(G+' [+] Found domain info!')
#                 w = resp.text.encode('ascii', 'ignore')
#                 quest = w.splitlines()
#                 print(O+' [!] Parsing info...\n')
#                 print(R+' [+] REPORT :-\n')
#                 time.sleep(1)
#                 for q in quest:
#                     q = q.replace('"','')
#                     if ':' in q and '[' not in q and '{' not in q:
#                         q1 = q.split(':',1)[0].strip().title()
#                         q2 = q.split(':',1)[1].strip().replace(',','')
#                         if q1.lower() == 'typeid' or q1.lower() == 'number' or q1.lower() == 'type':
#                             print(C+'\n   [+] '+q1+' : '+GR+q2)
#                         else:
#                             print(C+'   [+] '+q1+' : '+GR+q2)
#                         time.sleep(0.01)

#                     elif ('{' or '[' in q) and (':' in q):
#                         w1 = q.split(':',1)[0].strip().upper()
#                         w2 = q.split(':',1)[1].strip()
#                         if w1.lower() == 'keywords':
#                             print(C+'\n   [+] '+w1+' : '+GR+w2)
#                         else:
#                             print(O+'\n [+] '+w1+' :-'+'\n')

#             else:
#                 print(R+' [-] Did not find any info about domain '+O+domain)
#                 print(R+' [+] Try with another one...')

#         else:
#             print(R+' [-] FULL CONTACT API TOKEN not set!')
#             print(R+' [-] This module cannot be used!')

#     except Exception as e:
#         print(R+' [-] Encountered Exception : '+str(e))

#     print(G+'\n [+] Public Contact Info Module Completed!\n')
