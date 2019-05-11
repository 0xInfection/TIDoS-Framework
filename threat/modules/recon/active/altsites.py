#!/usr/bin/env python
from core.colors import color
def altsites(target):
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
# import time
# import requests
# import hashlib
# from core.Core.colors import *

# md5s = {}
# responses = {}

# def altsites(web):

#     print(R+'\n    ===================================')
#     print(R+'     A L T E R N A T I V E   S I T E S')
#     print(R+'    ===================================\n')

#     print(GR+' [*] Setting User-Agents...')
#     time.sleep(0.7)
#     user_agents = {
#             'Chrome on Windows 8.1' : 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36',
#             'Safari on iOS'         : 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4',
#             'IE6 on Windows XP'     : 'Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
#             'Googlebot'             : 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
#             }

#     print(GR+'\n [*] Preparing for series of requests...')
#     for name, agent in user_agents.items():
#         print(B+' [+] Using User-Agent : '+C+name)
#         print(GR+' [+] UA Value : '+O+agent)
#         headers = {'User-Agent' : agent}
#         print(GR+' [*] Making the request...')
#         req = requests.get(web, headers=headers, allow_redirects=True, verify=True)
#         responses[name] = req

#     print(O+'\n [!] Comparing base value standards...')
#     time.sleep(0.5)
#     for name, response in responses.items():
#         print(B+' [+] User-Agent : '+C+name)
#         print(GR+' [+] Response : '+O+str(response))
#         md5s[name] = hashlib.md5(response.text.encode('utf-8')).hexdigest()

#     print(O+'\n [!] Matching hexdigest signatures...')
#     for name, md5 in md5s.iteritems():
#         print(B+'\n [+] User-Agent : '+C+name)
#         print(GR+' [+] Hex-Digest : '+O+str(md5))
#         if name != 'Chrome on Windows 8.1':
#             if md5 != md5s['Chrome on Windows 8.1']:
#                 print(G+' [+] '+O+str(name)+G+' differs fromk baseline!')
#             else:
#                 print(R+' [-] No alternative site found via User-Agent spoofing:'+ str(md5))
#     print(G+'\n [+] Alternate Site Discovery Completed!\n')
