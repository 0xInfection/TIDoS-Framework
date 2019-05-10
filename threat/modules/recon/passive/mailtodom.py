#!/usr/bin/env python
from core.colors import color
def mailtodom(target):
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
# import os
# import sys
# import requests
# import re
# import time
# from core.Core.colors import *
# from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# def getRes0x00():

#     email = raw_input(O+' [#] Enter the email :> '+R)
#     if '@' in email and '.' in email:
#         pass
#     else:
#         email = raw_input(O+' [#] Enter a valid email :> '+R)

#     print(GR+' [*] Setting headers... (behaving as a browser)...')
#     time.sleep(0.7)
#     headers =   {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
#                  'Accept-Language':'en-US;',
#                  'Accept-Encoding': 'gzip, deflate',
#                  'Accept': 'text/html,application/xhtml+xml,application/xml;',
#                  'Connection':'close'}
#     print(O+' [!] Making the no-verify request...')
#     time.sleep(0.5)
#     url = "https://whoisology.com/search_ajax/search?action=email&value="+email+"&page=1&section=admin"
#     result = ''
#     try:
#         result = requests.get(url, headers=headers, verify=False, timeout=10).content
#         if result != '':
#             regex = re.compile('whoisology\.com\/(.*?)">')
#             stuff = regex.findall(result)
#             if len(stuff) > 0:
#                 for line in stuff:
#                     if line.strip() != '':
#                         if '.' in line:
#                             print(G+' [+] Received Domain : '+O+line)
#             else:
#                 print(R+ " [-] Empty domain result for email : "+O+email)
#     except:
#         print(R+" [-] Can't reach url...")
#         print(R+' [-] Request timed out!')

# def mailtodom():

#     print(GR+' [*] Loading module...')
#     time.sleep(0.6)
#     print(R+'\n    ===============================')
#     print(R+'     E M A I L   T O   D O M A I N ')
#     print(R+'    ===============================\n')
#     time.sleep(0.7)
#     getRes0x00()
