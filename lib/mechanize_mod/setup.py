#!/usr/bin/env python
"""Stateful programmatic web browsing.

Stateful programmatic web browsing, after Andy Lester's Perl module
WWW::Mechanize.

mechanize.Browser implements the urllib2.OpenerDirector interface.  Browser
objects have state, including navigation history, HTML form state, cookies,
etc.  The set of features and URL schemes handled by Browser objects is
configurable.  The library also provides an API that is mostly compatible with
urllib2: your urllib2 program will likely still work if you replace "urllib2"
with "mechanize" everywhere.

Features include: ftp:, http: and file: URL schemes, browser history, hyperlink
and HTML form support, HTTP cookies, HTTP-EQUIV and Refresh, Referer [sic]
header, robots.txt, redirections, proxies, and Basic and Digest HTTP
authentication.

Much of the code originally derived from Perl code by Gisle Aas (libwww-perl),
Johnny Lee (MSIE Cookie support) and last but not least Andy Lester
(WWW::Mechanize).  urllib2 was written by Jeremy Hylton.

"""

import os
import setuptools
import sys

if sys.version_info < (2, 7):
    raise SystemExit('mechanize requires python >= 2.7')

if sys.version_info.major > 2:
    raise SystemExit('mechanize only works on python 2.x')

VERSION = open(os.path.join("mechanize", "_version.py")).\
    readlines()[0].strip(' "\n')

CLASSIFIERS = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: BSD License
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 2 :: Only
Topic :: Internet
Topic :: Internet :: File Transfer Protocol (FTP)
Topic :: Internet :: WWW/HTTP
Topic :: Internet :: WWW/HTTP :: Browsers
Topic :: Internet :: WWW/HTTP :: Indexing/Search
Topic :: Internet :: WWW/HTTP :: Site Management
Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Software Development :: Testing
Topic :: Software Development :: Testing :: Traffic Generation
Topic :: System :: Archiving :: Mirroring
Topic :: System :: Networking :: Monitoring
Topic :: System :: Systems Administration
Topic :: Text Processing
Topic :: Text Processing :: Markup
Topic :: Text Processing :: Markup :: HTML
Topic :: Text Processing :: Markup :: XML
"""


def main():
    setuptools.setup(
        name="mechanize",
        version=VERSION,
        license="BSD",
        platforms=["any"],
        install_requires=['html5lib>=0.999999999'],
        extras_require={'fast': ['html5-parser>=0.4.4']},
        classifiers=[c for c in CLASSIFIERS.split("\n") if c],
        zip_safe=True,
        author="Kovid Goyal",
        author_email='no@no.no',
        description=__doc__.split("\n", 1)[0],
        long_description=__doc__.split("\n", 2)[-1],
        url="https://github.com/python-mechanize/mechanize",
        download_url=("https://pypi.python.org/packages/source/m/mechanize/"
                      "mechanize-%s.tar.gz" % VERSION),
        packages=["mechanize"],
    )


if __name__ == "__main__":
    main()
