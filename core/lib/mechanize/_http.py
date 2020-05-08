"""HTTP related handlers.

Note that some other HTTP handlers live in more specific modules: _auth.py,
_gzip.py, etc.


Copyright 2002-2006 John J Lee <jjl@pobox.com>

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD or ZPL 2.1 licenses (see the file
LICENSE included with the distribution).

"""

from __future__ import absolute_import

import logging
import socket
import time
from io import BytesIO

from . import _rfc3986, _sockettimeout
from ._headersutil import is_html
from ._request import Request
from ._response import response_seek_wrapper
from ._urllib2_fork import BaseHandler, HTTPError
from ._equiv import HTTPEquivParser
from .polyglot import create_response_info, RobotFileParser, is_py2, as_unicode

debug = logging.getLogger("mechanize").debug
debug_robots = logging.getLogger("mechanize.robots").debug


def parse_head(fileobj):
    """Return a list of key, value pairs."""
    p = HTTPEquivParser(fileobj.read(4096))
    return p()


class HTTPEquivProcessor(BaseHandler):
    """Append META HTTP-EQUIV headers to regular HTTP headers."""

    handler_order = 300  # before handlers that look at HTTP headers

    def http_response(self, request, response):
        if not hasattr(response, "seek"):
            response = response_seek_wrapper(response)
        http_message = response.info()
        url = response.geturl()
        ct_hdrs = http_message.getheaders("content-type")
        if is_html(ct_hdrs, url, True):
            try:
                try:
                    html_headers = parse_head(response)
                finally:
                    response.seek(0)
            except Exception:
                pass
            else:
                for hdr, val in html_headers:
                    if is_py2:
                        # add a header
                        http_message.dict[hdr.lower()] = val
                        text = hdr + b": " + val
                        for line in text.split(b"\n"):
                            http_message.headers.append(line + b"\n")
                    else:
                        hdr = hdr.decode('iso-8859-1')
                        http_message[hdr] = val.decode('iso-8859-1')
        return response

    https_response = http_response


class MechanizeRobotFileParser(RobotFileParser):

    def __init__(self, url='', opener=None):
        RobotFileParser.__init__(self, url)
        self._opener = opener
        self._timeout = _sockettimeout._GLOBAL_DEFAULT_TIMEOUT

    def set_opener(self, opener=None):
        from . import _opener
        if opener is None:
            opener = _opener.OpenerDirector()
        self._opener = opener

    def set_timeout(self, timeout):
        self._timeout = timeout

    def read(self):
        """Reads the robots.txt URL and feeds it to the parser."""
        if self._opener is None:
            self.set_opener()
        req = Request(self.url, unverifiable=True, visit=False,
                      timeout=self._timeout)
        try:
            f = self._opener.open(req)
        except HTTPError as err:
            f = err
        except (IOError, socket.error, OSError) as exc:
            debug_robots("ignoring error opening %r: %s" %
                         (self.url, exc))
            return
        lines = []
        line = f.readline()
        while line:
            lines.append(line.strip())
            line = f.readline()
        status = f.code
        if status == 401 or status == 403:
            self.disallow_all = True
            debug_robots("disallow all")
        elif status >= 400:
            self.allow_all = True
            debug_robots("allow all")
        elif status == 200 and lines:
            debug_robots("parse lines")
            if is_py2:
                self.parse(lines)
            else:
                self.parse(map(as_unicode, lines))


class RobotExclusionError(HTTPError):

    def __init__(self, request, *args):
        HTTPError.__init__(self, *args)
        self.request = request


