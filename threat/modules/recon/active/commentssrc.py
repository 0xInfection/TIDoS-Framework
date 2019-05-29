#!/usr/bin/env python
from core.colors import color
def commentssrc(target):
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
# import lxml
# import os
# import requests
# import re
# import time
# from bs4 import BeautifulSoup
# import sys
# from core.Core.colors import *
# found = 0x00
# urls = []
# links = []

# def commentssrc(web):

#     print(R+'\n    =================================')
#     print(R+'     C O M M E N T S   S C R A P E R')
#     print(R+'    =================================')
#     print(O+' [It is recommended to run ScanEnum/Crawlers')
#     print(O+'       before running this module]\n')
#     print(GR+' [*] Importing links...')
#     po = web.split('//')[1]
#     p = 'tmp/logs/'+po+'-logs/'+po+'-links.lst'
#     links = [web]

#     for w in links:
#         print(GR+' [*] Making the request...')
#         req = requests.get(w).content
#         print(O+' [!] Setting parse parameters...')
#         comments = re.findall('<!--(.*)-->',req)
#         print(G+" [+] Searching for comments on page: "+O+web+'\n')
#         for comment in comments:
#             print(C+'   '+comment)
#             time.sleep(0.03)
#             found = 0x01

#     soup = BeautifulSoup(req,'lxml')
#     for line in soup.find_all('a'):
#         newline = line.get('href')
#         try:
#             if newline[:4] == "http":
#                 if web in newline:
#                     urls.append(str(newline))
#             elif newline[:1] == "/":
#                 combline = web+newline
#                 urls.append(str(combline))
#         except:
#             pass
#             print(R+' [-] Unhandled Exception Occured!')

#     try:
#         for uurl in urls:
#             print(G+"\n [+] Searching for comments on page: "+O+uurl+'\n')
#             req = requests.get(uurl)
#             comments = re.findall('<!--(.*)-->',req.text)
#             for comment in comments:
#                 print(C+'   '+comment)
#                 time.sleep(0.03)

#     except requests.exceptions:
#         print(R+' [-] Outbound Query Exception...')

#     if found == 0x00:
#         print(R+' [-] No comments found in source code!')

#     print(G+' [+] Comments Scraping Done!')
