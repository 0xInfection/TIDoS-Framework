"""Tests for urllib2-level functionality.

This is urllib2's tests (most of which came from mechanize originally), plus
some extra tests added, and modifications from bug fixes and feature additions
to mechanize.
"""

# TODO:
# Request
# CacheFTPHandler (hard to write)
# parse_keqv_list, parse_http_list

import StringIO
import httplib
import os
import sys
import unittest

import mechanize

from mechanize._http import parse_head
from mechanize._response import test_response
from mechanize import HTTPRedirectHandler, \
    HTTPEquivProcessor, HTTPRefreshProcessor, \
    HTTPCookieProcessor, HTTPRefererProcessor, \
    HTTPErrorProcessor, HTTPHandler
from mechanize import OpenerDirector, build_opener, Request
from mechanize._urllib2_fork import AbstractHTTPHandler
from mechanize._util import write_file

import mechanize._response
import mechanize._sockettimeout as _sockettimeout
import mechanize._testcase
import mechanize._urllib2_fork
from mechanize._mechanize import sanepathname2url

## from logging import getLogger, DEBUG
## l = getLogger("mechanize")
# l.setLevel(DEBUG)


class AlwaysEqual:
    def __cmp__(self, other):
        return 0


class TrivialTests(mechanize._testcase.TestCase):
    def test_trivial(self):
        # A couple trivial tests

        self.assertRaises(ValueError, mechanize.urlopen, 'bogus url')

        fname = os.path.join(self.make_temp_dir(), "test.txt")
        write_file(fname, "data")
        if fname[1:2] == ":":
            fname = fname[2:]
        # And more hacking to get it to work on MacOS. This assumes
        # urllib.pathname2url works, unfortunately...
        if os.name == 'mac':
            fname = '/' + fname.replace(':', '/')
        elif os.name == 'riscos':
            import string
            fname = os.expand(fname)
            fname = fname.translate(string.maketrans("/.", "./"))

        file_url = "file://%s" % sanepathname2url(fname)
        f = mechanize.urlopen(file_url)

        buf = f.read()
        f.close()

    def test_parse_http_list(self):
        tests = [('a,b,c', ['a', 'b', 'c']), (
            'path"o,l"og"i"cal, example', ['path"o,l"og"i"cal', 'example']),
                 ('a, b, "c", "d", "e,f", g, h',
                  ['a', 'b', '"c"', '"d"', '"e,f"', 'g',
                   'h']), ('a="b\\"c", d="e\\,f", g="h\\\\i"',
                           ['a="b"c"', 'd="e,f"', 'g="h\\i"'])]
        for string, list in tests:
            self.assertEquals(
                mechanize._urllib2_fork.parse_http_list(string), list)


def test_request_headers_dict():
    """
    The Request.headers dictionary is not a documented interface.  It should
    stay that way, because the complete set of headers are only accessible
    through the .get_header(), .has_header(), .header_items() interface.
    However, .headers pre-dates those methods, and so real code will be using
    the dictionary.

    The introduction in 2.4 of those methods was a mistake for the same reason:
    code that previously saw all (urllib2 user)-provided headers in .headers
    now sees only a subset (and the function interface is ugly and incomplete).
    A better change would have been to replace .headers dict with a dict
    subclass (or UserDict.DictMixin instance?)  that preserved the .headers
    interface and also provided access to the "unredirected" headers.  It's
    probably too late to fix that, though.


    Check .capitalize() case normalization:

    >>> url = "http://example.com"
    >>> Request(url, headers={"Spam-eggs": "blah"}).headers["Spam-eggs"]
    'blah'
    >>> Request(url, headers={"spam-EggS": "blah"}).headers["Spam-eggs"]
    'blah'

    Currently, Request(url, "Spam-eggs").headers["Spam-Eggs"] raises KeyError,
    but that could be changed in future.

    """


def test_request_headers_methods():
    """
    Note the case normalization of header names here, to .capitalize()-case.
    This should be preserved for backwards-compatibility.  (In the HTTP case,
    normalization to .title()-case is done by urllib2 before sending headers to
    httplib).

    >>> url = "http://example.com"
    >>> r = Request(url, headers={"Spam-eggs": "blah"})
    >>> r.has_header("Spam-eggs")
    True
    >>> r.header_items()
    [('Spam-eggs', 'blah')]
    >>> r.add_header("Foo-Bar", "baz")
    >>> items = r.header_items()
    >>> items.sort()
    >>> items
    [('Foo-bar', 'baz'), ('Spam-eggs', 'blah')]

    Note that e.g. r.has_header("spam-EggS") is currently False, and
    r.get_header("spam-EggS") returns None, but that could be changed in
    future.

    >>> r.has_header("Not-there")
    False
    >>> print r.get_header("Not-there")
    None
    >>> r.get_header("Not-there", "default")
    'default'

    """


def test_password_manager(self):
    """
    >>> mgr = mechanize.HTTPPasswordMgr()
    >>> add = mgr.add_password
    >>> add("Some Realm", "http://example.com/", "joe", "password")
    >>> add("Some Realm", "http://example.com/ni", "ni", "ni")
    >>> add("c", "http://example.com/foo", "foo", "ni")
    >>> add("c", "http://example.com/bar", "bar", "nini")
    >>> add("b", "http://example.com/", "first", "blah")
    >>> add("b", "http://example.com/", "second", "spam")
    >>> add("a", "http://example.com", "1", "a")
    >>> add("Some Realm", "http://c.example.com:3128", "3", "c")
    >>> add("Some Realm", "d.example.com", "4", "d")
    >>> add("Some Realm", "e.example.com:3128", "5", "e")

    >>> mgr.find_user_password("Some Realm", "example.com")
    ('joe', 'password')
    >>> mgr.find_user_password("Some Realm", "http://example.com")
    ('joe', 'password')
    >>> mgr.find_user_password("Some Realm", "http://example.com/")
    ('joe', 'password')
    >>> mgr.find_user_password("Some Realm", "http://example.com/spam")
    ('joe', 'password')
    >>> mgr.find_user_password("Some Realm", "http://example.com/spam/spam")
    ('joe', 'password')
    >>> mgr.find_user_password("c", "http://example.com/foo")
    ('foo', 'ni')
    >>> mgr.find_user_password("c", "http://example.com/bar")
    ('bar', 'nini')

    Actually, this is really undefined ATM
##     Currently, we use the highest-level path where more than one match:

##     >>> mgr.find_user_password("Some Realm", "http://example.com/ni")
##     ('joe', 'password')

    Use latest add_password() in case of conflict:

    >>> mgr.find_user_password("b", "http://example.com/")
    ('second', 'spam')

    No special relationship between a.example.com and example.com:

    >>> mgr.find_user_password("a", "http://example.com/")
    ('1', 'a')
    >>> mgr.find_user_password("a", "http://a.example.com/")
    (None, None)

    Ports:

    >>> mgr.find_user_password("Some Realm", "c.example.com")
    (None, None)
    >>> mgr.find_user_password("Some Realm", "c.example.com:3128")
    ('3', 'c')
    >>> mgr.find_user_password("Some Realm", "http://c.example.com:3128")
    ('3', 'c')
    >>> mgr.find_user_password("Some Realm", "d.example.com")
    ('4', 'd')
    >>> mgr.find_user_password("Some Realm", "e.example.com:3128")
    ('5', 'e')

    """
    pass


