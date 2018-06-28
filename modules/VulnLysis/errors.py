#!/usr/bin/env python2
# coding: utf-8

#-:-:-:-:-:-:-:-:-:-:-:-:#
#    TIDoS Framework     #
#-:-:-:-:-:-:-:-:-:-:-:-:#

#This module requires TIDoS Framework
#https://github.com/theInfectedDrake/TIDoS-Framework 

import re
import time
import requests
from colors import *

from re import search
from lib.utils.printer import *

def error0x00(content,url):
	patterns = ("<font face=\"Arial\" size=2>error \'800a0005\'</font>",
				"<h2> <i>Runtime Error</i> </h2></span>",
				"<p>Active Server Pages</font> <font face=\"Arial\" size=2>error \'ASP 0126\'</font>",
				"Warning: session_start():",
				"<b> Description: </b>An unhandled exception occurred during the execution of the",
				"<H1>Error page exception</H1>",
				"<h2> <i>Runtime Error</i> </h2></span>",
				"<b>Fatal Error</b>",
				"<h2> <i>Access is denied</i> </h2></span>",
				"Warning: opendir(Array):",
				"<H3>Original Exception: </H3>",
				"Server object error",
				"invalid literal for int()",
				"exceptions.ValueError",
				"\[an error occurred while processing this directive\]",
				"<HTML><HEAD><TITLE>Error Occurred While Processing Request</TITLE>",
				"</HEAD><BODY><HR><H3>Error Occurred While Processing Request</H3><P>",
				"\[java.lang.",
				"class java.lang.",
				"java.lang.NullPointerException",
				"java.rmi.ServerException",
				"at java.lang.",
				"onclick=\"toggle(\'full exception chain stacktrace\')",
				"at org.apache.catalina",
				"at org.apache.coyote.",
				"at org.apache.tomcat.",
				"at org.apache.jasper.",
				"<html><head><title>Application Exception</title>",
				"<p>Microsoft VBScript runtime </font>",
				"<font face=\"Arial\" size=2>error '800a000d'</font>",
				"<TITLE>nwwcgi Error",
				"The session id contains illegal characters",
				"\] does not contain handler parameter named",
				"PythonHandler django.core.handlers.modpython",
				"t = loader.get_template(template_name) # You need to create a 404.html template.",
				"<h2>Traceback <span>(innermost last)</span></h2>",
				"<h1 class=\"error_title\">Ruby on Rails application could not be started</h1>",
				"<title>Error Occurred While Processing Request</title></head><body><p></p>",
				"<HTML><HEAD><TITLE>Error Occurred While Processing Request</TITLE></HEAD><BODY><HR><H3>",
				"<TR><TD><H4>Error Diagnostic Information</H4><P><P>",
				"<li>Search the <a href=\"http://www.macromedia.com/support/coldfusion/\"",
				"target=\"new\">Knowledge Base</a> to find a solution to your problem.</li>",
				"Server.Execute Error",
				"<h2 style=\"font:8pt/11pt verdana; color:000000\">HTTP 403.6 - Forbidden: IP address rejected<br>",
				"<TITLE>500 Internal Server Error</TITLE>",
				"<b>warning</b>[/]\w\/\w\/\S*",
				"<b>Fatal error</b>:",
				"<b>Warning</b>:",
				"open_basedir restriction in effect",
				"eval()'d code</b> on line <b>",
				"Fatal error</b>:  preg_replace",
				"thrown in <b>",
				"Stack trace:",
				"</b> on line <b>"
				)
	for pattern in patterns:
		if search(pattern,content):
			print G+' [!] Possible FPD at '+O+url
			print G+" [+] Found : \"%s\" at %s" % (pattern,url)

def request(web):

	req = requests.get(web, verify=False)
	print GR+' [*] Parsing the content...'
	m = req.content
	error0x00(m,web)

def errors(web):

	print R+'\n       ========================='
	print R+'        E R R O R   H U N T E R '
	print R+'       ========================='
	print O+'   [This module covers up Full Path Disclosure]\n'
	print GR+' [*] Making the request...'
	time.sleep(0.5)
	request(web)

