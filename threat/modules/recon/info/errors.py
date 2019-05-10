#!/usr/bin/env python
from core.colors import color
def errors(target):
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
# import re
# import sys
# sys.path.append('files/signature-db/')
# import time
# import requests
# from core.Core.colors import *
# from re import search
# from bs4 import BeautifulSoup
# from commonerror_signatures import patterns
# urls = []
# links = []
# found = 0x00

# def check0x00(content,url):

#     for pattern in patterns:
#         print(C+' [!] Finding '+B+pattern+C+' ...')
#         time.sleep(0.005)
#         if search(pattern, content):
#             print(G+' [!] Possible error at '+O+url)
#             print(G+" [+] Found : \"%s\" at %s" % (pattern,url))
#             found = 0x01

# def request(url):

#     time.sleep(0.5)
#     links = [url]
#     po = url.split('//')[1]
#     for w in links:
#         print(GR+' [*] Scraping Page: '+O+url)
#         req = requests.get(w).text
#         check0x00(req, url)

#     soup = BeautifulSoup(req,'lxml')
#     for line in soup.find_all('a', href=True):
#         newline = line['href']
#         try:
#             if newline[:4] == "http":
#                 if po in newline:
#                     urls.append(str(newline))
#             elif newline[:1] == "/":
#                 combline = url+newline
#                 urls.append(str(combline))
#         except:
#             print(R+' [-] Unhandled Exception Occured!')

#     try:
#         for uurl in urls:
#             print(G+"\n [+] Scraping Page: "+O+uurl)
#             req = requests.get(uurl).text
#             check0x00(req, url)

#     except requests.exceptions:
#         print(R+' [-] Outbound Query Exception...')

#     if found == 0x00:
#         print(R+'\n [-] No Errors found in Source Code!\n')

#     print(G+' [+] Scraping Done!')

# def errors(web):

#     print(R+'\n       =========================')
#     print(R+'        E R R O R   H U N T E R ')
#     print(R+'       =========================')
#     print(O+'  [This module covers up Full Path Disclosures]\n')
#     print(GR+' [*] Making the request...')
#     time.sleep(0.5)
#     request(web)
