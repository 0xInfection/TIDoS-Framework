#!/usr/bin/env python

# Search PyPI, the Python Package Index, and retrieve latest mechanize tarball.

# This is just to demonstrate mechanize: You should use easy_install to do
# this, not this silly script.

import sys
import os
import urlparse

import mechanize


def download_mechanize():
    browser = mechanize.Browser(factory=mechanize.RobustFactory())
    browser.set_handle_robots(False)

    browser.open("http://pypi.python.org/pypi")
    browser.select_form(name="searchform")
    browser.form["term"] = "mechanize"
    browser.submit()
    browser.follow_link(text_regex="mechanize-?(.*)")
    link = browser.find_link(text_regex=r"\.tar\.gz")
    filename = os.path.basename(urlparse.urlsplit(link.url)[2])
    if os.path.exists(filename):
        sys.exit("%s already exists, not grabbing" % filename)
    browser.retrieve(link.url, filename)


if __name__ == "__main__":
    download_mechanize()
