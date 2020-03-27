"""Convenient HTTP UserAgent class.

This is a subclass of urllib2.OpenerDirector.


Copyright 2003-2006 John J. Lee <jjl@pobox.com>

This code is free software; you can redistribute it and/or modify it under
the terms of the BSD or ZPL 2.1 licenses (see the file LICENSE
included with the distribution).

"""

from __future__ import absolute_import

import copy

from . import _auth, _gzip, _opener, _response, _sockettimeout, _urllib2
from .polyglot import iteritems, itervalues


class UserAgentBase(_opener.OpenerDirector):
    """Convenient user-agent class.

    Do not use .add_handler() to add a handler for something already dealt with
    by this code.

    The only reason at present for the distinction between UserAgent and
    UserAgentBase is so that classes that depend on .seek()able responses
    (e.g. mechanize.Browser) can inherit from UserAgentBase.  The subclass
    UserAgent exposes a .set_seekable_responses() method that allows switching
    off the adding of a .seek() method to responses.

    Public attributes:

    addheaders: list of (name, value) pairs specifying headers to send with
     every request, unless they are overridden in the Request instance.

     >>> ua = UserAgentBase()
     >>> ua.addheaders = [
     ...  ("User-agent", "Mozilla/5.0 (compatible)"),
     ...  ("From", "responsible.person@example.com")]

    """

    handler_classes = {
        # scheme handlers
        "http": _urllib2.HTTPHandler,
        # CacheFTPHandler is buggy, at least in 2.3, so we don't use it
        "ftp": _urllib2.FTPHandler,
        "file": _urllib2.FileHandler,

        # other handlers
        "_unknown": _urllib2.UnknownHandler,
        # HTTP{S,}Handler depend on HTTPErrorProcessor too
        "_http_error": _urllib2.HTTPErrorProcessor,
        "_http_default_error": _urllib2.HTTPDefaultErrorHandler,

        # feature handlers
        "_basicauth": _urllib2.HTTPBasicAuthHandler,
        "_digestauth": _urllib2.HTTPDigestAuthHandler,
        "_redirect": _urllib2.HTTPRedirectHandler,
        "_cookies": _urllib2.HTTPCookieProcessor,
        "_refresh": _urllib2.HTTPRefreshProcessor,
        "_equiv": _urllib2.HTTPEquivProcessor,
        "_proxy": _urllib2.ProxyHandler,
        "_proxy_basicauth": _urllib2.ProxyBasicAuthHandler,
        "_proxy_digestauth": _urllib2.ProxyDigestAuthHandler,
        "_robots": _urllib2.HTTPRobotRulesProcessor,
        "_gzip": _gzip.HTTPGzipProcessor,

        # debug handlers
        "_debug_redirect": _urllib2.HTTPRedirectDebugProcessor,
        "_debug_response_body": _urllib2.HTTPResponseDebugProcessor,
    }

    default_schemes = ["http", "ftp", "file"]
    default_others = ["_unknown", "_http_error", "_http_default_error"]
    default_features = [
        "_gzip",
        "_redirect",
        "_cookies",
        "_refresh",
        "_equiv",
        "_basicauth",
        "_digestauth",
        "_proxy",
        "_proxy_basicauth",
        "_proxy_digestauth",
        "_robots",
    ]
    if hasattr(_urllib2, 'HTTPSHandler'):
        handler_classes["https"] = _urllib2.HTTPSHandler
        default_schemes.append("https")

    def __init__(self):
        _opener.OpenerDirector.__init__(self)

        ua_handlers = self._ua_handlers = {}
        for scheme in (self.default_schemes + self.default_others +
                       self.default_features):
            klass = self.handler_classes[scheme]
            ua_handlers[scheme] = klass()
        for handler in tuple(itervalues(ua_handlers)):
            self.add_handler(handler)

        # Yuck.
        # Ensure correct default constructor args were passed to
        # HTTPRefreshProcessor and HTTPEquivProcessor.
        if "_refresh" in ua_handlers:
            self.set_handle_refresh(True)
        if "_equiv" in ua_handlers:
            self.set_handle_equiv(True)
        # Ensure default password managers are installed.
        pm = ppm = None
        if "_basicauth" in ua_handlers or "_digestauth" in ua_handlers:
            pm = _urllib2.HTTPPasswordMgrWithDefaultRealm()
        if ("_proxy_basicauth" in ua_handlers or
                "_proxy_digestauth" in ua_handlers):
            ppm = _auth.HTTPProxyPasswordMgr()
        self.set_password_manager(pm)
        self.set_proxy_password_manager(ppm)
        # set default certificate manager
        if "https" in ua_handlers:
            cm = _urllib2.HTTPSClientCertMgr()
            self.set_client_cert_manager(cm)

    def close(self):
        _opener.OpenerDirector.close(self)
        self._ua_handlers = None

