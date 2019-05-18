#!/usr/bin/env python
from core.colors import color
def cloudflaremisc(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# # coding: utf-8

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import requests
# import time
# import re
# import socket
# import mechanize
# import cookielib
# from urllib import urlencode
# from re import search
# from core.Core.colors import *
# br = mechanize.Browser()

# cj = cookielib.LWPCookieJar()
# br.set_cookiejar(cj)

# br.set_handle_equiv(True)
# br.set_handle_redirect(True)
# br.set_handle_referer(True)
# br.set_handle_robots(False)

# br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
# br.addheaders = [
#     ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# def cloud0x00(web):

#     web = web.replace('https://','')
#     web = web.replace('http://','')
#     print(R+'\n   =========================================')
#     print(R+'    C L O U D F L A R E   M I S C O N F I G.')
#     print(R+'   =========================================\n')
#     time.sleep(0.4)
#     print(GR+' [*] Checking server status...')
#     try:
#         ip_addr = socket.gethostbyname(web)
#         print(G+' [+] Server detected online...')
#         time.sleep(0.5)
#         print(G+' [+] Server IP :> '+O+ip_addr)
#     except:
#         print(R+' [-] Server seems down...')

#     print(GR+' [*] Trying to identify backend...')
#     time.sleep(0.4)
#     web = 'http://' + web
#     try:
#         print(GR+' [*] Making the no-verify request...')
#         time.sleep(0.6)
#         r = requests.get(web, verify=False)
#         header = r.headers['Server']
#         if 'cloudflare' in header:
#             print(O+' [+] The website is behind '+R+'Cloudflare.')
#             print(G+' [+] Server : Cloudflare')
#             time.sleep(0.4)
#             m = raw_input(O+' [+] Do you want TIDoS to try and bypass Cloudflare? (y/n) :> ')
#             if m == 'y' or m == 'Y':
#                 bypass(web)
#             elif m == 'n' or m == 'N':
#                 pass
#             else:
#                 print(R+' [-] Invalid choice...')
#                 serverdetect(web)
#             try:
#                 ip_addr = bypass.ip_addr
#             except:
#                 pass
#         else:
#             print(R+' [-] Website does not seem to be a part of Cloudflare Network...')
#     except:
#         print(R+' [-] Failed to identify server.\n [-] Some error occured!')
#         pass

# def bypass(domain):

#     print(GR+' [*] Trying to get real IP...')
#     post = urlencode({'cfS': domain})
#     result = br.open(
#         'http://www.crimeflare.info/cgi-bin/cfsearch.cgi ', post).read()

#     match = search(r' \b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', result)
#     if match:
#         bypass.ip_addr = match.group().split(' ')[1][:-1]
#         print(G+' [+] Cloudflare found misconfigured!')
#         time.sleep(0.4)
#         print(GR+' [*] Identifying IP...')
#         time.sleep(0.5)
#         print(G+' [+] Real IP Address : ' + bypass.ip_addr + '\n')
#     else:
#         print(R+' [-] Cloudflare properly configured...')
#         print(R+' [-] Unable to find remote IP!\n')
#         pass

# def cloudflaremisc(web):

#     print(GR+' [*] Loading...')
#     time.sleep(0.5)
#     cloud0x00(web)
