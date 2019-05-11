#!/usr/bin/env python
from core.colors import color
def robot(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # coding:  utf-8

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author : @_tID
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import requests, time
# from time import sleep
# from core.Core.colors import *

# def robot(web):

#     print(R+'\n   =============================')
#     print(R+'    R O B O T S   C H E C K E R')
#     print(R+'   =============================\n')

#     url = web + '/robots.txt'
#     print(' [!] Testing for robots.txt...\n')
#     try:
#         resp = requests.get(url).text
#         m = str(resp)
#         print(O+' [+] Robots.txt found!')
#         print(GR+' [*] Displaying contents of robots.txt...')
#         print(G+m)
#     except:
#         print(R+' [-] Robots.txt not found')

#     print(' [!] Testing for sitemap.xml...\n')
#     url0 = web + '/sitemap.xml'
#     try:
#         resp = requests.get(url0).text
#         m = str(resp)
#         print(O+' [+] Sitemap.xml found!')
#         print(GR+' [*] Displaying contents of sitemap.xml')
#         print(G+m)
#     except:
#         print(R+' [-] Sitemap.xml not found')