class HTTPRobotRulesProcessor(BaseHandler):
    # before redirections, after everything else
    handler_order = 800
    http_response_class = None

    def __init__(self, rfp_class=MechanizeRobotFileParser):
        self.rfp_class = rfp_class
        self.rfp = None
        self._host = None

    def __copy__(self):
        return self.__class__(self.rfp_class)

    def http_request(self, request):
        scheme = request.get_type()
        if scheme not in ["http", "https"]:
            # robots exclusion only applies to HTTP
            return request

        if request.get_selector() == "/robots.txt":
            # /robots.txt is always OK to fetch
            return request

        host = request.get_host()

        # robots.txt requests don't need to be allowed by robots.txt :-)
        origin_req = getattr(request, "_origin_req", None)
        if (origin_req is not None and
                origin_req.get_selector() == "/robots.txt" and
                origin_req.get_host() == host):
            return request

        if host != self._host:
            self.rfp = self.rfp_class()
            try:
                self.rfp.set_opener(self.parent)
            except AttributeError:
                debug("%r instance does not support set_opener" %
                      self.rfp.__class__)
            self.rfp.set_url(scheme + "://" + host + "/robots.txt")
            self.rfp.set_timeout(request.timeout)
            self.rfp.read()
            self._host = host

        ua = request.get_header("User-agent", "")
        if self.rfp.can_fetch(ua, request.get_full_url()):
            return request
        else:
            # XXX This should really have raised URLError.  Too late now...
            factory = self.http_response_class or create_response_info
            msg = b"request disallowed by robots.txt"
            raise RobotExclusionError(
                request,
                request.get_full_url(),
                403, msg,
                factory(BytesIO()), BytesIO(msg))

    https_request = http_request


class HTTPRefererProcessor(BaseHandler):
    """Add Referer header to requests.

    This only makes sense if you use each RefererProcessor for a single
    chain of requests only (so, for example, if you use a single
    HTTPRefererProcessor to fetch a series of URLs extracted from a single
    page, this will break).

    There's a proper implementation of this in mechanize.Browser.

    """

    def __init__(self):
        self.referer = None

    def http_request(self, request):
        if ((self.referer is not None) and
                not request.has_header("Referer")):
            request.add_unredirected_header("Referer", self.referer)
        return request

    def http_response(self, request, response):
        self.referer = response.geturl()
        return response

    https_request = http_request
    https_response = http_response


def clean_refresh_url(url):
    # e.g. Firefox 1.5 does (something like) this
    if ((url.startswith('"') and url.endswith('"')) or
            (url.startswith("'") and url.endswith("'"))):
        url = url[1:-1]
    return _rfc3986.clean_url(url, 'utf-8')  # XXX encoding


def parse_refresh_header(refresh):
    """
    >>> parse_refresh_header("1; url=http://example.com/")
    (1.0, 'http://example.com/')
    >>> parse_refresh_header("1; url='http://example.com/'")
    (1.0, 'http://example.com/')
    >>> parse_refresh_header("1")
    (1.0, None)
    >>> parse_refresh_header("blah")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: invalid literal for float(): blah

    """

    ii = refresh.find(";")
    if ii != -1:
        pause, newurl_spec = float(refresh[:ii]), refresh[ii + 1:]
        jj = newurl_spec.find("=")
        key = None
        if jj != -1:
            key, newurl = newurl_spec[:jj], newurl_spec[jj + 1:]
            newurl = clean_refresh_url(newurl)
        if key is None or key.strip().lower() != "url":
            raise ValueError()
    else:
        pause, newurl = float(refresh), None
    return pause, newurl


class HTTPRefreshProcessor(BaseHandler):
    """Perform HTTP Refresh redirections.

    Note that if a non-200 HTTP code has occurred (for example, a 30x
    redirect), this processor will do nothing.

    By default, only zero-time Refresh headers are redirected.  Use the
    max_time attribute / constructor argument to allow Refresh with longer
    pauses.  Use the honor_time attribute / constructor argument to control
    whether the requested pause is honoured (with a time.sleep()) or
    skipped in favour of immediate redirection.

    Public attributes:

    max_time: see above
    honor_time: see above

    """
    handler_order = 1000

    def __init__(self, max_time=0, honor_time=True):
        self.max_time = max_time
        self.honor_time = honor_time
        self._sleep = time.sleep

    def __copy__(self):
        return self.__class__(self.max_time, self.honor_time)

    def http_response(self, request, response):
        code, msg, hdrs = response.code, response.msg, response.info()

        if code == 200 and 'refresh' in hdrs:
            refresh = hdrs.getheaders("refresh")[0]
            try:
                pause, newurl = parse_refresh_header(refresh)
            except ValueError:
                debug("bad Refresh header: %r" % refresh)
                return response

            if newurl is None:
                newurl = response.geturl()
            if (self.max_time is None) or (pause <= self.max_time):
                if pause > 1E-3 and self.honor_time:
                    self._sleep(pause)
                hdrs["location"] = newurl
                # hardcoded http is NOT a bug
                response = self.parent.error(
                    "http", request, response,
                    "refresh", msg, hdrs)
            else:
                debug("Refresh header ignored: %r" % refresh)

        return response

    https_response = http_response
