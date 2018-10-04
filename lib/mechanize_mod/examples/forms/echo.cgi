#!/usr/bin/python
# -*-python-*-

print "Content-Type: text/html\n"
import sys
import os
import string
import cgi

from types import ListType

print "<html><head><title>Form submission parameters</title></head>"
form = cgi.FieldStorage()
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
