#!/usr/bin/python
# -*-python-*-

# This is used by functional_tests.py

#import cgitb; cgitb.enable()

import time

print "Content-Type: text/html"
year_plus_one = time.localtime(time.time())[0] + 1
expires = "expires=09-Nov-%d 23:12:40 GMT" % (year_plus_one,)
print "Set-Cookie: foo=bar; %s" % expires
print "Set-Cookie: sessioncookie=spam\n"
import sys
import os
import string
import cgi
import Cookie
import urllib
from xml.sax import saxutils

from types import ListType

print "<html><head><title>Cookies and form submission parameters</title>"
cookie = Cookie.SimpleCookie()
cookieHdr = os.environ.get("HTTP_COOKIE", "")
cookie.load(cookieHdr)
form = cgi.FieldStorage()
refresh_value = None
if "refresh" in form:
    refresh = form["refresh"]
    if not isinstance(refresh, ListType):
        refresh_value = refresh.value
if refresh_value is not None:
    print '<meta http-equiv="refresh" content=%s>' % (
        saxutils.quoteattr(urllib.unquote_plus(refresh_value)))
elif "foo" not in cookie:
    print '<meta http-equiv="refresh" content="5">'

print "</head>"
print "<p>Received cookies:</p>"
print "<pre>"
print cgi.escape(os.environ.get("HTTP_COOKIE", ""))
print "</pre>"
if "foo" in cookie:
    print "<p>Your browser supports cookies!"
if "sessioncookie" in cookie:
    print "<p>Received session cookie"
print "<p>Referer:</p>"
print "<pre>"
print cgi.escape(os.environ.get("HTTP_REFERER", ""))
print "</pre>"
print "<p>Received parameters:</p>"
print "<pre>"
for k in form.keys():
    v = form[k]
    if isinstance(v, ListType):
        vs = []
        for item in v:
            vs.append(item.value)
        text = string.join(vs, ", ")
    else:
        text = v.value
    print "%s: %s" % (cgi.escape(k), cgi.escape(text))
print "</pre></html>"