# XXX
# def set_timeout(self, timeout):
#         self._timeout = timeout
# def set_http_connection_cache(self, conn_cache):
#         self._http_conn_cache = conn_cache
# def set_ftp_connection_cache(self, conn_cache):
# XXX ATM, FTP has cache as part of handler; should it be separate?
#         self._ftp_conn_cache = conn_cache

    def set_handled_schemes(self, schemes):
        """Set sequence of URL scheme (protocol) strings.

        For example: ua.set_handled_schemes(["http", "ftp"])

        If this fails (with ValueError) because you've passed an unknown
        scheme, the set of handled schemes will not be changed.

        """
        want = {}
        for scheme in schemes:
            if scheme.startswith("_"):
                raise ValueError("not a scheme '%s'" % scheme)
            if scheme not in self.handler_classes:
                raise ValueError("unknown scheme '%s'")
            want[scheme] = None

        # get rid of scheme handlers we don't want
        for scheme, oldhandler in tuple(iteritems(self._ua_handlers)):
            if scheme.startswith("_"):
                continue  # not a scheme handler
            if scheme not in want:
                self._replace_handler(scheme, None)
            else:
                del want[scheme]  # already got it
        # add the scheme handlers that are missing
        for scheme in want:
            self._set_handler(scheme, True)

    def set_cookiejar(self, cookiejar):
        """Set a mechanize.CookieJar, or None."""
        self._set_handler("_cookies", obj=cookiejar)

    # XXX could use Greg Stein's httpx for some of this instead?
    # or httplib2??
    def set_proxies(self, proxies=None, proxy_bypass=None):
        """Configure proxy settings.

        :arg proxies: dictionary mapping URL scheme to proxy specification.
          None means use the default system-specific settings.
        :arg proxy_bypass: function taking hostname, returning whether proxy
          should be used.  None means use the default system-specific settings.

        The default is to try to obtain proxy settings from the system (see the
        documentation for urllib.urlopen for information about the
        system-specific methods used -- note that's urllib, not urllib2).

        To avoid all use of proxies, pass an empty proxies dict.

        >>> ua = UserAgentBase()
        >>> def proxy_bypass(hostname):
        ...     return hostname == "noproxy.com"
        >>> ua.set_proxies(
        ...     {"http": "joe:password@myproxy.example.com:3128",
        ...      "ftp": "proxy.example.com"},
        ...     proxy_bypass)

        """
        self._set_handler(
            "_proxy",
            True,
            constructor_kwds=dict(proxies=proxies, proxy_bypass=proxy_bypass))

    def add_password(self, url, user, password, realm=None):
        self._password_manager.add_password(realm, url, user, password)

    def add_proxy_password(self, user, password, hostport=None, realm=None):
        self._proxy_password_manager.add_password(realm, hostport, user,
                                                  password)

    def add_client_certificate(self, url, key_file, cert_file):
        """Add an SSL client certificate, for HTTPS client auth.

        key_file and cert_file must be filenames of the key and certificate
        files, in PEM format.  You can use e.g. OpenSSL to convert a p12 (PKCS
        12) file to PEM format:

        openssl pkcs12 -clcerts -nokeys -in cert.p12 -out cert.pem
        openssl pkcs12 -nocerts -in cert.p12 -out key.pem


        Note that client certificate password input is very inflexible ATM.  At
        the moment this seems to be console only, which is presumably the
        default behaviour of libopenssl.  In future mechanize may support
        third-party libraries that (I assume) allow more options here.

        """
        self._client_cert_manager.add_key_cert(url, key_file, cert_file)

    # the following are rarely useful -- use add_password / add_proxy_password
    # instead
    def set_password_manager(self, password_manager):
        """Set a mechanize.HTTPPasswordMgrWithDefaultRealm, or None."""
        self._password_manager = password_manager
        self._set_handler("_basicauth", obj=password_manager)
        self._set_handler("_digestauth", obj=password_manager)

    def set_proxy_password_manager(self, password_manager):
        """Set a mechanize.HTTPProxyPasswordMgr, or None."""
        self._proxy_password_manager = password_manager
        self._set_handler("_proxy_basicauth", obj=password_manager)
        self._set_handler("_proxy_digestauth", obj=password_manager)

    def set_client_cert_manager(self, cert_manager):
        """Set a mechanize.HTTPClientCertMgr, or None."""
        handler = self._ua_handlers["https"]
        self._client_cert_manager = handler.client_cert_manager = cert_manager

    def set_ca_data(self, cafile=None, capath=None, cadata=None, context=None):
        '''
        Set the SSL Context used for connecting to SSL servers.

        This method accepts the same arguments as the
        :py:meth:`ssl.SSLContext.load_verify_locations()` method from the
        python standard library. You can also pass a pre-built context via the
        `context` keyword argument. Note that to use this feature, you must be
        using python >= 2.7.9. In addition you can directly pass in
        a pre-built :class:`ssl.SSLContext` as the `context` argument.

        '''
        import ssl
        if context is None:
            try:
                context = ssl.create_default_context(
                    cafile=cafile, capath=capath, cadata=cadata)
            except AttributeError:
                raise RuntimeError('python >= 2.7.9 required')
        handler = self._ua_handlers["https"]
        handler.ssl_context = context

    # these methods all take a boolean parameter
    def set_handle_robots(self, handle):
        """Set whether to observe rules from robots.txt."""
        self._set_handler("_robots", handle)

    def set_handle_redirect(self, handle):
        """Set whether to handle HTTP 30x redirections."""
        self._set_handler("_redirect", handle)

    def set_handle_refresh(self, handle, max_time=None, honor_time=True):
        """Set whether to handle HTTP Refresh headers."""
        self._set_handler(
            "_refresh",
            handle,
            constructor_kwds={"max_time": max_time,
                              "honor_time": honor_time})

    def set_handle_equiv(self, handle, head_parser_class=None):
        """Set whether to treat HTML http-equiv headers like HTTP headers.

        Response objects may be .seek()able if this is set (currently returned
        responses are, raised HTTPError exception responses are not).

        """
        if head_parser_class is not None:
            constructor_kwds = {"head_parser_class": head_parser_class}
        else:
            constructor_kwds = {}
        self._set_handler("_equiv", handle, constructor_kwds=constructor_kwds)

    def set_request_gzip(self, handle):
        """Add header indicating to server that we handle gzip
        content encoding. Note that if the server sends gzip'ed content,
        it is handled automatically in any case, regardless of this setting.

        """
        self._set_handler(
            "_gzip", True, constructor_kwds={'request_gzip': bool(handle)})
    set_handle_gzip = set_request_gzip  # legacy

    def set_debug_redirects(self, handle):
        """
        Log information about HTTP redirects (including refreshes).

        Logging is performed using module logging.  The logger name is
        `"mechanize.http_redirects"`.  To actually print some debug output,
        eg:

        .. code-block:: python

            import sys, logging
            logger = logging.getLogger("mechanize.http_redirects")
            logger.addHandler(logging.StreamHandler(sys.stdout))
            logger.setLevel(logging.INFO)

        Other logger names relevant to this module:

        * `mechanize.http_responses`
        * `mechanize.cookies`

        To turn on everything:

        .. code-block:: python

            import sys, logging
            logger = logging.getLogger("mechanize")
            logger.addHandler(logging.StreamHandler(sys.stdout))
            logger.setLevel(logging.INFO)

        """
        self._set_handler("_debug_redirect", handle)

    def set_debug_responses(self, handle):
        """Log HTTP response bodies.

        See :meth:`set_debug_redirects()` for details of logging.

        Response objects may be .seek()able if this is set (currently returned
        responses are, raised HTTPError exception responses are not).

        """
        self._set_handler("_debug_response_body", handle)

    def set_debug_http(self, handle):
        """Print HTTP headers to sys.stdout."""
        level = int(bool(handle))
        for scheme in "http", "https":
            h = self._ua_handlers.get(scheme)
            if h is not None:
                h.set_http_debuglevel(level)

    def _copy_state(self, other):
        if self._ua_handlers is None:
            raise ValueError('Cannot copy state from a closed UserAgentBase')
        other.addheaders = self.addheaders[:]
        rmap = {v: k for k, v in iteritems(self._ua_handlers)}

        def clone_handler(h):
            ans = copy.copy(h)
            ans.add_parent(other)
            try:
                other._ua_handlers[rmap[h]] = ans
            except KeyError:
                pass
            return ans

        other._ua_handlers.clear()
        other.handlers = [clone_handler(h) for h in self.handlers]
        other._handler_index_valid = False

    def handlers_by_class(self, cls):
        for h in self.handlers:
            if isinstance(h, cls):
                yield h

    def _set_handler(self,
                     name,
                     handle=None,
                     obj=None,
                     constructor_args=(),
                     constructor_kwds={}):
        if handle is None:
            handle = obj is not None
        if handle:
            handler_class = self.handler_classes[name]
            if obj is not None:
                newhandler = handler_class(obj)
            else:
                newhandler = handler_class(*constructor_args,
                                           **constructor_kwds)
        else:
            newhandler = None
        self._replace_handler(name, newhandler)

    def _replace_handler(self, name, newhandler=None):
        # first, if handler was previously added, remove it
        if name is not None:
            handler = self._ua_handlers.pop(name, None)
            if handler is not None:
                try:
                    self.handlers.remove(handler)
                except ValueError:
                    pass
        # then add the replacement, if any
        if newhandler is not None:
            self.add_handler(newhandler)
            self._ua_handlers[name] = newhandler


class UserAgent(UserAgentBase):
    def __init__(self):
        UserAgentBase.__init__(self)
        self._seekable = False

    def set_seekable_responses(self, handle):
        """Make response objects .seek()able."""
        self._seekable = bool(handle)

    def open(self,
             fullurl,
             data=None,
             timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        if self._seekable:

            def bound_open(fullurl,
                           data=None,
                           timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
                return UserAgentBase.open(self, fullurl, data, timeout)

            response = _opener.wrapped_open(bound_open,
                                            _response.seek_wrapped_response,
                                            fullurl, data, timeout)
        else:
            response = UserAgentBase.open(self, fullurl, data)
        return response
