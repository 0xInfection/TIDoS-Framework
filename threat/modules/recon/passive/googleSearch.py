#!/usr/bin/env python
from core.colors import color
def googleSearch(target):
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
# import time
# import sys, platform
# import os
# import urllib2
# try:
#     from google import search
# except:
#     from googlesearch import search
# from time import sleep
# from core.Core.colors import *

# def googleSearch():

#     try:
#         time.sleep(0.4)
#         print(R+'\n   ===========================')
#         print(R+'    G O O G L E   S E A R C H')
#         print(R+'   ===========================\n')
#         lol = raw_input(O+ " [#] QUERY :> " + color.END)
#         time.sleep(0.8)
#         m = raw_input(O+' [#] Search limit (not recommended above 30) :> ')
#         print(G+ " [!] Below are the list of websites with info on '" +lol+ "'")
#         x = search(lol, tld='com', lang='es', stop=int(m))
#         for url in x:
#             print(O+"   [!] Site Found :> "+W + url)
#             q = open('.google-cookie','w')
#             q.close()
#     except urllib2.HTTPError:
#         print(R+' [-] You have used google many times.')
#         print(R+' [-] Service temporarily unavailable.')
