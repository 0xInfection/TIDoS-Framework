#!/usr/bin/env python
from core.colors import color
from database.database_module import save_data


#save_data(host.database, host.module, host.lvl1, host.lvl2, host.lvl3, host.name, data)

# import os
# import sys
import requests
# import re
# import time
# import json

#from requests.packages.urllib3.exceptions import InsecureRequestWarning

#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def getRes0x00(target):
    for host in target:
        host.lvl2='hacked_emails'
        host.lvl3=''
#     email = raw_input(O+' [#] Enter the email :> '+R)
#     if '@' in email and '.' in email:
#         pass
#     else:
#         email = raw_input(O+' [#] Enter a valid email :> '+R)

#     print(' [*] Setting headers... (behaving as a browser)...')
#     time.sleep(0.7)
#     headers =   {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
#                  'Accept-Language':'en-US;',
#                  'Accept-Encoding': 'gzip, deflate',
#                  'Accept': 'text/html,application/xhtml+xml,application/xml;',
#                  'Connection':'close'}
#     print(O+' [!] Making the no-verify request...')
#     time.sleep(0.5)
#     url = 'https://hacked-emails.com/api?q='+str(email)

#     try:
#         req = requests.get(url, headers=headers, timeout=10, verify=False)
#         content = req.text
#         if content != "":
#             content = json.loads(content)
#             if content['status'] == "found":
#                 print("Result found ("+G+str(content['results']) + " results" + Style.RESET_ALL + ")")
#                 for line in content['data']:
#                     try:
#                         print(G+" [+] "+O+email+G+" found in : " +C+ str(line['title']) +R+" (" + str(line['date_leaked'])+')')
#                     except:
#                         print(R+" [-] Can't parse the leak titles via APi...")
#             else:
#                 print(R+' [-] Email '+O+email+R+' not found in any breaches!')
#         else:
#             print(R+' [-] Error found in Json Request...')

#     except Exception:
#         print(R+" [-] Can't reach url...")
#         print(R+' [-] Request timed out!')

def hackedmail(target):
    getRes0x00(target)
