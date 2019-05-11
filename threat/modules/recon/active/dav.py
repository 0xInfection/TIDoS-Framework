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
# import re
#!/usr/bin/env python
from core.colors import color
def dav(target):
    print('This module is not yet available.')
    pass
# import time
# import urllib2
# from re import search, I
# from core.Core.colors import *

# content_type = 'application/xml; charset="utf-8"'

# def htsearch(url):

#     print(O+' [!] Setting headers...')
#     time.sleep(0.7)
#     headers = {'Content-Type' : content_type}
#     print(O+' [!] Setting buffers...')
#     content =  "<?xml version='1.0'?>\r\n"
#     content += "<g:searchrequest xmlns:g='DAV:'>\r\n"
#     content += "<g:sql>\r\n"
#     content += "Select 'DAV:displayname' from scope()\r\n"
#     content += "</g:sql>\r\n"
#     content += "</g:searchrequest>\r\n"
#     time.sleep(0.7)
#     print(GR+' [*] Setting the parameters...')
#     req = urllib2.Request(url,headers=headers,data=content)
#     req.get_method = lambda : sr
#     try:
#         time.sleep(0.7)
#         print(GR+' [*] Making the request...')
#         resp = urllib2.urlopen(req)
#     except urllib2.HTTPError as e:
#         print(R+' [-] Exception : '+str(e))

#     print(C+' [+] Matching the signatures...')
#     time.sleep(0.7)
#     regexp = r'<a:response>|<a:status>|xmlns:a=\"DAV:\"'
#     if re.search(regexp,resp.read()) and str(resp.code) == '200':
#         print(G+' [+] HTTP Search Method found Enabled!')
#         print(G+' [+] DAV Directory Listing at : '+O+url)
#     else:
#         print(R+' [-] No HTTP Searching Profiling Found...')

# def profind(url):

#     print(O+' [!] Setting headers...')
#     headers = {'Depth' : 1,
#                'Content-Type' : content_type}
#     time.sleep(0.7)
#     print(O+' [!] Setting buffers...')
#     content = "<?xml version='1.0'?>\r\n"
#     content += "<a:propfind xmlns:a='DAV:'>\r\n"
#     content += "<a:prop>\r\n"
#     content += "<a:displayname:/>\r\n"
#     content += "</a:prop>\r\n"
#     content += "</a:propfind>\r\n"
#     time.sleep(0.7)
#     print(GR+' [*] Setting the parameters...')
#     req = urllib2.Request(url,headers=headers,data=content)
#     req.get_method = lambda : pro
#     time.sleep(0.7)
#     try:
#         print(GR+' [*] Making the request...')
#         resp = urllib2.urlopen(req)
#     except urllib2.HTTPError as e:
#         print(R+' [-] Exception : '+str(e))
#     time.sleep(0.7)
#     print(C+' [+] Matching the signatures...')
#     if 'D:href' in resp.read() and resp.code == 200:
#         print(G+' [+] HTTP Profind Method Found Enabled!')
#         print(G+' [+] DAV Directory Listing at : '+O+url)
#     else:
#         print(R+' [-] No Profind HTTP Profiling Found...')

# def dav(web):

#     print(GR+' [*] Loading module...')
#     time.sleep(0.7)
#     print(R+'\n    =========================================')
#     print(R+'     D A V   H T T P   E N U M E R A T I O N')
#     print(R+'    =========================================\n')
#     time.sleep(0.7)
#     print(O+' [!] Loading HTTP methods...')
#     global pro, sr
#     pro = 'PROFIND'
#     sr = 'SEARCH'
#     print(GR+'\n [*] Initiating HTTP Search module...')
#     htsearch(web)
#     print(G+' [+] HTTP Search module Completed!')
#     time.sleep(1)
#     print(GR+'\n [*] Initiating HTTP Profind Moule...')
#     profind(web)
#     print(G+' [+] HTTP Profind Module Completed!')

#     print(G+' [+] HTTP Profiling of DAV Completed!\n')
