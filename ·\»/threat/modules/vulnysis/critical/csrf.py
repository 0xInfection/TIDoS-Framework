#!/usr/bin/env python
from core.colors import color
def csrf(target):
    print('This module is not yet available.')
    pass
# #!/usr/bin/env python
# #-*- coding: utf-8 -*-

# #-:-:-:-:-:-:-:-:-:-:-:-:#
# #    TIDoS Framework     #
# #-:-:-:-:-:-:-:-:-:-:-:-:#

# #Author: 0xInfection (@_tID)

# #Modified version of CSRFProbe
# #https://github.com/the-Infected-drake/CSRFProbe
# #This module requires TIDoS Framework
# #https://github.com/0xInfection/TIDoS-Framework

# from __future__ import print_function
# import difflib
# import cookielib
# from bs4 import BeautifulSoup
# import urllib
# import urllib2
# import re
# import time
# import ssl
# import sys
# sys.path.append('files/')
# from Crawler import *
# from Form import *
# from uri import *
# from core.Core.colors import *

# ssl.match_hostname = lambda cert, hostname: True

# def request(referer,action,form,opener):

#     data = urllib.urlencode(form)
#     headers = {'User-Agent' : 'Mozilla/5.0 (Windows 8.0; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)','Referer' : referer}
#     try:
#         return opener.open(action,data).read()

#     except urllib2.HTTPError:
#         print("HTTP Error 1: "+action)
#         return

#     except ValueError:
#         print("Value Error: "+action)
#         return

#     except:
#         return ''

# def check0x00(web):

#     print(R+'\n   ====================================================')
#     print(R+'    C R O S S   S I T E   R E Q U E S T   F O R G E R Y')
#     print(R+'   ====================================================')
#     time.sleep(0.7)
#     print(O+' [This module has only full support for domains of startpages]')
#     print(O+'   [Hence, may not satisfactorily work for all domains]\n')

#     if 'http' not in web:
#         web = 'http://' + web

#     # Just to make sure BeautifulSoup is working properly :)
#     form1="""<form action="/drupal/?q=node&amp;destination=node"  accept-charset="UTF-8" method="post" id="user-login-form">
#     <div><div class="form-item" id="edit-name-wrapper">
#      <label for="edit-name">Username: <span class="form-required" title="This field is required.">*</span></label>
#      <input type="text" maxlength="60" name="name" id="edit-name" size="15" value="test1" class="form-text required" />
#     </div>
#     <div class="form-item" id="edit-pass-wrapper">
#      <label for="edit-pass">Password: <span class="form-required" title="This field is required.">*</span></label>
#      <input type="password" value="a9z8e7" name="pass" id="edit-pass"  maxlength="60"  size="15"  class="form-text required" />
#     </div>
#     <input type="submit" name="op" id="edit-submit" value="Log in"  class="form-submit" />
#     <div class="item-list"><ul><li class="first"><a href="/drupal/?q=user/register" title="Create a new user account.">Create new account</a></li>
#     <li class="last"><a href="/drupal/?q=user/password" title="Request new password via e-mail.">Request new password</a></li>
#     </ul></div><input type="hidden" name="form_build_id" id="form-6a060c0861888b7321fab4f5ac6cb908" value="form-6a060c0861888b7321fab4f5ac6cb908"  />
#     <input type="hidden" name="form_id" id="edit-user-login-block" value="user_login_block"  />
#     </div></form> """

#     form2="""<form action="/drupal/?q=node&amp;destination=node"  accept-charset="UTF-8" method="post" id="user-login-form">
#     <div><div class="form-item" id="edit-name-wrapper">
#      <label for="edit-name">Username: <span class="form-required" title="This field is required.">*</span></label>
#      <input type="text" maxlength="60" name="name" id="edit-name" size="15" value="test2" class="form-text required" />
#     </div>
#     <div class="form-item" id="edit-pass-wrapper">
#      <label for="edit-pass">Password: <span class="form-required" title="This field is required.">*</span></label>
#      <input type="password" value="a9z8e7" name="pass" id="edit-pass"  maxlength="60"  size="15"  class="form-text required" />
#     </div>
#     <input type="submit" name="op" id="edit-submit" value="Log in"  class="form-submit" />
#     <div class="item-list"><ul><li class="first"><a href="/drupal/?q=user/register" title="Create a new user account.">Create new account</a></li>
#     <li class="last"><a href="/drupal/?q=user/password" title="Request new password via e-mail.">Request new password</a></li>
#     </ul></div><input type="hidden" name="form_build_id" id="form-6a060c0861888b7321fab4f5ac6cb908" value="form-6a060c0861888b7321fab4f5ac6cb908"  />
#     <input type="hidden" name="form_id" id="edit-user-login-block" value="user_login_block"  />
#     </div></form> """

