#!/usr/bin/env python
from core.colors import color
def googlegroups(target):
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
# import json
# import time
# import requests
# import re
# from core.Core.colors import *

# def getemails0x00(domain):

#     global flag
#     flag = False
#     page_counter = 0
#     try:
#         while page_counter < 100 :
#             print(GR+' [*] Setting parameters...')
#             time.sleep(0.6)
#             results = 'http://www.google.com/search?q='+str(domain)+'&hl=en&lr=&ie=UTF-8&start=' + repr(page_counter) + '&sa=N'
#             print(O+' [!] Making the request...')
#             response = requests.get(results)
#             print(GR+' [*] Extracting reponse...')
#             text = response.text
#             emails = re.findall('([\w\.\-]+@'+domain+')',tagparse(text))
#             for email in emails:
#                 print(G+' [+] Received e-mail : '+O+email)
#                 flag = True
#             page_counter = page_counter + 10
#     except IOError:
#         print(R+" [-] Error connecting to Google Groups...")

#     try:
#         while page_counter < 100 :
#             print(GR+' [*] Setting parameters...')
#             time.sleep(0.6)
#             results = 'http://groups.google.com/groups?q='+str(domain)+'&hl=en&lr=&ie=UTF-8&start=' + repr(page_counter) + '&sa=N'
#             print(O+' [!] Making the request...')
#             response = requests.get(results)
#             print(GR+' [*] Extracting reponse...')
#             text = response.text
#             emails = re.findall('([\w\.\-]+@'+domain+')',tagparse(text))
#             for email in emails:
#                 print(G+' [+] Received e-mail : '+O+email)
#                 flag = True
#             page_counter = page_counter + 10
#     except IOError:
#         print(R+" [-] Error connecting to Google Groups...")

# def tagparse(text):
#     print(GR+' [*] Parsing raw data...')
#     time.sleep(0.5)
#     finished = 0
#     while not finished:
#         finished = 1
#         start = text.find("<")
#         if start >= 0:
#             stop = text[start:].find(">")
#             if stop >= 0:
#                 text = text[:start] + text[start+stop+1:]
#                 finished = 0
#     return text

# def googlegroups(web):

#     print(GR+' [*] Loading module...')
#     time.sleep(0.7)
#     print(R+'\n    ===========================')
#     print(R+'     G O O G L E   G R O U P S')
#     print(R+'    ===========================\n')

#     print(O+' [!] Initiating enumeration via Google Web...')
#     time.sleep(0.7)
#     print(O+' [!] Parsing url...')
#     web = web.replace('https://','')
#     web = web.replace('http://','')
#     getemails0x00(web)
#     if flag == False:
#         print(R+' [-] No results found via enumeration on Google Groups...')
#     print(G+' [+] Done!')
