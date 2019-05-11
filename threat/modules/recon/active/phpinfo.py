#!/usr/bin/env python
from core.colors import color
def phpinfo(target):
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
# import re
# import time
# import os
# import requests
# from core.Core.colors import *
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# pathsinfo = []
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# def phpinfo(web):

#     found = 0x00
#     print(R+'\n    =============================')
#     print(R+'     P H P I N F O   F I N D E R')
#     print(R+'    =============================\n')

#     print(GR+' [*] Importing file paths...')
#     if os.path.exists('files/fuzz-db/phpinfo_paths.lst'):
#         with open('files/fuzz-db/phpinfo_paths.lst','r') as paths:
#             for path in paths:
#                 path = '/' + path.replace('\n','')
#                 pathsinfo.append(path)

#         print(O+' [!] Starting bruteforce...')
#         for p in pathsinfo:
#             web0x00 = web + p
#             req = requests.get(web0x00, allow_redirects=False, verify=False)
#             if (req.status_code == 200 or req.status_code == 302):
#                 if re.search(r'\<title\>phpinfo()\<\/title\>|\<h1 class\=\"p\"\>PHP Version',req.content):
#                     found = 0x01
#                     print(G+' [+] Found PHPInfo File At : '+O+web0x00)
#             else:
#                 print(B+' [*] Checking : '+C+web0x00+R+' ('+str(req.status_code)+')')

#         if found == 0x00:
#             print(R+'\n [-] Did not find PHPInfo file...\n')
#     else:
#         print(R+' [-] Bruteforce filepath not found!')