#     Cookie0 = cookielib.CookieJar()
#     Cookie1 = cookielib.CookieJar()

#     resp1 = urllib2.build_opener(urllib2.HTTPCookieProcessor(Cookie0))
#     resp2 = urllib2.build_opener(urllib2.HTTPCookieProcessor(Cookie1))

#     actionDone = []

#     csrf=''
#     init1 = web
#     form = Form()

#     # Hope it works properly (no lxml error ;=;)
#     bs1=BeautifulSoup(form1).findAll('form',action=True)[0]
#     bs2=BeautifulSoup(form2).findAll('form',action=True)[0]

#     action = init1

#     resp1.open(action)
#     resp2.open(action)

#     crawler = Crawler(init1,resp1)
#     print(GR+" [*] Initializing crawling...")

#     global url
#     try:

#         while crawler.noinit():
#             url = crawler.next()
#             print(C+' [+] Crawling :> ' +B+ url)

#             try:
#                 soup=crawler.process(web)
#                 if not soup:
#                     continue;

#                 i=0
#                 print(O+' [*] Retrieving all forms on ' +C+ url +O+'...')
#                 for m in getAllForms(soup):
#                     action = uri.buildAction(url,m['action'])
#                     if not action in actionDone and action!='':
#                         try:
#                             print()
#                             result = form.prepareFormInputs(m)
#                             r1 = request(url, action, result, resp1)
#                             result = form.prepareFormInputs(m)
#                             r2 = request(url, action, result, resp2)

#                             if(len(csrf)>0):
#                                 if not re.search(csrf, r2):
#                                     print(G+ '[+] Looks like we got a CSRF vulnerability on '+O+url+G+'!\n')
#                                     try:
#                                         if m['name']:
#                                             print(R+'\n  =====')
#                                             print(R+'   PoC')
#                                             print(R+'  =====\n')
#                                             print(B+' [+] URL : ' +P+url)
#                                             print(C+' [+] Name : ' +O+m['name'])
#                                             print(G+' [+] Action : ' +O+m['action'])

#                                     except KeyError:

#                                         print(R+'\n  =====')
#                                         print(R+'   PoC')
#                                         print(R+'  =====\n')
#                                         print(B+' [+] URL : ' +P+url)
#                                         print(G+' [+] Action : ' +O+m['action'])

#                                     print(O+' [+] Code : '+W+urllib.urlencode(result))
#                                     print('')

#                                 continue;

#                             o2 = resp2.open(url).read()

#                             try:
#                                 form2 = getAllForms(BeautifulSoup(o2))[i]

#                             except IndexError:
#                                 print(R+' [-] Form Error')
#                                 continue;

#                             contents2 = form.prepareFormInputs(form2)
#                             r3 = request(url,action,contents2,resp2)

#                             checkdiff = difflib.ndiff(r1.splitlines(1),r2.splitlines(1))
#                             checkdiff0 = difflib.ndiff(r1.splitlines(1),r3.splitlines(1))

#                             result12 = []
#                             for n in checkdiff:
#                                 if re.match('\+|-',n):
#                                     result12.append(n)
#                             result13 = []
#                             for n in checkdiff0:
#                                 if re.match('\+|-',n):
#                                     result13.append(n)

#                             if len(result12)<=len(result13):

#                                 try:
#                                     if m['name']:

#                                         print(R+'\n  =====')
#                                         print(R+'   PoC')
#                                         print(R+'  =====\n')
#                                         print(B+' [+] URL : ' +P+url)
#                                         print(C+' [+] Name : ' +O+m['name'])
#                                         print(G+' [+] Action : ' +W+m['action'])

#                                 except KeyError:

#                                     print(R+'\n  =====')
#                                     print(R+'   PoC')
#                                     print(R+'  =====\n')
#                                     print(B+' [+] URL : ' +P+url)
#                                     print(G+' [+] Action : ' +W+m['action'])

#                                 print(O+' [+] Code : '+W+urllib.urlencode(result))
#                                 print('')

#                         except urllib2.HTTPError as msg:
#                             print(msg.__str__())
#                             pass

#                     actionDone.append(action)
#                     i+=1

#             except urllib2.URLError as e:
#                 print(R+' [-] Exception at %s' % url)
#                 print(R+' [-] Error : '+str(e))
#                 continue;

#     except KeyboardInterrupt:
#         print(R+"\n [-] Interrupted by user")

# def csrf(web):

#     try:
#         time.sleep(0.5)
#         print(GR+' [*] Loading up module...')
#         time.sleep(0.5)
#         check0x00(web)
#         print(G+" [+] Scan completed!")
#     except ssl.CertificateError:
#         print(R+" [-] This module only support domains of startpages...")

#     except:
#         pass
