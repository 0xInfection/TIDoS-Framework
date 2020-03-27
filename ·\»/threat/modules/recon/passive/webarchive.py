#!/usr/bin/env python
from core.colors import color
def webarchive(target):
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
# import json
# from core.Core.colors import *
# from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# def getRes0x00(web):

#     error = 0
#     fdate = raw_input(O+' [#] Year from when results to be fetched (eg. 2010) :> '+C)
#     tdate = raw_input(GR+' [#] Year till when results to be fetched (eg. 2017) :> '+C)
#     limit = raw_input(O+' [#] No. of results (eg. 50) :> '+C)

#     if "://" in web:
#         web = web.split('://')[1]

#     print(GR+' [*] Setting headers... (behaving as a browser)...')
#     time.sleep(0.7)
#     headers =   {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
#                  'Accept-Language':'en-US;',
#                  'Accept-Encoding': 'gzip, deflate',
#                  'Accept': 'text/html,application/xhtml+xml,application/xml;',
#                  'Connection':'close'}
#     print(GR+' [*] Setting parameters...')
#     url = "https://web.archive.org/cdx/search/cdx?url="+web+"&matchType=domain&limit="+limit+"&output=json&from="+fdate+"&to="+tdate
#     time.sleep(0.5)
#     try:
#         print(O+' [!] Making the no-verify request...')
#         req = requests.get(url, headers=headers, timeout=10, verify=False)
#         json_data = json.loads(req.text)
#         if len(json_data) == 0:
#             print(R+' [-] No results found!')
#             error = 1
#     except Exception as e:
#         print(R+' [-] Error loading Url...')
#         print(R+' [-] Request got timed out!')
#         error = 1

#     if error == 0:
#         try:
#             print(GR+' [*] Found the following backups at '+O+'web.archive.org...\n')
#             result = [ x for x in json_data if x[2] != 'original']
#             result.sort(key=lambda x: x[1])
#             for line in result:
#                 timestamp = line[1]
#                 website   = line[2]
#                 tlinks  = "https://web.archive.org/web/" + str(timestamp) + "/" + str(website)
#                 sdates = str(timestamp[:4]) + "/" + str(timestamp[4:6]) + "/" + str(timestamp[6:8])
#                 print(" {}{}   {}{}  {}({})".format(C, sdates, B, website, O, tlinks))
#                 time.sleep(0.04)

#         except Exception as e:
#             print(R+' [-] Unhandled Exception Encountered!')
#             print(R+' [-] Exception : '+str(e))

# def webarchive(web):

#     print(GR+' [*] Loading module...')
#     time.sleep(0.6)
#     print(R+'\n    =============================================')
#     print(R+'     W A Y B A C K   M A C H I N E   L O O K U P')
#     print(R+'    =============================================\n')
#     time.sleep(0.7)
#     getRes0x00(web)
