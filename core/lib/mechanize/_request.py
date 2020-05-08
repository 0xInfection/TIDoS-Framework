"""Integration with Python standard library module urllib2: Request class.

Copyright 2004-2006 John J Lee <jjl@pobox.com>

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD or ZPL 2.1 licenses (see the file
LICENSE included with the distribution).

"""

from __future__ import absolute_import
import logging

from . import _rfc3986
from . import _sockettimeout
from . import _urllib2_fork
from .polyglot import urlencode, is_string, unicode_type, iteritems

warn = logging.getLogger("mechanize").warning


def as_utf8(x):
    if isinstance(x, bytes):
        return x
    if not is_string(x):
        x = unicode_type(x)
    if isinstance(x, unicode_type):
        x = x.encode('utf-8')
    return x


class Request(_urllib2_fork.Request):

    '''
    A request for some network resource. Note that if you specify the method as
    'GET' and the data as a dict, then it will be automatically appended to the
    URL. If you leave method as None, then the method will be auto-set to
    POST and the data will become part of the POST request.

    :arg str url: The URL to request
    :arg data: Data to send with this request. Can be either a dictionary
        which will be encoded and sent as application/x-www-form-urlencoded
        data or a bytestring which will be sent as is. If you use a bytestring
        you should also set the Content-Type header appropriately.
    :arg dict headers: Headers to send with this request
    :arg str method: Method to use for HTTP requests. If not specified
        mechanize will choose GET or POST automatically as appropriate.
    :arg float timeout: Timeout in seconds

    The remaining arguments are for internal use.
    '''

    def __init__(self, url, data=None, headers={},
                 origin_req_host=None, unverifiable=False, visit=None,
                 timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT,
                 method=None):
        # In mechanize 0.2, the interpretation of a unicode url argument will
        # change: A unicode url argument will be interpreted as an IRI, and a
        # bytestring as a URI. For now, we accept unicode or bytestring.  We
        # don't insist that the value is always a URI (specifically, must only
        # contain characters which are legal), because that might break working
        # code (who knows what bytes some servers want to see, especially with
        # browser plugins for internationalised URIs).
        if not _rfc3986.is_clean_uri(url):
            warn("url argument is not a URI "
                 "(contains illegal characters) %r" % url)
        if isinstance(data, dict):
            data = {as_utf8(k): as_utf8(v) for k, v in iteritems(data)}
            data = urlencode(data)
            data = data or None
            if data and method == 'GET':
                url += ('&' if '?' in url else '?') + data
                data = None
        _urllib2_fork.Request.__init__(self, url, data, headers, method=method)
        self.selector = None
        self.visit = visit
        self.timeout = timeout

    def __str__(self):
        return "<Request for %s>" % self.get_full_url()
