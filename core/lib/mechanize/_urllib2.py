from __future__ import absolute_import
# urllib2 work-alike interface
# ...from urllib2...
from .polyglot import HTTPError, URLError

# ...and from mechanize
from ._auth import HTTPProxyPasswordMgr, HTTPSClientCertMgr
from ._debug import HTTPRedirectDebugProcessor, HTTPResponseDebugProcessor
from ._http import (HTTPEquivProcessor, HTTPRefererProcessor,
                    HTTPRefreshProcessor, HTTPRobotRulesProcessor,
                    RobotExclusionError)
from ._opener import (OpenerDirector, SeekableResponseOpener, build_opener,
                      install_opener, urlopen)
from ._request import Request
# crap ATM
# from _gzip import \
# HTTPGzipProcessor
from ._urllib2_fork import (
    AbstractBasicAuthHandler, AbstractDigestAuthHandler, BaseHandler,
    CacheFTPHandler, FileHandler, FTPHandler, HTTPBasicAuthHandler,
    HTTPCookieProcessor, HTTPDefaultErrorHandler, HTTPDigestAuthHandler,
    HTTPErrorProcessor, HTTPHandler, HTTPPasswordMgr,
    HTTPPasswordMgrWithDefaultRealm, HTTPRedirectHandler, HTTPSHandler,
    ProxyBasicAuthHandler, ProxyDigestAuthHandler, ProxyHandler,
    UnknownHandler)
__all__ = [
    'URLError',
    'HTTPError',
    'HTTPSClientCertMgr',
    'HTTPProxyPasswordMgr',
    'HTTPRedirectDebugProcessor',
    'HTTPRobotRulesProcessor',
    'HTTPResponseDebugProcessor',
    'HTTPRefreshProcessor',
    'HTTPRefererProcessor',
    'HTTPEquivProcessor',
    'RobotExclusionError',
    'OpenerDirector',
    'build_opener',
    'SeekableResponseOpener',
    'install_opener',
    'urlopen',
    'Request',
    'HTTPHandler',
    'HTTPSHandler',
    'AbstractBasicAuthHandler',
    'ProxyHandler',
    'HTTPDefaultErrorHandler',
    'ProxyDigestAuthHandler',
    'HTTPDigestAuthHandler',
    'FTPHandler',
    'HTTPPasswordMgrWithDefaultRealm',
    'CacheFTPHandler',
    'HTTPErrorProcessor',
    'AbstractDigestAuthHandler',
    'HTTPRedirectHandler',
    'UnknownHandler',
    'HTTPCookieProcessor',
    'BaseHandler',
    'HTTPBasicAuthHandler',
    'ProxyBasicAuthHandler',
    'HTTPPasswordMgr',
    'FileHandler',
]