def test_password_manager_default_port(self):
    """
    >>> mgr = mechanize.HTTPPasswordMgr()
    >>> add = mgr.add_password

    The point to note here is that we can't guess the default port if there's
    no scheme.  This applies to both add_password and find_user_password.

    >>> add("f", "http://g.example.com:80", "10", "j")
    >>> add("g", "http://h.example.com", "11", "k")
    >>> add("h", "i.example.com:80", "12", "l")
    >>> add("i", "j.example.com", "13", "m")
    >>> mgr.find_user_password("f", "g.example.com:100")
    (None, None)
    >>> mgr.find_user_password("f", "g.example.com:80")
    ('10', 'j')
    >>> mgr.find_user_password("f", "g.example.com")
    (None, None)
    >>> mgr.find_user_password("f", "http://g.example.com:100")
    (None, None)
    >>> mgr.find_user_password("f", "http://g.example.com:80")
    ('10', 'j')
    >>> mgr.find_user_password("f", "http://g.example.com")
    ('10', 'j')
    >>> mgr.find_user_password("g", "h.example.com")
    ('11', 'k')
    >>> mgr.find_user_password("g", "h.example.com:80")
    ('11', 'k')
    >>> mgr.find_user_password("g", "http://h.example.com:80")
    ('11', 'k')
    >>> mgr.find_user_password("h", "i.example.com")
    (None, None)
    >>> mgr.find_user_password("h", "i.example.com:80")
    ('12', 'l')
    >>> mgr.find_user_password("h", "http://i.example.com:80")
    ('12', 'l')
    >>> mgr.find_user_password("i", "j.example.com")
    ('13', 'm')
    >>> mgr.find_user_password("i", "j.example.com:80")
    (None, None)
    >>> mgr.find_user_password("i", "http://j.example.com")
    ('13', 'm')
    >>> mgr.find_user_password("i", "http://j.example.com:80")
    (None, None)

    """


