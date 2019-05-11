#!/usr/bin/env python
from core.colors import color
def links(target):
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
# import time
# import os
# import sys
# sys.path.append('tmp/')
# import requests
# from core.Core.colors import *

# final_links = []

# def links(web):

#     print(R+'\n   =====================')
#     print(R+'    P A G E   L I N K S ')
#     print(R+'   =====================\n')
#     time.sleep(0.4)
#     print('' + GR + color.BOLD + ' [!] Fetching links to the website...')
#     time.sleep(0.4)
#     print(GR +" [~] Result: "+ color.END)
#     web0 = web.replace('http://','')

#     domains = [web]
#     for dom in domains:
#         text = requests.get('http://api.hackertarget.com/pagelinks/?q=' + dom).text
#         result = str(text)
#         if 'error' not in result and 'no links found' not in result:

#             woo = result.splitlines()
#             for w in woo:
#                 if str(web0).lower() in w.lower():
#                     final_links.append(w)

#             print(O+'\n [!] Receiving links...')
#             for p in final_links:
#                 print(G+' [+] Found link : '+O+p)
#                 time.sleep(0.06)

#             if 'http://' in web:
#                 po = web.replace('http://','')
#             elif 'https://' in web:
#                 po = web.replace('https://','')
#             p = 'tmp/logs/'+po+'-logs/'+str(po)+'-links.lst'
#             open(p, 'w+')
#             print(B+' [!] Saving links...')
#             time.sleep(1)
#             for m in final_links:
#                 m = m + '\n'
#                 ile = open(p,"a")
#                 ile.write(m)
#                 ile.close()
#             pa = os.getcwd()
#             print(G+' [+] Links saved under '+pa+'/'+p+'!')
#             print('')

#         else:
#             print(R+' [-] Outbound Query Exception!')
#             time.sleep(0.8)
