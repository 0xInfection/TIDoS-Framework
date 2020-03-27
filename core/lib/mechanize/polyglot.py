#!/usr/bin/env python
# vim:fileencoding=utf-8
# Copyright: 2018, Kovid Goyal <kovid at kovidgoyal.net>

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
import collections

is_py2 = sys.version_info.major < 3

if is_py2:
    import types
    from urllib import (
            urlencode, pathname2url, quote, addinfourl, quote_plus,
            urlopen, splitattr, splithost as urllib_splithost, getproxies,
            ftpwrapper, proxy_bypass as urllib_proxy_bypass, splitpasswd,
            splitport, splittype, splituser, splitvalue,
            unquote, unwrap, url2pathname
    )
    from urllib2 import (
            HTTPError, URLError, install_opener, build_opener, ProxyHandler
    )
    from robotparser import RobotFileParser
    from urlparse import urlsplit, urljoin, urlparse, urlunparse
    from httplib import HTTPMessage, HTTPConnection, HTTPSConnection
    from cookielib import (
            DEFAULT_HTTP_PORT, CookiePolicy, DefaultCookiePolicy,
            FileCookieJar, LoadError, LWPCookieJar, _debug, domain_match,
            eff_request_host, escape_path, is_HDN, lwp_cookie_str, reach,
            request_path, request_port, user_domain_match, Cookie, CookieJar,
            MozillaCookieJar, request_host)
    from cStringIO import StringIO
    from future_builtins import map  # noqa

    def is_string(x):
        return isinstance(x, basestring)

    def iteritems(x):
        return x.iteritems()

    def itervalues(x):
        return x.itervalues()

    def is_class(obj):
        return isinstance(obj, (types.ClassType, type))

    def raise_with_traceback(exc):
        exec('raise exc, None, sys.exc_info()[2]')

    def is_mapping(x):
        return isinstance(x, collections.Mapping)

    codepoint_to_chr = unichr
    unicode_type = unicode
    create_response_info = HTTPMessage


else:
    from urllib.error import HTTPError, URLError
    from urllib.robotparser import RobotFileParser
    from urllib.parse import (
            urlsplit, urljoin, urlparse, urlunparse,
            urlencode, quote_plus, splitattr, splithost as urllib_splithost,
            splitpasswd, splitport, splittype, splituser, splitvalue,
            unquote, unwrap
    )
    from urllib.request import (
            pathname2url, quote, addinfourl, install_opener, build_opener,
            ProxyHandler, urlopen as _urlopen, getproxies, ftpwrapper,
            proxy_bypass as urllib_proxy_bypass, url2pathname, Request)
    from http.client import (
            HTTPMessage, parse_headers, HTTPConnection,
            HTTPSConnection)
    from http.cookiejar import (
            DEFAULT_HTTP_PORT, CookiePolicy, DefaultCookiePolicy,
            FileCookieJar, LoadError, LWPCookieJar, _debug, domain_match,
            eff_request_host, escape_path, is_HDN, lwp_cookie_str, reach,
            request_path, request_port, user_domain_match, Cookie, CookieJar,
            MozillaCookieJar, request_host)
    from io import StringIO

    def is_string(x):
        return isinstance(x, str)

    def iteritems(x):
        return x.items()

    def itervalues(x):
        return x.values()

    def is_class(obj):
        return isinstance(obj, type)

    def raise_with_traceback(exc):
        raise exc.with_traceback(sys.exc_info()[2])

    codepoint_to_chr = chr
    unicode_type = str
    map = map

    # Legacy code expects HTTPMessage.getheaders()
    def getheaders(self, name):
        return self.get_all(name, failobj=[])
    HTTPMessage.getheaders = getheaders

    # We want __getitem__ to return the last header not the first
    def getitem(self, name):
        vals = self.get_all(name, [None])
        return vals[-1]
    HTTPMessage.__getitem__ = getitem

    # Legacy method names
    HTTPMessage.gettype = HTTPMessage.get_content_type
    HTTPMessage.getmainttype = HTTPMessage.get_content_maintype
    HTTPMessage.getsubtype = HTTPMessage.get_content_subtype

    def is_mapping(x):
        return isinstance(x, collections.abc.Mapping)

    def create_response_info(fp):
        return parse_headers(fp)

    def urlopen(*a, **kw):
        proxies = kw.pop('proxies', None)
        if proxies is None:
            return _urlopen(*a, **kw)
        r = Request(a[0])
        for k, v in proxies.items():
            r.set_proxy(v, k)
        return _urlopen(r, *a[1:], **kw)


def as_unicode(x, encoding='utf-8'):
    if isinstance(x, bytes):
        x = x.decode('utf-8')
    return x


if False:
    (HTTPError, urlsplit, urljoin, urlparse, urlunparse, urlencode,
     HTTPMessage, splitattr, urllib_splithost, getproxies, ftpwrapper,
     urllib_proxy_bypass, splituser, splitpasswd, splitport,
     splitvalue, splittype, unquote, unwrap, url2pathname)
    pathname2url, RobotFileParser, URLError, quote, HTTPConnection
    HTTPSConnection, StringIO, addinfourl, install_opener, build_opener
    ProxyHandler, quote_plus, urlopen
    (DEFAULT_HTTP_PORT, CookiePolicy, DefaultCookiePolicy,
     FileCookieJar, LoadError, LWPCookieJar, _debug,
     domain_match, eff_request_host, escape_path, is_HDN,
     lwp_cookie_str, reach, request_path, request_port,
     user_domain_match, Cookie, CookieJar, MozillaCookieJar, request_host)
