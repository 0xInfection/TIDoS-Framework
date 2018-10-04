#!/usr/bin/env python

from __future__ import print_function
import sys

from mechanize import Browser, urljoin, urlopen

if len(sys.argv) == 1:
    uri = "http://wwwsearch.sourceforge.net/"
else:
    uri = sys.argv[1]

br = Browser()
br.open(urljoin(uri, "mechanize/example.html"))
form = next(br.forms())
form = br.forms[0]
print(form)
form["comments"] = "Thanks, Gisle"
# form.click() returns a mechanize.Request object
# (see HTMLForm.click.__doc__ if you want to use only the forms support, and
# not the rest of mechanize)
print(urlopen(form.click()).read())
