#!/usr/bin/env python
from core.colors import color
def serverdetect(target):
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
# import re
# import socket
# import mechanize
# import cookielib
# from urllib import urlencode
# from re import search
# from core.Core.colors import *
# br = mechanize.Browser()

# # Cookie Jar
# cj = cookielib.LWPCookieJar()
# br.set_cookiejar(cj)

# # Browser options
# br.set_handle_equiv(True)
# br.set_handle_redirect(True)
# br.set_handle_referer(True)
# br.set_handle_robots(False)

# # Follows refresh 0 but not hangs on refresh > 0
# br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
# br.addheaders = [
#     ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# def serverdetect(web):

#     print(R+'\n   ===========================')
#     print(R+'    D E T E C T   S E R V E R')
#     print(R+'   ===========================\n')
#     time.sleep(0.4)
#     print(GR+' [*] Checking server status...')
#     web = web.replace('https://','')
#     web = web.replace('http://','')
#     try:
#         ip_addr = socket.gethostbyname(web)
#         print(G+' [+] Server detected online...')
#         time.sleep(0.5)
#         print(G+' [+] Server IP :> '+ip_addr)
#     except:
#         print(R+' [-] Server seems down...')

#     print(GR+' [*] Trying to identify backend...')
#     time.sleep(0.4)
#     web = 'http://' + web
#     try:
#         r = requests.get(web)
#         header = r.headers['Server']
#         if 'cloudflare' in header:
#             print(O+' [+] The website is behind Cloudflare.')
#             print(G+' [+] Server : Cloudflare')
#             time.sleep(0.4)
#             print(O+' [+] Use the "Cloudflare" VulnLysis module to try bypassing Clouflare...')

#         else:
#             print(B+' [+] Server : ' +C+header)
#         try:
#             print(O+' [+] Running On : ' +G+ r.headers['X-Powered-By'])
#         except:
#             pass
#     except:
#         print(R+' [-] Failed to identify server. Some error occured!')
#         pass

# # ===============================================================#
# # THIS HAS BEEN MIGRATED TO THE VULNERABILITY ENUMERATION MODULE
# # ===============================================================#

# #def bypass(domain):

# #    print GR+' [*] Trying to get real IP...'
#  #   post = urlencode({'cfS': domain})
#   #  result = br.open(
# #       'http://www.crimeflare.info/cgi-bin/cfsearch.cgi ', post).read()
# #
#  #   match = search(r' \b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', result)
#   #  if match:
#    #     bypass.ip_addr = match.group().split(' ')[1][:-1]
# #       print G+' [+] Cloudflare found misconfigured!'
# #       time.sleep(0.4)
# #       print GR+' [*] Identifying IP...'
# #       time.sleep(0.5)
#  #       print G+' [+] Real IP Address : ' + bypass.ip_addr + '\n'
#   #  else:
# #       print R+' [-] Cloudflare properly configured...'
# #       print R+' [-] Unable to find remote IP!\n'
# #       pass
# #
