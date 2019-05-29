#!/usr/bin/env python
from core.colors import color
def internalip(target):
    print('This module is not yet available.')
    pass
    # #!/usr/bin/env python
# # coding: utf-8
# #
# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #
# #Author : @_tID (0xInfection)
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import re
# import sys
# import time
# import requests
# from core.Core.colors import *
# sys.path.append('files/signature-db/')
# from bs4 import BeautifulSoup
# from infodisc_signatures import INTERNAL_IP_SIGNATURE as signature
# links = []
# urls = []
# found = 0x00
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# def internalip0x00(url):

#     print(R+'\n    ========================')
#     print(R+'     INTERNAL IP DISCLOSURE')
#     print(R+'    ========================\n')
#     time.sleep(0.5)
#     links = [url]
#     po = url.split('//')[1]
#     for w in links:
#         print(GR+' [*] Scraping Page: '+O+url)
#         req = requests.get(w).text
#         check0x00(req)

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
#             check0x00(req)

#     except requests.exceptions:
#         print(R+' [-] Outbound Query Exception...')

#     if found == 0x00:
#         print(R+'\n [-] No Internal IPs found disclosed in plaintext in source code!\n')

#     print(G+' [+] Scraping Done!')

# def check0x00(req):
#     comments = re.findall(signature,req)
#     print(GR+" [*] Searching for Internal IPs...")
#     for comment in comments:
#         print(C+'   '+comment)
#         time.sleep(0.03)
#         found = 0x01

# def internalip(web):

#     print(GR+' [*] Loading module...')
#     time.sleep(0.6)
#     internalip0x00(web)