class MockOpener:
    addheaders = []

    def open(self,
             req,
             data=None,
             timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        self.req, self.data, self.timeout = req, data, timeout

    def error(self, proto, *args):
        self.proto, self.args = proto, args


class MockFile:
    def read(self, count=None):
        pass

    def readline(self, count=None):
        pass

    def close(self):
        pass


def http_message(mapping):
    """
    >>> http_message({"Content-Type": "text/html"}).items()
    [('content-type', 'text/html')]

    """
    f = []
    for kv in mapping.items():
        f.append("%s: %s" % kv)
    f.append("")
    msg = httplib.HTTPMessage(StringIO.StringIO("\r\n".join(f)))
    return msg


class MockResponse(StringIO.StringIO):
    def __init__(self, code, msg, headers, data, url=None):
        StringIO.StringIO.__init__(self, data)
        self.code, self.msg, self.headers, self.url = code, msg, headers, url

    def info(self):
        return self.headers

    def geturl(self):
        return self.url


class MockCookieJar:
    def add_cookie_header(self, request, unverifiable=False):
        self.ach_req, self.ach_u = request, unverifiable

    def extract_cookies(self, response, request, unverifiable=False):
        self.ec_req, self.ec_r, self.ec_u = request, response, unverifiable


class FakeMethod:
    def __init__(self, meth_name, action, handle):
        self.meth_name = meth_name
        self.handle = handle
        self.action = action

    def __call__(self, *args):
        return self.handle(self.meth_name, self.action, *args)


class MockHandler:
    # useful for testing handler machinery
    # see add_ordered_mock_handlers() docstring
    handler_order = 500

    def __init__(self, methods):
        self._define_methods(methods)

    def _define_methods(self, methods):
        for spec in methods:
            if len(spec) == 2:
                name, action = spec
            else:
                name, action = spec, None
            meth = FakeMethod(name, action, self.handle)
            setattr(self.__class__, name, meth)

    def handle(self, fn_name, action, *args, **kwds):
        self.parent.calls.append((self, fn_name, args, kwds))
        if action is None:
            return None
        elif action == "return self":
            return self
        elif action == "return response":
            res = MockResponse(200, "OK", {}, "")
            return res
        elif action == "return request":
            return Request("http://blah/")
        elif action.startswith("error"):
            code = action[action.rfind(" ") + 1:]
            try:
                code = int(code)
            except ValueError:
                pass
            res = MockResponse(200, "OK", {}, "")
            return self.parent.error("http", args[0], res, code, "", {})
        elif action == "raise":
            raise mechanize.URLError("blah")
        assert False

    def close(self):
        pass

    def add_parent(self, parent):
        self.parent = parent
        self.parent.calls = []

    def __lt__(self, other):
        if not hasattr(other, "handler_order"):
            # Try to preserve the old behavior of having custom classes
            # inserted after default ones (works only for custom user
            # classes which are not aware of handler_order).
            return True
        return self.handler_order < other.handler_order


def add_ordered_mock_handlers(opener, meth_spec):
    """Create MockHandlers and add them to an OpenerDirector.

    meth_spec: list of lists of tuples and strings defining methods to define
    on handlers.  eg:

    [["http_error", "ftp_open"], ["http_open"]]

    defines methods .http_error() and .ftp_open() on one handler, and
    .http_open() on another.  These methods just record their arguments and
    return None.  Using a tuple instead of a string causes the method to
    perform some action (see MockHandler.handle()), eg:

    [["http_error"], [("http_open", "return request")]]

    defines .http_error() on one handler (which simply returns None), and
    .http_open() on another handler, which returns a Request object.

    """
    handlers = []
    count = 0
    for meths in meth_spec:

        class MockHandlerSubclass(MockHandler):
            pass

        h = MockHandlerSubclass(meths)
        h.handler_order += count
        h.add_parent(opener)
        count = count + 1
        handlers.append(h)
        opener.add_handler(h)
    return handlers


def build_test_opener(*handler_instances):
    opener = OpenerDirector()
    for h in handler_instances:
        opener.add_handler(h)
    return opener


class MockHTTPHandler(mechanize.BaseHandler):
    # useful for testing redirections and auth
    # sends supplied headers and code as first response
    # sends 200 OK as second response

    def __init__(self, code, headers):
        self.code = code
        self.headers = headers
        self.reset()

    def reset(self):
        self._count = 0
        self.requests = []

    def http_open(self, req):
        import mimetools
        import copy
        from StringIO import StringIO
        self.requests.append(copy.deepcopy(req))
        if self._count == 0:
            self._count = self._count + 1
            name = "Not important"
            msg = mimetools.Message(StringIO(self.headers))
            return self.parent.error("http", req,
                                     test_response(), self.code, name, msg)
        else:
            self.req = req
            return test_response("", [], req.get_full_url())


class MockHTTPResponse:
    def __init__(self, fp, msg, status, reason):
        self.fp = fp
        self.msg = msg
        self.status = status
        self.reason = reason

    def read(self):
        return ''


class MockHTTPClass:
    def __init__(self):
        self.req_headers = []
        self.data = None
        self.raise_on_endheaders = False
        self._tunnel_headers = {}

    def __call__(self, host, timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        self.host = host
        self.timeout = timeout
        return self

    def set_debuglevel(self, level):
        self.level = level

    def set_tunnel(self, host, port=None, headers=None):
        self._tunnel_host = host
        self._tunnel_port = port
        if headers:
            self._tunnel_headers = headers
        else:
            self._tunnel_headers.clear()

    def request(self, method, url, body=None, headers={}):
        self.method = method
        self.selector = url
        self.req_headers += headers.items()
        self.req_headers.sort()
        if body:
            self.data = body
        if self.raise_on_endheaders:
            import socket

            raise socket.error()

    def getresponse(self):
        return MockHTTPResponse(MockFile(), {}, 200, "OK")


class MockHTTPSHandler(AbstractHTTPHandler):
    # Useful for testing the Proxy-Authorization request by verifying the
    # properties of httpcon
    httpconn = MockHTTPClass()

    def https_open(self, req):
        return self.do_open(self.httpconn, req)


class MockPasswordManager:
    def add_password(self, realm, uri, user, password):
        self.realm = realm
        self.url = uri
        self.user = user
        self.password = password

    def find_user_password(self, realm, authuri):
        self.target_realm = realm
        self.target_url = authuri
        return self.user, self.password


class OpenerDirectorTests(unittest.TestCase):
    def test_add_non_handler(self):
        class NonHandler(object):
            pass

        self.assertRaises(TypeError, OpenerDirector().add_handler,
                          NonHandler())

    def test_badly_named_methods(self):
        # test work-around for three methods that accidentally follow the
        # naming conventions for handler methods
        # (*_open() / *_request() / *_response())

        # These used to call the accidentally-named methods, causing a
        # TypeError in real code; here, returning self from these mock
        # methods would either cause no exception, or AttributeError.

        from mechanize import URLError

        o = OpenerDirector()
        meth_spec = [
            [("do_open", "return self"), ("proxy_open", "return self")],
            [("redirect_request", "return self")],
        ]
        handlers = add_ordered_mock_handlers(o, meth_spec)
        o.add_handler(mechanize.UnknownHandler())
        for scheme in "do", "proxy", "redirect":
            self.assertRaises(URLError, o.open, scheme + "://example.com/")

    def test_handled(self):
        # handler returning non-None means no more handlers will be called
        o = OpenerDirector()
        meth_spec = [
            ["http_open", "ftp_open", "http_error_302"],
            ["ftp_open"],
            [("http_open", "return self")],
            [("http_open", "return self")],
        ]
        handlers = add_ordered_mock_handlers(o, meth_spec)

        req = Request("http://example.com/")
        r = o.open(req)
        # Second .http_open() gets called, third doesn't, since second returned
        # non-None.  Handlers without .http_open() never get any methods called
        # on them.
        # In fact, second mock handler defining .http_open() returns self
        # (instead of response), which becomes the OpenerDirector's return
        # value.
        self.assertEqual(r, handlers[2])
        calls = [(handlers[0], "http_open"), (handlers[2], "http_open")]
        for expected, got in zip(calls, o.calls):
            handler, name, args, kwds = got
            self.assertEqual((handler, name), expected)
            self.assertEqual(args, (req, ))

    def test_reindex_handlers(self):
        o = OpenerDirector()

        class MockHandler:
            def add_parent(self, parent):
                pass

            def close(self):
                pass

            def __lt__(self, other):
                return self.handler_order < other.handler_order

        # this first class is here as an obscure regression test for bug
        # encountered during development: if something manages to get through
        # to _maybe_reindex_handlers, make sure it's properly removed and
        # doesn't affect adding of subsequent handlers
        class NonHandler(MockHandler):
            handler_order = 1

        class Handler(MockHandler):
            handler_order = 2

            def http_open(self):
                pass

        class Processor(MockHandler):
            handler_order = 3

            def any_response(self):
                pass

            def http_response(self):
                pass

        o.add_handler(NonHandler())
        h = Handler()
        o.add_handler(h)
        p = Processor()
        o.add_handler(p)
        o._maybe_reindex_handlers()
        self.assertEqual(o.handle_open, {"http": [h]})
        self.assertEqual(len(o.process_response.keys()), 1)
        self.assertEqual(list(o.process_response["http"]), [p])
        self.assertEqual(list(o._any_response), [p])
        self.assertEqual(o.handlers, [h, p])

    def test_handler_order(self):
        o = OpenerDirector()
        handlers = []
        for meths, handler_order in [
            ([("http_open", "return self")], 500),
            (["http_open"], 0),
        ]:

            class MockHandlerSubclass(MockHandler):
                pass

            h = MockHandlerSubclass(meths)
            h.handler_order = handler_order
            handlers.append(h)
            o.add_handler(h)

        r = o.open("http://example.com/")
        # handlers called in reverse order, thanks to their sort order
        self.assertEqual(o.calls[0][0], handlers[1])
        self.assertEqual(o.calls[1][0], handlers[0])

    def test_raise(self):
        # raising URLError stops processing of request
        o = OpenerDirector()
        meth_spec = [
            [("http_open", "raise")],
            [("http_open", "return self")],
        ]
        handlers = add_ordered_mock_handlers(o, meth_spec)

        req = Request("http://example.com/")
        self.assertRaises(mechanize.URLError, o.open, req)
        self.assertEqual(o.calls, [(handlers[0], "http_open", (req, ), {})])

# def test_error(self):
# XXX this doesn't actually seem to be used in standard library,
# but should really be tested anyway...

    def test_http_error(self):
        # XXX http_error_default
        # http errors are a special case
        o = OpenerDirector()
        meth_spec = [
            [("http_open", "error 302")],
            [("http_error_400", "raise"), "http_open"],
            [("http_error_302", "return response"), "http_error_303",
             "http_error"],
            [("http_error_302")],
        ]
        handlers = add_ordered_mock_handlers(o, meth_spec)

        req = Request("http://example.com/")
        r = o.open(req)
        assert len(o.calls) == 2
        calls = [(handlers[0], "http_open", (req, )), (
            handlers[2], "http_error_302", (req, AlwaysEqual(), 302, "", {}))]
        for expected, got in zip(calls, o.calls):
            handler, method_name, args = expected
            self.assertEqual((handler, method_name), got[:2])
            self.assertEqual(args, got[2])

    def test_http_error_raised(self):
        # should get an HTTPError if an HTTP handler raises a non-200 response
        # XXX it worries me that this is the only test that excercises the else
        # branch in HTTPDefaultErrorHandler
        from mechanize import _response
        o = mechanize.OpenerDirector()
        o.add_handler(mechanize.HTTPErrorProcessor())
        o.add_handler(mechanize.HTTPDefaultErrorHandler())

        class HTTPHandler(AbstractHTTPHandler):
            def http_open(self, req):
                return _response.test_response(code=302)

        o.add_handler(HTTPHandler())
        self.assertRaises(mechanize.HTTPError, o.open, "http://example.com/")

    def test_processors(self):
        # *_request / *_response methods get called appropriately
        o = OpenerDirector()
        meth_spec = [
            [("http_request", "return request"),
             ("http_response", "return response")],
            [("http_request", "return request"),
             ("http_response", "return response")],
        ]
        handlers = add_ordered_mock_handlers(o, meth_spec)

        req = Request("http://example.com/")
        r = o.open(req)
        # processor methods are called on *all* handlers that define them,
        # not just the first handler that handles the request
        calls = [(handlers[0], "http_request"), (handlers[1], "http_request"),
                 (handlers[0], "http_response"),
                 (handlers[1], "http_response")]

        self.assertEqual(len(o.calls), len(calls))
        for i, (handler, name, args, kwds) in enumerate(o.calls):
            if i < 2:
                # *_request
                self.assertEqual((handler, name), calls[i])
                self.assertEqual(len(args), 1)
                self.assertTrue(isinstance(args[0], Request))
            else:
                # *_response
                self.assertEqual((handler, name), calls[i])
                self.assertEqual(len(args), 2)
                self.assertTrue(isinstance(args[0], Request))
                # response from opener.open is None, because there's no
                # handler that defines http_open to handle it
                self.assertTrue(args[1] is None or
                                isinstance(args[1], MockResponse))

    def test_any(self):
        # XXXXX two handlers case: ordering
        o = OpenerDirector()
        meth_spec = [[
            ("http_request", "return request"),
            ("http_response", "return response"),
            ("ftp_request", "return request"),
            ("ftp_response", "return response"),
            ("any_request", "return request"),
            ("any_response", "return response"),
        ]]
        handlers = add_ordered_mock_handlers(o, meth_spec)
        handler = handlers[0]

        for scheme in ["http", "ftp"]:
            o.calls = []
            req = Request("%s://example.com/" % scheme)
            r = o.open(req)

            calls = [
                (handler, "any_request"),
                (handler, ("%s_request" % scheme)),
                (handler, "any_response"),
                (handler, ("%s_response" % scheme)),
            ]
            self.assertEqual(len(o.calls), len(calls))
            for i, ((handler, name, args, kwds), calls) in (
                    enumerate(zip(o.calls, calls))):
                if i < 2:
                    # *_request
                    self.assert_((handler, name) == calls)
                    self.assert_(len(args) == 1)
                    self.assert_(isinstance(args[0], Request))
                else:
                    # *_response
                    self.assert_((handler, name) == calls)
                    self.assert_(len(args) == 2)
                    self.assert_(isinstance(args[0], Request))
                    # response from opener.open is None, because there's no
                    # handler that defines http_open to handle it
                    self.assert_(args[1] is None or
                                 isinstance(args[1], MockResponse))


class MockRobotFileParserClass:
    def __init__(self):
        self.calls = []
        self._can_fetch = True

    def clear(self):
        self.calls = []

    def __call__(self):
        self.calls.append("__call__")
        return self

    def set_url(self, url):
        self.calls.append(("set_url", url))

    def set_timeout(self, timeout):
        self.calls.append(("set_timeout", timeout))

    def set_opener(self, opener):
        self.calls.append(("set_opener", opener))

    def read(self):
        self.calls.append("read")

    def can_fetch(self, ua, url):
        self.calls.append(("can_fetch", ua, url))
        return self._can_fetch


class MockPasswordManager:
    def add_password(self, realm, uri, user, password):
        self.realm = realm
        self.url = uri
        self.user = user
        self.password = password

    def find_user_password(self, realm, authuri):
        self.target_realm = realm
        self.target_url = authuri
        return self.user, self.password


class HandlerTests(mechanize._testcase.TestCase):
    def test_ftp(self):
        class MockFTPWrapper:
            def __init__(self, data):
                self.data = data

            def retrfile(self, filename, filetype):
                self.filename, self.filetype = filename, filetype
                return StringIO.StringIO(self.data), len(self.data)

        class NullFTPHandler(mechanize.FTPHandler):
            def __init__(self, data):
                self.data = data

            def connect_ftp(self, user, passwd, host, port, dirs, timeout):
                self.user, self.passwd = user, passwd
                self.host, self.port = host, port
                self.dirs = dirs
                self.timeout = timeout
                self.ftpwrapper = MockFTPWrapper(self.data)
                return self.ftpwrapper

        import ftplib
        import socket
        data = "rheum rhaponicum"
        h = NullFTPHandler(data)
        o = h.parent = MockOpener()

        for url, host, port, type_, dirs, timeout, filename, mimetype in [
            ("ftp://localhost/foo/bar/baz.html", "localhost", ftplib.FTP_PORT,
             "I", ["foo", "bar"], _sockettimeout._GLOBAL_DEFAULT_TIMEOUT,
             "baz.html", "text/html"),
            ("ftp://localhost:80/foo/bar/", "localhost", 80, "D",
             ["foo", "bar"], _sockettimeout._GLOBAL_DEFAULT_TIMEOUT, "", None),
            ("ftp://localhost/baz.gif;type=a", "localhost", ftplib.FTP_PORT,
             "A", [], _sockettimeout._GLOBAL_DEFAULT_TIMEOUT, "baz.gif",
             None),  # TODO: really this should guess image/gif
        ]:
            req = Request(url, timeout=timeout)
            r = h.ftp_open(req)
            # ftp authentication not yet implemented by FTPHandler
            self.assertTrue(h.user == h.passwd == "")
            self.assertEqual(h.host, socket.gethostbyname(host))
            self.assertEqual(h.port, port)
            self.assertEqual(h.dirs, dirs)
            if sys.version_info >= (2, 6):
                self.assertEquals(h.timeout, timeout)
            self.assertEqual(h.ftpwrapper.filename, filename)
            self.assertEqual(h.ftpwrapper.filetype, type_)
            headers = r.info()
            self.assertEqual(headers.get("Content-type"), mimetype)
            self.assertEqual(int(headers["Content-length"]), len(data))

    def test_file(self):
        import rfc822
        import socket
        h = mechanize.FileHandler()
        o = h.parent = MockOpener()

        temp_file = os.path.join(self.make_temp_dir(), "test.txt")
        urlpath = sanepathname2url(os.path.abspath(temp_file))
        towrite = "hello, world\n"
        try:
            fqdn = socket.gethostbyname(socket.gethostname())
        except socket.gaierror:
            fqdn = "localhost"
        for url in [
                "file://localhost%s" % urlpath, "file://%s" % urlpath,
                "file://%s%s" % (socket.gethostbyname('localhost'), urlpath),
                "file://%s%s" % (fqdn, urlpath)
        ]:
            write_file(temp_file, towrite)
            r = h.file_open(Request(url))
            try:
                data = r.read()
                headers = r.info()
                newurl = r.geturl()
            finally:
                r.close()
            stats = os.stat(temp_file)
            modified = rfc822.formatdate(stats.st_mtime)
            self.assertEqual(data, towrite)
            self.assertEqual(headers["Content-type"], "text/plain")
            self.assertEqual(headers["Content-length"], "13")
            self.assertEqual(headers["Last-modified"], modified)

        for url in [
                "file://localhost:80%s" % urlpath,
                "file:///file_does_not_exist.txt",
                "file://%s:80%s/%s" % (socket.gethostbyname('localhost'),
                                       sanepathname2url(os.getcwd()),
                                       temp_file),
                "file://somerandomhost.ontheinternet.com%s/%s" %
            (sanepathname2url(os.getcwd()), temp_file),
        ]:
            write_file(temp_file, towrite)
            self.assertRaises(mechanize.URLError, h.file_open, Request(url))

        h = mechanize.FileHandler()
        o = h.parent = MockOpener()
        # XXXX why does // mean ftp (and /// mean not ftp!), and where
        #  is file: scheme specified?  I think this is really a bug, and
        #  what was intended was to distinguish between URLs like:
        # file:/blah.txt (a file)
        # file://localhost/blah.txt (a file)
        # file:///blah.txt (a file)
        # file://ftp.example.com/blah.txt (an ftp URL)
        for url, ftp in [
            ("file://ftp.example.com//foo.txt", True),
            ("file://ftp.example.com///foo.txt", False),
                # XXXX bug: fails with OSError, should be URLError
            ("file://ftp.example.com/foo.txt", False),
        ]:
            req = Request(url)
            try:
                h.file_open(req)
            # XXXX remove OSError when bug fixed
            except (mechanize.URLError, OSError):
                self.assertFalse(ftp)
            else:
                self.assertTrue(o.req is req)
                self.assertEqual(req.type, "ftp")

    def test_http(self):
        class MockHTTPResponse:
            def __init__(self, fp, msg, status, reason):
                self.fp = fp
                self.msg = msg
                self.status = status
                self.reason = reason

            def read(self):
                return ''

        class MockHTTPClass:
            def __init__(self):
                self.req_headers = []
                self.data = None
                self.raise_on_endheaders = False

            def __call__(self,
                         host,
                         timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
                self.host = host
                self.timeout = timeout
                return self

            def set_debuglevel(self, level):
                self.level = level

            def request(self, method, url, body=None, headers={}):
                self.method = method
                self.selector = url
                self.req_headers += headers.items()
                self.req_headers.sort()
                if body:
                    self.data = body
                if self.raise_on_endheaders:
                    import socket
                    raise socket.error()

            def getresponse(self):
                return MockHTTPResponse(MockFile(), {}, 200, "OK")

        h = AbstractHTTPHandler()
        o = h.parent = MockOpener()

        url = "http://example.com/"
        for method, data in [("GET", None), ("POST", "blah")]:
            req = Request(url, data, {"Foo": "bar"})
            req.add_unredirected_header("Spam", "eggs")
            http = MockHTTPClass()
            r = h.do_open(http, req)

            # result attributes
            r.read
            r.readline  # wrapped MockFile methods
            r.info
            r.geturl  # addinfourl methods
            r.code, r.msg == 200, "OK"  # added from MockHTTPClass.getreply()
            hdrs = r.info()
            hdrs.get
            hdrs.has_key  # r.info() gives dict from .getreply()
            self.assertEqual(r.geturl(), url)

            self.assertEqual(http.host, "example.com")
            self.assertEqual(http.level, 0)
            self.assertEqual(http.method, method)
            self.assertEqual(http.selector, "/")
            self.assertEqual(http.req_headers,
                             [("Connection", "close"), ("Foo", "bar"),
                              ("Spam", "eggs")])
            self.assertEqual(http.data, data)

        # check socket.error converted to URLError
        http.raise_on_endheaders = True
        self.assertRaises(mechanize.URLError, h.do_open, http, req)

        # check adding of standard headers
        o.addheaders = [("Spam", "eggs")]
        for data in "", None:  # POST, GET
            req = Request("http://example.com/", data)
            r = MockResponse(200, "OK", {}, "")
            newreq = h.do_request_(req)
            if data is None:  # GET
                self.assertTrue("Content-length" not in req.unredirected_hdrs)
                self.assertTrue("Content-type" not in req.unredirected_hdrs)
            else:  # POST
                self.assertEqual(req.unredirected_hdrs["Content-Length"], "0")
                self.assertEqual(req.unredirected_hdrs["Content-Type"],
                                 "application/x-www-form-urlencoded")
            # XXX the details of Host could be better tested
            self.assertEqual(req.unredirected_hdrs["Host"], "example.com")
            self.assertEqual(req.unredirected_hdrs["Spam"], "eggs")

            # don't clobber existing headers
            req.add_unredirected_header("Content-Length", "foo")
            req.add_unredirected_header("Content-Type", "bar")
            req.add_unredirected_header("Host", "baz")
            req.add_unredirected_header("Spam", "foo")
            newreq = h.do_request_(req)
            self.assertEqual(req.unredirected_hdrs["Content-Length"], "foo")
            self.assertEqual(req.unredirected_hdrs["Content-Type"], "bar")
            self.assertEqual(req.unredirected_hdrs["Host"], "baz")
            self.assertEqual(req.unredirected_hdrs["Spam"], "foo")

    def test_http_double_slash(self):
        # Checks that the presence of an unnecessary double slash in a url
        # doesn't break anything Previously, a double slash directly after the
        # host could cause incorrect parsing of the url
        h = AbstractHTTPHandler()
        o = h.parent = MockOpener()

        data = ""
        ds_urls = [
            "http://example.com/foo/bar/baz.html",
            "http://example.com//foo/bar/baz.html",
            "http://example.com/foo//bar/baz.html",
            "http://example.com/foo/bar//baz.html",
        ]

        for ds_url in ds_urls:
            ds_req = Request(ds_url, data)

            # Check whether host is determined correctly if there is no proxy
            np_ds_req = h.do_request_(ds_req)
            self.assertEqual(np_ds_req.unredirected_hdrs["Host"],
                             "example.com")

            # Check whether host is determined correctly if there is a proxy
            ds_req.set_proxy("someproxy:3128", None)
            p_ds_req = h.do_request_(ds_req)
            self.assertEqual(p_ds_req.unredirected_hdrs["Host"], "example.com")

    def test_errors(self):
        h = HTTPErrorProcessor()
        o = h.parent = MockOpener()

        req = Request("http://example.com")
        # all 2xx are passed through
        r = mechanize._response.test_response()
        newr = h.http_response(req, r)
        self.assertTrue(r is newr)
        self.assertTrue(not hasattr(o, "proto"))  # o.error not called
        r = mechanize._response.test_response(code=202, msg="Accepted")
        newr = h.http_response(req, r)
        self.assertTrue(r is newr)
        self.assertTrue(not hasattr(o, "proto"))  # o.error not called
        r = mechanize._response.test_response(code=206, msg="Partial content")
        newr = h.http_response(req, r)
        self.assertTrue(r is newr)
        self.assertTrue(not hasattr(o, "proto"))  # o.error not called
        # anything else calls o.error (and MockOpener returns None, here)
        r = mechanize._response.test_response(code=502, msg="Bad gateway")
        self.assertTrue(h.http_response(req, r) is None)
        self.assertEqual(o.proto, "http")  # o.error called
        self.assertEqual(o.args, (req, r, 502, "Bad gateway", AlwaysEqual()))

    def test_referer(self):
        h = HTTPRefererProcessor()
        o = h.parent = MockOpener()

        # normal case
        url = "http://example.com/"
        req = Request(url)
        r = MockResponse(200, "OK", {}, "", url)
        newr = h.http_response(req, r)
        self.assert_(r is newr)
        self.assert_(h.referer == url)
        newreq = h.http_request(req)
        self.assert_(req is newreq)
        self.assert_(req.unredirected_hdrs["Referer"] == url)
        # don't clobber existing Referer
        ref = "http://set.by.user.com/"
        req.add_unredirected_header("Referer", ref)
        newreq = h.http_request(req)
        self.assert_(req is newreq)
        self.assert_(req.unredirected_hdrs["Referer"] == ref)

    def test_raise_http_errors(self):
        # HTTPDefaultErrorHandler should raise HTTPError if no error handler
        # handled the error response
        from mechanize import _response
        h = mechanize.HTTPDefaultErrorHandler()

        url = "http://example.com"
        code = 500
        msg = "Error"
        request = mechanize.Request(url)
        response = _response.test_response(url=url, code=code, msg=msg)

        # case 1. it's not an HTTPError
        try:
            h.http_error_default(request, response, code, msg, response.info())
        except mechanize.HTTPError as exc:
            self.assert_(exc is not response)
            self.assert_(exc.fp is response)
        else:
            self.assert_(False)

        # case 2. response object is already an HTTPError, so just re-raise it
        error = mechanize.HTTPError(url, code, msg, "fake headers", response)
        try:
            h.http_error_default(request, error, code, msg, error.info())
        except mechanize.HTTPError as exc:
            self.assert_(exc is error)
        else:
            self.assert_(False)

    def test_robots(self):
        # XXX useragent
        from mechanize import HTTPRobotRulesProcessor
        opener = OpenerDirector()
        rfpc = MockRobotFileParserClass()
        h = HTTPRobotRulesProcessor(rfpc)
        opener.add_handler(h)

        url = "http://example.com:80/foo/bar.html"
        req = Request(url)
        # first time: initialise and set up robots.txt parser before checking
        #  whether OK to fetch URL
        h.http_request(req)
        self.assertEquals(rfpc.calls, [
            "__call__",
            ("set_opener", opener),
            ("set_url", "http://example.com:80/robots.txt"),
            ("set_timeout", _sockettimeout._GLOBAL_DEFAULT_TIMEOUT),
            "read",
            ("can_fetch", "", url),
        ])
        # second time: just use existing parser
        rfpc.clear()
        req = Request(url)
        h.http_request(req)
        self.assert_(rfpc.calls == [
            ("can_fetch", "", url),
        ])
        # different URL on same server: same again
        rfpc.clear()
        url = "http://example.com:80/blah.html"
        req = Request(url)
        h.http_request(req)
        self.assert_(rfpc.calls == [
            ("can_fetch", "", url),
        ])
        # disallowed URL
        rfpc.clear()
        rfpc._can_fetch = False
        url = "http://example.com:80/rhubarb.html"
        req = Request(url)
        try:
            h.http_request(req)
        except mechanize.HTTPError as e:
            self.assert_(e.request == req)
            self.assert_(e.code == 403)
        # new host: reload robots.txt (even though the host and port are
        #  unchanged, we treat this as a new host because
        #  "example.com" != "example.com:80")
        rfpc.clear()
        rfpc._can_fetch = True
        url = "http://example.com/rhubarb.html"
        req = Request(url)
        h.http_request(req)
        self.assertEquals(rfpc.calls, [
            "__call__",
            ("set_opener", opener),
            ("set_url", "http://example.com/robots.txt"),
            ("set_timeout", _sockettimeout._GLOBAL_DEFAULT_TIMEOUT),
            "read",
            ("can_fetch", "", url),
        ])
        # https url -> should fetch robots.txt from https url too
        rfpc.clear()
        url = "https://example.org/rhubarb.html"
        req = Request(url)
        h.http_request(req)
        self.assertEquals(rfpc.calls, [
            "__call__",
            ("set_opener", opener),
            ("set_url", "https://example.org/robots.txt"),
            ("set_timeout", _sockettimeout._GLOBAL_DEFAULT_TIMEOUT),
            "read",
            ("can_fetch", "", url),
        ])
        # non-HTTP URL -> ignore robots.txt
        rfpc.clear()
        url = "ftp://example.com/"
        req = Request(url)
        h.http_request(req)
        self.assert_(rfpc.calls == [])

    def test_redirected_robots_txt(self):
        # redirected robots.txt fetch shouldn't result in another attempted
        # robots.txt fetch to check the redirection is allowed!
        import mechanize
        from mechanize import build_opener, HTTPHandler, \
            HTTPDefaultErrorHandler, HTTPRedirectHandler, \
            HTTPRobotRulesProcessor

        class MockHTTPHandler(mechanize.BaseHandler):
            def __init__(self):
                self.requests = []

            def http_open(self, req):
                import mimetools
                import httplib
                import copy
                from StringIO import StringIO
                self.requests.append(copy.deepcopy(req))
                if req.get_full_url() == "http://example.com/robots.txt":
                    hdr = "Location: http://example.com/en/robots.txt\r\n\r\n"
                    msg = mimetools.Message(StringIO(hdr))
                    return self.parent.error("http", req,
                                             test_response(), 302, "Blah", msg)
                else:
                    return test_response("Allow: *", [], req.get_full_url())

        hh = MockHTTPHandler()
        hdeh = HTTPDefaultErrorHandler()
        hrh = HTTPRedirectHandler()
        rh = HTTPRobotRulesProcessor()
        o = build_test_opener(hh, hdeh, hrh, rh)
        o.open("http://example.com/")
        self.assertEqual([req.get_full_url() for req in hh.requests], [
            "http://example.com/robots.txt",
            "http://example.com/en/robots.txt",
            "http://example.com/",
        ])

    def test_cookies(self):
        cj = MockCookieJar()
        h = HTTPCookieProcessor(cj)
        o = h.parent = MockOpener()

        req = Request("http://example.com/")
        r = MockResponse(200, "OK", {}, "")
        newreq = h.http_request(req)
        self.assertTrue(cj.ach_req is req is newreq)
        self.assertEquals(req.get_origin_req_host(), "example.com")
        self.assertFalse(cj.ach_u)
        newr = h.http_response(req, r)
        self.assertTrue(cj.ec_req is req)
        self.assertTrue(cj.ec_r is r is newr)
        self.assertFalse(cj.ec_u)

    def test_http_equiv(self):
        h = HTTPEquivProcessor()
        o = h.parent = MockOpener()

        data = ('<html><head>'
                '<meta http-equiv="Refresh" content="spam&amp;eggs">'
                '</head></html>')
        headers = [
            ("Foo", "Bar"),
            ("Content-type", "text/html"),
            ("Refresh", "blah"),
        ]
        url = "http://example.com/"
        req = Request(url)
        r = mechanize._response.make_response(data, headers, url, 200, "OK")
        newr = h.http_response(req, r)

        new_headers = newr.info()
        self.assertEqual(new_headers["Foo"], "Bar")
        self.assertEqual(new_headers["Refresh"], "spam&eggs")
        self.assertEqual(
            new_headers.getheaders("Refresh"), ["blah", "spam&eggs"])

    def test_refresh(self):
        # XXX test processor constructor optional args
        h = HTTPRefreshProcessor(max_time=None, honor_time=False)

        for val, valid in [
            ('0; url="http://example.com/foo/"', True),
            ("2", True),
                # in the past, this failed with UnboundLocalError
            ('0; "http://example.com/foo/"', False),
        ]:
            o = h.parent = MockOpener()
            req = Request("http://example.com/")
            headers = http_message({"refresh": val})
            r = MockResponse(200, "OK", headers, "", "http://example.com/")
            newr = h.http_response(req, r)
            if valid:
                self.assertEqual(o.proto, "http")
                self.assertEqual(o.args, (req, r, "refresh", "OK", headers))

    def test_refresh_honor_time(self):
        class SleepTester:
            def __init__(self, test, seconds):
                self._test = test
                if seconds is 0:
                    seconds = None  # don't expect a sleep for 0 seconds
                self._expected = seconds
                self._got = None

            def sleep(self, seconds):
                self._got = seconds

            def verify(self):
                self._test.assertEqual(self._expected, self._got)

        class Opener:
            called = False

            def error(self, *args, **kwds):
                self.called = True

        def test(rp, header, refresh_after):
            expect_refresh = refresh_after is not None
            opener = Opener()
            rp.parent = opener
            st = SleepTester(self, refresh_after)
            rp._sleep = st.sleep
            rp.http_response(
                Request("http://example.com"),
                test_response(headers=[("Refresh", header)]), )
            self.assertEqual(expect_refresh, opener.called)
            st.verify()

        # by default, only zero-time refreshes are honoured
        test(HTTPRefreshProcessor(), "0", 0)
        test(HTTPRefreshProcessor(), "2", None)

        # if requested, more than zero seconds are allowed
        test(HTTPRefreshProcessor(max_time=None), "2", 2)
        test(HTTPRefreshProcessor(max_time=30), "2", 2)

        # no sleep if we don't "honor_time"
        test(HTTPRefreshProcessor(max_time=30, honor_time=False), "2", 0)

        # request for too-long wait before refreshing --> no refresh occurs
        test(HTTPRefreshProcessor(max_time=30), "60", None)

    def test_redirect(self):
        from_url = "http://example.com/a.html"
        to_url = "http://example.com/b.html"
        h = HTTPRedirectHandler()
        o = h.parent = MockOpener()

        # ordinary redirect behaviour
        for code in 301, 302, 303, 307, "refresh":
            for data in None, "blah\nblah\n":
                method = getattr(h, "http_error_%s" % code)
                req = Request(from_url, data)
                req.add_header("Nonsense", "viking=withhold")
                req.add_unredirected_header("Spam", "spam")
                req.origin_req_host = "example.com"  # XXX
                try:
                    method(req,
                           MockFile(), code, "Blah",
                           http_message({
                               "location": to_url
                           }))
                except mechanize.HTTPError:
                    # 307 in response to POST requires user OK
                    self.assertEqual(code, 307)
                    self.assertTrue(data is not None)
                self.assertEqual(o.req.get_full_url(), to_url)
                try:
                    self.assertEqual(o.req.get_method(), "GET")
                except AttributeError:
                    self.assertFalse(o.req.has_data())

                # now it's a GET, there should not be headers regarding content
                # (possibly dragged from before being a POST)
                headers = [x.lower() for x in o.req.headers]
                self.assertTrue("content-length" not in headers)
                self.assertTrue("content-type" not in headers)

                self.assertEqual(o.req.headers["Nonsense"], "viking=withhold")
                self.assertTrue("Spam" not in o.req.headers)
                self.assertTrue("Spam" not in o.req.unredirected_hdrs)

        # loop detection
        req = Request(from_url)

        def redirect(h, req, url=to_url):
            h.http_error_302(req,
                             MockFile(), 302, "Blah",
                             http_message({
                                 "location": url
                             }))

        # Note that the *original* request shares the same record of
        # redirections with the sub-requests caused by the redirections.

        # detect infinite loop redirect of a URL to itself
        req = Request(from_url, origin_req_host="example.com")
        count = 0
        try:
            while 1:
                redirect(h, req, "http://example.com/")
                count = count + 1
        except mechanize.HTTPError:
            # don't stop until max_repeats, because cookies may introduce state
            self.assertEqual(count, HTTPRedirectHandler.max_repeats)

        # detect endless non-repeating chain of redirects
        req = Request(from_url, origin_req_host="example.com")
        count = 0
        try:
            while 1:
                redirect(h, req, "http://example.com/%d" % count)
                count = count + 1
        except mechanize.HTTPError:
            self.assertEqual(count, HTTPRedirectHandler.max_redirections)

    def test_redirect_bad_uri(self):
        # bad URIs should be cleaned up before redirection
        from mechanize._response import test_html_response
        from_url = "http://example.com/a.html"
        bad_to_url = "http://example.com/b. |html"
        good_to_url = "http://example.com/b.%20%7Chtml"

        h = HTTPRedirectHandler()
        o = h.parent = MockOpener()

        req = Request(from_url)
        h.http_error_302(
            req,
            test_html_response(),
            302,
            "Blah",
            http_message({
                "location": bad_to_url
            }), )
        self.assertEqual(o.req.get_full_url(), good_to_url)

    def test_refresh_bad_uri(self):
        # bad URIs should be cleaned up before redirection
        from mechanize._response import test_html_response
        from_url = "http://example.com/a.html"
        bad_to_url = "http://example.com/b. |html"
        good_to_url = "http://example.com/b.%20%7Chtml"

        h = HTTPRefreshProcessor(max_time=None, honor_time=False)
        o = h.parent = MockOpener()

        req = Request("http://example.com/")
        r = test_html_response(
            headers=[("refresh", '0; url="%s"' % bad_to_url)])
        newr = h.http_response(req, r)
        headers = o.args[-1]
        self.assertEqual(headers["Location"], good_to_url)

    def test_cookie_redirect(self):
        # cookies shouldn't leak into redirected requests
        import mechanize
        from mechanize import CookieJar, build_opener, HTTPHandler, \
            HTTPCookieProcessor, HTTPError, HTTPDefaultErrorHandler, \
            HTTPRedirectHandler

        from test_cookies import interact_netscape

        cj = CookieJar()
        interact_netscape(cj, "http://www.example.com/", "spam=eggs")
        hh = MockHTTPHandler(302, "Location: http://www.cracker.com/\r\n\r\n")
        hdeh = HTTPDefaultErrorHandler()
        hrh = HTTPRedirectHandler()
        cp = HTTPCookieProcessor(cj)
        o = build_test_opener(hh, hdeh, hrh, cp)
        o.open("http://www.example.com/")
        self.assertFalse(hh.req.has_header("Cookie"))

    def test_proxy(self):
        o = OpenerDirector()
        ph = mechanize.ProxyHandler(dict(http="proxy.example.com:3128"))
        o.add_handler(ph)
        meth_spec = [[("http_open", "return response")]]
        handlers = add_ordered_mock_handlers(o, meth_spec)

        o._maybe_reindex_handlers()

        req = Request("http://acme.example.com/")
        self.assertEqual(req.get_host(), "acme.example.com")
        r = o.open(req)
        self.assertEqual(req.get_host(), "proxy.example.com:3128")

        self.assertEqual([(handlers[0], "http_open")],
                         [tup[0:2] for tup in o.calls])

    def test_proxy_no_proxy(self):
        self.monkey_patch_environ("no_proxy", "python.org")
        o = OpenerDirector()
        ph = mechanize.ProxyHandler(dict(http="proxy.example.com"))
        o.add_handler(ph)
        req = Request("http://www.perl.org/")
        self.assertEqual(req.get_host(), "www.perl.org")
        r = o.open(req)
        self.assertEqual(req.get_host(), "proxy.example.com")
        req = Request("http://www.python.org")
        self.assertEqual(req.get_host(), "www.python.org")
        r = o.open(req)
        if sys.version_info >= (2, 6):
            # no_proxy environment variable not supported in python 2.5
            self.assertEqual(req.get_host(), "www.python.org")

    def test_proxy_custom_proxy_bypass(self):
        self.monkey_patch_environ("no_proxy",
                                  mechanize._testcase.MonkeyPatcher.Unset)

        def proxy_bypass(hostname):
            return hostname == "noproxy.com"

        o = OpenerDirector()
        ph = mechanize.ProxyHandler(
            dict(http="proxy.example.com"), proxy_bypass=proxy_bypass)

        def is_proxied(url):
            o.add_handler(ph)
            req = Request(url)
            o.open(req)
            return req.has_proxy()

        self.assertTrue(is_proxied("http://example.com"))
        self.assertFalse(is_proxied("http://noproxy.com"))

    def test_proxy_https(self):
        o = OpenerDirector()
        ph = mechanize.ProxyHandler(dict(https='proxy.example.com:3128'))
        o.add_handler(ph)
        meth_spec = [[("https_open", "return response")]]
        handlers = add_ordered_mock_handlers(o, meth_spec)
        req = Request("https://www.example.com/")
        self.assertEqual(req.get_host(), "www.example.com")
        r = o.open(req)
        self.assertEqual(req.get_host(), "proxy.example.com:3128")
        self.assertEqual([(handlers[0], "https_open")],
                         [tup[0:2] for tup in o.calls])

    def test_basic_auth(self, quote_char='"'):
        opener = OpenerDirector()
        password_manager = MockPasswordManager()
        auth_handler = mechanize.HTTPBasicAuthHandler(password_manager)
        realm = "ACME Widget Store"
        http_handler = MockHTTPHandler(
            401, 'WWW-Authenticate: Basic realm=%s%s%s\r\n\r\n' %
            (quote_char, realm, quote_char))
        opener.add_handler(auth_handler)
        opener.add_handler(http_handler)
        self._test_basic_auth(
            opener,
            auth_handler,
            "Authorization",
            realm,
            http_handler,
            password_manager,
            "http://acme.example.com/protected",
            "http://acme.example.com/protected", )

    def test_basic_auth_with_single_quoted_realm(self):
        self.test_basic_auth(quote_char="'")

    def test_proxy_basic_auth(self):
        opener = OpenerDirector()
        ph = mechanize.ProxyHandler(dict(http="proxy.example.com:3128"))
        opener.add_handler(ph)
        password_manager = MockPasswordManager()
        auth_handler = mechanize.ProxyBasicAuthHandler(password_manager)
        realm = "ACME Networks"
        http_handler = MockHTTPHandler(
            407, 'Proxy-Authenticate: Basic realm="%s"\r\n\r\n' % realm)
        opener.add_handler(auth_handler)
        opener.add_handler(http_handler)
        self._test_basic_auth(
            opener,
            auth_handler,
            "Proxy-authorization",
            realm,
            http_handler,
            password_manager,
            "http://acme.example.com:3128/protected",
            "proxy.example.com:3128", )

    def test_proxy_https_proxy_authorization(self):
        o = OpenerDirector()
        ph = mechanize.ProxyHandler(dict(https='proxy.example.com:3128'))
        o.add_handler(ph)
        https_handler = MockHTTPSHandler()
        o.add_handler(https_handler)
        req = Request("https://www.example.com/")
        req.add_header("Proxy-Authorization", "FooBar")
        req.add_header("User-Agent", "Grail")
        self.assertEqual(req.get_host(), "www.example.com")
        self.assertIsNone(req._tunnel_host)
        r = o.open(req)
        # Verify Proxy-Authorization gets tunneled to request.
        # httpsconn req_headers do not have the Proxy-Authorization header but
        # the req will have.
        self.assertFalse(("Proxy-Authorization",
                          "FooBar") in https_handler.httpconn.req_headers)
        self.assertTrue(
            ("User-Agent", "Grail") in https_handler.httpconn.req_headers)
        self.assertIsNotNone(req._tunnel_host)
        self.assertEqual(req.get_host(), "proxy.example.com:3128")
        self.assertEqual(req.get_header("Proxy-authorization"), "FooBar")

    def test_basic_and_digest_auth_handlers(self):
        # HTTPDigestAuthHandler threw an exception if it couldn't handle a 40*
        # response (http://python.org/sf/1479302), where it should instead
        # return None to allow another handler (especially
        # HTTPBasicAuthHandler) to handle the response.

        # Also (http://python.org/sf/1479302, RFC 2617 section 1.2), we must
        # try digest first (since it's the strongest auth scheme), so we record
        # order of calls here to check digest comes first:
        class RecordingOpenerDirector(OpenerDirector):
            def __init__(self):
                OpenerDirector.__init__(self)
                self.recorded = []

            def record(self, info):
                self.recorded.append(info)

        class TestDigestAuthHandler(mechanize.HTTPDigestAuthHandler):
            def http_error_401(self, *args, **kwds):
                self.parent.record("digest")
                mechanize.HTTPDigestAuthHandler.http_error_401(self, *args,
                                                               **kwds)

        class TestBasicAuthHandler(mechanize.HTTPBasicAuthHandler):
            def http_error_401(self, *args, **kwds):
                self.parent.record("basic")
                mechanize.HTTPBasicAuthHandler.http_error_401(self, *args,
                                                              **kwds)

        opener = RecordingOpenerDirector()
        password_manager = MockPasswordManager()
        digest_handler = TestDigestAuthHandler(password_manager)
        basic_handler = TestBasicAuthHandler(password_manager)
        realm = "ACME Networks"
        http_handler = MockHTTPHandler(
            401, 'WWW-Authenticate: Basic realm="%s"\r\n\r\n' % realm)
        opener.add_handler(digest_handler)
        opener.add_handler(basic_handler)
        opener.add_handler(http_handler)
        opener._maybe_reindex_handlers()

        # check basic auth isn't blocked by digest handler failing
        self._test_basic_auth(
            opener,
            basic_handler,
            "Authorization",
            realm,
            http_handler,
            password_manager,
            "http://acme.example.com/protected",
            "http://acme.example.com/protected", )
        # check digest was tried before basic (twice, because
        # _test_basic_auth called .open() twice)
        self.assertEqual(opener.recorded, ["digest", "basic"] * 2)

    def _test_basic_auth(self, opener, auth_handler, auth_header, realm,
                         http_handler, password_manager, request_url,
                         protected_url):
        import base64
        user, password = "wile", "coyote"

        # .add_password() fed through to password manager
        auth_handler.add_password(realm, request_url, user, password)
        self.assertEqual(realm, password_manager.realm)
        self.assertEqual(request_url, password_manager.url)
        self.assertEqual(user, password_manager.user)
        self.assertEqual(password, password_manager.password)

        r = opener.open(request_url)

        # should have asked the password manager for the username/password
        self.assertEqual(password_manager.target_realm, realm)
        self.assertEqual(password_manager.target_url, protected_url)

        # expect one request without authorization, then one with
        self.assertEqual(len(http_handler.requests), 2)
        self.assertFalse(http_handler.requests[0].has_header(auth_header))
        userpass = '%s:%s' % (user, password)
        auth_hdr_value = 'Basic ' + base64.encodestring(userpass).strip()
        self.assertEqual(http_handler.requests[1].get_header(auth_header),
                         auth_hdr_value)

        # if the password manager can't find a password, the handler won't
        # handle the HTTP auth error
        password_manager.user = password_manager.password = None
        http_handler.reset()
        r = opener.open(request_url)
        self.assertEqual(len(http_handler.requests), 1)
        self.assertFalse(http_handler.requests[0].has_header(auth_header))


class HeadParserTests(unittest.TestCase):
    def test(self):
        from mechanize import HTTPEquivParser
        htmls = [
            (
                b"""<meta http-equiv=refresh content="1; http://example.com/">
                """, [("refresh", "1; http://example.com/")]),

            (
                b"""
                <html><head><title>\xea</title>
                <meta http-equiv="refresh" content="1; http://example.com/">
                <meta name="spam" content="eggs">
                <meta content="b&bsol;ar" http-equiv="f&Newline;oo">
                <p> <!-- p is not allowed in head, so parsing should stop -->
                <meta http-equiv="moo" content="cow">
                </html>
                """,
                [("refresh", "1; http://example.com/"), ("f\noo", "b\\ar")]),

            (
                b"""<meta http-equiv="refresh">
                """, []),

        ]
        for html, result in htmls:
            headers = HTTPEquivParser(html)()
            self.assertEqual(result, headers)


class A:
    def a(self):
        pass


class B(A):
    def a(self):
        pass

    def b(self):
        pass


class C(A):
    def c(self):
        pass


class D(C, B):
    def a(self):
        pass

    def d(self):
        pass


class FunctionTests(unittest.TestCase):
    def test_build_opener(self):
        class MyHTTPHandler(HTTPHandler):
            pass

        class FooHandler(mechanize.BaseHandler):
            def foo_open(self):
                pass

        class BarHandler(mechanize.BaseHandler):
            def bar_open(self):
                pass

        o = build_opener(FooHandler, BarHandler)
        self.opener_has_handler(o, FooHandler)
        self.opener_has_handler(o, BarHandler)

        # can take a mix of classes and instances
        o = build_opener(FooHandler, BarHandler())
        self.opener_has_handler(o, FooHandler)
        self.opener_has_handler(o, BarHandler)

        # subclasses of default handlers override default handlers
        o = build_opener(MyHTTPHandler)
        self.opener_has_handler(o, MyHTTPHandler)

        # a particular case of overriding: default handlers can be passed
        # in explicitly
        o = build_opener()
        self.opener_has_handler(o, HTTPHandler)
        o = build_opener(HTTPHandler)
        self.opener_has_handler(o, HTTPHandler)
        o = build_opener(HTTPHandler())
        self.opener_has_handler(o, HTTPHandler)

        # Issue2670: multiple handlers sharing the same base class
        class MyOtherHTTPHandler(HTTPHandler):
            pass

        o = build_opener(MyHTTPHandler, MyOtherHTTPHandler)
        self.opener_has_handler(o, MyHTTPHandler)
        self.opener_has_handler(o, MyOtherHTTPHandler)

    def opener_has_handler(self, opener, handler_class):
        for h in opener.handlers:
            if h.__class__ == handler_class:
                break
        else:
            self.assertTrue(False)


class RequestTests(unittest.TestCase):
    def setUp(self):
        self.get = Request("http://www.python.org/~jeremy/")
        self.post = Request(
            "http://www.python.org/~jeremy/",
            "data",
            headers={"X-Test": "test"})

    def test_method(self):
        self.assertEqual("POST", self.post.get_method())
        self.assertEqual("GET", self.get.get_method())

    def test_add_data(self):
        self.assertTrue(not self.get.has_data())
        self.assertEqual("GET", self.get.get_method())
        self.get.add_data("spam")
        self.assertTrue(self.get.has_data())
        self.assertEqual("POST", self.get.get_method())

    def test_get_full_url(self):
        self.assertEqual("http://www.python.org/~jeremy/",
                         self.get.get_full_url())

    def test_selector(self):
        self.assertEqual("/~jeremy/", self.get.get_selector())
        req = Request("http://www.python.org/")
        self.assertEqual("/", req.get_selector())

    def test_get_type(self):
        self.assertEqual("http", self.get.get_type())

    def test_get_host(self):
        self.assertEqual("www.python.org", self.get.get_host())

    def test_get_host_unquote(self):
        req = Request("http://www.%70ython.org/")
        self.assertEqual("www.python.org", req.get_host())

    def test_proxy(self):
        self.assertTrue(not self.get.has_proxy())
        self.get.set_proxy("www.perl.org", "http")
        self.assertTrue(self.get.has_proxy())
        self.assertEqual("www.python.org", self.get.get_origin_req_host())
        self.assertEqual("www.perl.org", self.get.get_host())

    def test_data(self):
        r = Request('https://example.com', data={'a': 1})
        self.assertEqual(r.get_method(), 'POST')
        self.assertEqual(r.get_data(), 'a=1')
        r = Request('https://example.com', data={'a': 1}, method='GET')
        self.assertEqual(r.get_method(), 'GET')
        self.assertEqual(r.get_data(), None)
        self.assertEqual(r.get_full_url(), 'https://example.com?a=1')


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    unittest.main()
