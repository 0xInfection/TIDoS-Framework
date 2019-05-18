#!/usr/bin/env python
from core.colors import color
def icors(target):
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
# import re
# import sys
# import ssl
# import urllib2
# import urlparse
# import time
# from core.Core.colors import *

# def check0x00(url):

#     print(GR+' [*] Making request with random cookie value...')
#     time.sleep(0.4)
#     host = re.sub("^https?://", "", url)
#     if 'https://' in url:
#         print(O+' [!] Ignoring certificate errors...')
#         acao = cors0x00(url, True, True)
#     else:
#         print(GR+' [*] Passing values...')
#         acao = cors0x00(url, False, True)

#     if acao:

#         if (acao == "no_acac" or "*" == acao):
#             print(O+'\n [+] Access Control Allow Origin present (Without Credentials)...')
#         elif acao == "*":
#             print(O+' [!] Access Control Allow Origin present (point blank)...')
#         elif acao in ["//", "://"]:
#             print(G+' [+] Possible iCORS vulnerability found!...')
#             print(G+' [+] Access Control Allow Origin : '+O+'Any Origin Allowed...')
#         elif re.findall("\s|,|\|", acao):
#             print(R+' [¬]  Access Control Allow Origin present (multiple Credentials)...')
#         elif re.findall("\*.", acao):
#             print(R+' [-] Invalid iCORS : Only "*" is valid...')
#         elif re.findall("fiddle.jshell.net|s.codepen.io", acao):
#             print(GR+' [!] Access Control Allow Origin : Developer backdoor found!...')
#         elif "evil.org" in cors0x00(url, "evil.org"):
#             print(G+' [+] Access Control Allow Origin present : Origin Reflection...')
#         elif "null" == cors0x00(url, "null").lower():
#             print(G+' [+] Access Control Allow Origin present : Null Misconfiguration...')
#         elif host+".tk" in cors0x00(url, host+".tk"):
#             print(G+' [+] Access Control Allow Origin present : Post-domain Wildcard...')
#         elif "not"+host in cors0x00(url, "not"+url):
#             print(GR+' [¬] Access Control Allow Origin present : Post-Subdomain WildCard...')
#         elif "sub."+host in cors0x00(url, "sub."+url):
#             print(G+' [+] Access Control Allow Origin present : Arbitrary Subdomains Allowed...')
#         elif cors0x00(url, url, True).startswith("http://"):
#             print(G+' [+] Access Control Allow Origin present : Non-SSL Sites Allowed...')
#         else:
#             print(G+' [+] Access Control Allow Origin present : '+acao)

#     else:
#         print(R+' [-] Not vulnerable to iCORS...')
#     time.sleep(1)

# def cors0x00(url, ssltest, firstrun=False):

#     try:

#         request = urllib2.Request(url)
#         print(C+' [!] Setting origin : '+url)
#         request.add_header('Origin', url)
#         request.add_header('Cookie', "")
#         print(C+' [!] Setting user agent...')
#         request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64)')
#         if 'https://' not in url:
#             response = urllib2.urlopen(request, timeout=10)
#         else:
#             response = urllib2.urlopen(request, timeout=10, context=ssl._create_unverified_context())
#         acao = response.info().getheader('Access-Control-Allow-Origin')
#         acac = str(response.info().getheader('Access-Control-Allow-Credentials')).lower() == "true"
#         vary = "Origin" in str(response.info().getheader('Vary'))

#         if not acac:
#             print(O+' [*] Checking whether Access-Control-Allow-Credentials header value present...')
#             acao = "no_acac"
#         if acac and acao != '*':
#             print(G+" [+] Access-Control-Allow-Credentials present...")
#         if vary:
#             print(O+ " [!] Access-Control-Allow-Origin dynamically generated...")

#         return acao

#     except Exception as e:
#         print(R+' [-] Something happened...')
#         print(R+' [-] Error : '+str(e))

# def icors(web):

#     print(GR+' [*] Loading module...')
#     print(R+'\n    =========================================')
#     print(R+'     iNSECURE CROSS ORIGIN RESCOURCE SHARING')
#     print(R+'    =========================================\n')

#     check0x00(web)
#     time.sleep(1)
