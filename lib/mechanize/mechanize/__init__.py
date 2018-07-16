from __future__ import absolute_import

import logging

from ._clientcookie import request_host_lc as request_host
# cookies
from ._clientcookie import (Cookie, CookieJar, CookiePolicy,
                            DefaultCookiePolicy, FileCookieJar, LoadError,
                            LWPCookieJar, MozillaCookieJar,
                            effective_request_host, lwp_cookie_str)
# forms
from ._form_controls import (
    AmbiguityError, CheckboxControl, Control, ControlNotFoundError,
    FileControl, HiddenControl, HTMLForm, IgnoreControl, ImageControl, Item,
    ItemCountError, ItemNotFoundError, Label, ListControl, LocateError,
    Missing, PasswordControl, RadioControl, ScalarControl, SelectControl,
    SubmitButtonControl, SubmitControl, TextareaControl, TextControl)
from ._html import Factory, Link
# misc
from ._entities import html5_entities
from ._equiv import HTTPEquivParser
# high-level stateful browser-style interface
from ._mechanize import (Browser, BrowserStateError, FormNotFoundError,
                         History, LinkNotFoundError)
from ._opener import ContentTooShortError, OpenerFactory, urlretrieve
from ._response import (make_response, response_seek_wrapper,
                        seek_wrapped_response)
from ._rfc3986 import urljoin
from ._urllib2 import (
    AbstractBasicAuthHandler, AbstractDigestAuthHandler, BaseHandler,
    CacheFTPHandler, FileHandler, FTPHandler, HTTPBasicAuthHandler,
    HTTPCookieProcessor, HTTPDefaultErrorHandler, HTTPDigestAuthHandler,
    HTTPEquivProcessor, HTTPError, HTTPErrorProcessor, HTTPHandler,
    HTTPPasswordMgr, HTTPPasswordMgrWithDefaultRealm, HTTPProxyPasswordMgr,
    HTTPRedirectDebugProcessor, HTTPRedirectHandler, HTTPRefererProcessor,
    HTTPRefreshProcessor, HTTPResponseDebugProcessor, HTTPRobotRulesProcessor,
    HTTPSClientCertMgr, HTTPSHandler, OpenerDirector, ProxyBasicAuthHandler,
    ProxyDigestAuthHandler, ProxyHandler, Request, RobotExclusionError,
    SeekableResponseOpener, UnknownHandler, URLError, build_opener,
    install_opener, urlopen)
# configurable URL-opener interface
from ._useragent import UserAgent, UserAgentBase
from ._util import http2time as str2time
from ._version import __version__
from ._gzip import HTTPGzipProcessor

# If you hate the idea of turning bugs into warnings, do:
# import mechanize; mechanize.USE_BARE_EXCEPT = False
USE_BARE_EXCEPT = True

logger = logging.getLogger("mechanize")
if logger.level is logging.NOTSET:
    logger.setLevel(logging.CRITICAL)
del logger
__all__ = [
    'AbstractBasicAuthHandler',
    'AbstractDigestAuthHandler',
    'BaseHandler',
    'Browser',
    'BrowserStateError',
    'CacheFTPHandler',
    'ContentTooShortError',
    'Cookie',
    'CookieJar',
    'CookiePolicy',
    'DefaultCookiePolicy',
    'effective_request_host',
    'FTPHandler',
    'Factory',
    'FileCookieJar',
    'FileHandler',
    'FormNotFoundError',
    'HTTPBasicAuthHandler',
    'HTTPCookieProcessor',
    'HTTPDefaultErrorHandler',
    'HTTPDigestAuthHandler',
    'HTTPEquivProcessor',
    'HTTPError',
    'HTTPErrorProcessor',
    'HTTPGzipProcessor',
    'HTTPHandler',
    'HTTPSHandler',
    'HTTPPasswordMgr',
    'HTTPPasswordMgrWithDefaultRealm',
    'HTTPProxyPasswordMgr',
    'HTTPRedirectDebugProcessor',
    'HTTPRedirectHandler',
    'HTTPRefererProcessor',
    'HTTPRefreshProcessor',
    'HTTPResponseDebugProcessor',
    'HTTPRobotRulesProcessor',
    'HTTPSClientCertMgr',
    'History',
    'LWPCookieJar',
    'Link',
    'LinkNotFoundError',
    'LoadError',
    'MozillaCookieJar',
    'OpenerDirector',
    'OpenerFactory',
    'ProxyBasicAuthHandler',
    'ProxyDigestAuthHandler',
    'ProxyHandler',
    'Request',
    'RobotExclusionError',
    'SeekableResponseOpener',
    'URLError',
    'USE_BARE_EXCEPT',
    'UnknownHandler',
    'UserAgent',
    'UserAgentBase',
    'HTTPEquivParser',
    'html5_entities',
    '__version__',
    'build_opener',
    'install_opener',
    'lwp_cookie_str',
    'make_response',
    'request_host',
    'response_seek_wrapper',  # XXX deprecate in public interface?
    # XXX should probably use this internally in place of
    # response_seek_wrapper()
    'seek_wrapped_response',
    'str2time',
    'urlopen',
    'urlretrieve',
    'urljoin',

    # ClientForm API
    'AmbiguityError',
    'ControlNotFoundError',
    'ItemCountError',
    'ItemNotFoundError',
    'LocateError',
    'Missing',
    # deprecated
    'CheckboxControl',
    'Control',
    'FileControl',
    'HTMLForm',
    'HiddenControl',
    'IgnoreControl',
    'ImageControl',
    'Item',
    'Label',
    'ListControl',
    'PasswordControl',
    'RadioControl',
    'ScalarControl',
    'SelectControl',
    'SubmitButtonControl',
    'SubmitControl',
    'TextControl',
    'TextareaControl',
]
