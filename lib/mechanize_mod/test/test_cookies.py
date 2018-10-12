"""Tests for _clientcookie."""

import StringIO
import errno
import inspect
import mimetools
import os
import re
import sys
import tempfile
import time
import unittest

import mechanize
from mechanize._util import hide_experimental_warnings, \
    reset_experimental_warnings
from mechanize import Request


class FakeResponse:

    def __init__(self, headers=[], url=None):
        """
        headers: list of RFC822-style 'Key: value' strings
        """
        f = StringIO.StringIO("\n".join(headers))
        self._headers = mimetools.Message(f)
        self._url = url

    def info(self):
        return self._headers


def interact_2965(cookiejar, url, *set_cookie_hdrs):
    return _interact(cookiejar, url, set_cookie_hdrs, "Set-Cookie2")


def interact_netscape(cookiejar, url, *set_cookie_hdrs):
    return _interact(cookiejar, url, set_cookie_hdrs, "Set-Cookie")


def _interact(cookiejar, url, set_cookie_hdrs, hdr_name):
    """Perform a single request / response cycle, returning Cookie: header."""
    req = Request(url)
    cookiejar.add_cookie_header(req)
    cookie_hdr = req.get_header("Cookie", "")
    headers = []
    for hdr in set_cookie_hdrs:
        headers.append("%s: %s" % (hdr_name, hdr))
    res = FakeResponse(headers, url)
    cookiejar.extract_cookies(res, req)
    return cookie_hdr


class TempfileTestMixin:

    def setUp(self):
        self._tempfiles = []

    def tearDown(self):
        for fn in self._tempfiles:
            try:
                os.remove(fn)
            except IOError as exc:
                if exc.errno != errno.ENOENT:
                    raise

    def mktemp(self):
        fn = tempfile.mktemp()
        self._tempfiles.append(fn)
        return fn


def caller():
    return sys._getframe().f_back.f_back.f_code.co_name


def attribute_names(obj):
    return set([
        spec[0] for spec in inspect.getmembers(obj)
        if not spec[0].startswith("__")
    ])


class CookieJarInterfaceTests(unittest.TestCase):

    def test_add_cookie_header(self):
        from mechanize import CookieJar

        # verify only these methods are used
        class MockRequest(object):

            def __init__(self):
                self.added_headers = []
                self.called = set()

            def log_called(self):
                self.called.add(caller())

            def get_full_url(self):
                self.log_called()
                return "https://example.com:443"

            def get_host(self):
                self.log_called()
                return "example.com:443"

            def get_type(self):
                self.log_called()
                return "https"

            def has_header(self, header_name):
                self.log_called()
                return False

            def get_header(self, header_name, default=None):
                self.log_called()
                pass  # currently not called

            def header_items(self):
                self.log_called()
                pass  # currently not called

            def add_unredirected_header(self, key, val):
                self.log_called()
                self.added_headers.append((key, val))

            def is_unverifiable(self):
                self.log_called()
                return False

        jar = CookieJar()
        interact_netscape(jar, "https://example.com:443",
                          "foo=bar; port=443; secure")
        request = MockRequest()
        jar.add_cookie_header(request)
        expect_called = attribute_names(MockRequest) - set(
            ["port", "get_header", "header_items", "log_called"])
        self.assertEquals(request.called, expect_called)
        self.assertEquals(request.added_headers, [("Cookie", "foo=bar")])

    def test_extract_cookies(self):
        from mechanize import CookieJar

        # verify only these methods are used

        class StubMessage(object):

            def getheaders(self, name):
                return ["foo=bar; port=443"]

        class StubResponse(object):

            def info(self):
                return StubMessage()

        class StubRequest(object):

            def __init__(self):
                self.added_headers = []
                self.called = set()

            def log_called(self):
                self.called.add(caller())

            def get_full_url(self):
                self.log_called()
                return "https://example.com:443"

            def get_host(self):
                self.log_called()
                return "example.com:443"

            def is_unverifiable(self):
                self.log_called()
                return False

        jar = CookieJar()
        response = StubResponse()
        request = StubRequest()
        jar.extract_cookies(response, request)
        expect_called = attribute_names(StubRequest) - set(
            ["port", "log_called"])
        self.assertEquals(request.called, expect_called)
        self.assertEquals([(cookie.name, cookie.value) for cookie in jar],
                          [("foo", "bar")])

    def test_unverifiable(self):
        from mechanize._clientcookie import request_is_unverifiable

        # .unverifiable was added in mechanize, .is_unverifiable() later got
        # added in cookielib.  XXX deprecate .unverifiable
        class StubRequest(object):

            def __init__(self, attrs):
                self._attrs = attrs
                self.accessed = set()

            def __getattr__(self, name):
                self.accessed.add(name)
                try:
                    return self._attrs[name]
                except KeyError:
                    raise AttributeError(name)

        request = StubRequest(dict(is_unverifiable=lambda: False))
        self.assertEquals(request_is_unverifiable(request), False)

        request = StubRequest(
            dict(is_unverifiable=lambda: False, unverifiable=True))
        self.assertEquals(request_is_unverifiable(request), False)

        request = StubRequest(dict(unverifiable=False))
        self.assertEquals(request_is_unverifiable(request), False)


class CookieTests(unittest.TestCase):
    # XXX
    # Get rid of string comparisons where not actually testing str / repr.
    # .clear() etc.
    # IP addresses like 50 (single number, no dot) and domain-matching
    #  functions (and is_HDN)?  See draft RFC 2965 errata.
    # Strictness switches
    # is_third_party()
    # unverifiability / third_party blocking
    # Netscape cookies work the same as RFC 2965 with regard to port.
    # Set-Cookie with negative max age.
    # If turn RFC 2965 handling off, Set-Cookie2 cookies should not clobber
    #  Set-Cookie cookies.
    # Cookie2 should be sent if *any* cookies are not V1 (ie. V0 OR V2 etc.).
    # Cookies (V1 and V0) with no expiry date should be set to be discarded.
    # RFC 2965 Quoting:
    #  Should accept unquoted cookie-attribute values?  check errata draft.
    #   Which are required on the way in and out?
    #  Should always return quoted cookie-attribute values?
    # Proper testing of when RFC 2965 clobbers Netscape (waiting for errata).
    # Path-match on return (same for V0 and V1).
    # RFC 2965 acceptance and returning rules
    #  Set-Cookie2 without version attribute is rejected.

    # Netscape peculiarities list from Ronald Tschalar.
    # The first two still need tests, the rest are covered.
    # - Quoting: only quotes around the expires value are recognized as such
    # (and yes, some folks quote the expires value); quotes around any other
    # value are treated as part of the value.
    # - White space: white space around names and values is ignored
    # - Default path: if no path parameter is given, the path defaults to the
    # path in the request-uri up to, but not including, the last '/'. Note
    # that this is entirely different from what the spec says.
    # - Commas and other delimiters: Netscape just parses until the next ';'.
    # This means it will allow commas etc inside values (and yes, both
    # commas and equals are commonly appear in the cookie value). This also
    # means that if you fold multiple Set-Cookie header fields into one,
    # comma-separated list, it'll be a headache to parse (at least my head
    # starts hurting everytime I think of that code).
    # - Expires: You'll get all sorts of date formats in the expires,
    # including emtpy expires attributes ("expires="). Be as flexible as you
    # can, and certainly don't expect the weekday to be there; if you can't
    # parse it, just ignore it and pretend it's a session cookie.
    # - Domain-matching: Netscape uses the 2-dot rule for _all_ domains, not
    # just the 7 special TLD's listed in their spec. And folks rely on
    # that...

    def test_policy(self):
        policy = mechanize.DefaultCookiePolicy()
        jar = mechanize.CookieJar()
        jar.set_policy(policy)
        self.assertEquals(jar.get_policy(), policy)

    def test_domain_return_ok(self):
        # test optimization: .domain_return_ok() should filter out most
        # domains in the CookieJar before we try to access them (because that
        # may require disk access -- in particular, with MSIECookieJar)
        # This is only a rough check for performance reasons, so it's not too
        # critical as long as it's sufficiently liberal.
        import mechanize
        pol = mechanize.DefaultCookiePolicy()
        for url, domain, ok in [
            ("http://foo.bar.com/", "blah.com", False),
            ("http://foo.bar.com/", "rhubarb.blah.com", False),
            ("http://foo.bar.com/", "rhubarb.foo.bar.com", False),
            ("http://foo.bar.com/", ".foo.bar.com", True),
            ("http://foo.bar.com/", "foo.bar.com", True),
            ("http://foo.bar.com/", ".bar.com", True),
            ("http://foo.bar.com/", "com", True),
            ("http://foo.com/", "rhubarb.foo.com", False),
            ("http://foo.com/", ".foo.com", True),
            ("http://foo.com/", "foo.com", True),
            ("http://foo.com/", "com", True),
            ("http://foo/", "rhubarb.foo", False),
            ("http://foo/", ".foo", True),
            ("http://foo/", "foo", True),
            ("http://foo/", "foo.local", True),
            ("http://foo/", ".local", True),
        ]:
            request = mechanize.Request(url)
            r = pol.domain_return_ok(domain, request)
            if ok:
                self.assert_(r)
            else:
                self.assert_(not r)

    def test_missing_name(self):
        from mechanize import MozillaCookieJar, lwp_cookie_str

        # missing = sign in Cookie: header is regarded by Mozilla as a missing
        # NAME.  WE regard it as a missing VALUE.
        filename = tempfile.mktemp()
        c = MozillaCookieJar(filename)
        interact_netscape(c, "http://www.acme.com/", 'eggs')
        interact_netscape(c, "http://www.acme.com/", '"spam"; path=/foo/')
        cookie = c._cookies["www.acme.com"]["/"]['eggs']
        assert cookie.name == "eggs"
        assert cookie.value is None
        cookie = c._cookies["www.acme.com"]['/foo/']['"spam"']
        assert cookie.name == '"spam"'
        assert cookie.value is None
        assert lwp_cookie_str(cookie) == (
            r'"spam"; path="/foo/"; domain="www.acme.com"; '
            'path_spec; discard; version=0')
        old_str = repr(c)
        c.save(ignore_expires=True, ignore_discard=True)
        try:
            c = MozillaCookieJar(filename)
            c.revert(ignore_expires=True, ignore_discard=True)
        finally:
            os.unlink(c.filename)
        # cookies unchanged apart from lost info re. whether path was specified
        assert repr(c) == \
            re.sub("path_specified=%s" % True, "path_specified=%s" % False,
                   old_str)
        assert interact_netscape(c, "http://www.acme.com/foo/") == \
            '"spam"; eggs'

    def test_rfc2109_handling(self):
        # 2109 cookies have rfc2109 attr set correctly, and are handled
        # as 2965 or Netscape cookies depending on policy settings
        from mechanize import CookieJar, DefaultCookiePolicy

        for policy, version in [
            (DefaultCookiePolicy(), 0),
            (DefaultCookiePolicy(rfc2965=True), 1),
            (DefaultCookiePolicy(rfc2109_as_netscape=True), 0),
            (DefaultCookiePolicy(rfc2965=True, rfc2109_as_netscape=True), 0),
        ]:
            c = CookieJar(policy)
            interact_netscape(c, "http://www.example.com/", "ni=ni; Version=1")
            cookie = c._cookies["www.example.com"]["/"]["ni"]
            self.assert_(cookie.rfc2109)
            self.assertEqual(cookie.version, version)

    def test_ns_parser(self):
        from mechanize import CookieJar
        from mechanize._clientcookie import DEFAULT_HTTP_PORT

        c = CookieJar()
        interact_netscape(c, "http://www.acme.com/",
                          'spam=eggs; DoMain=.acme.com; port; blArgh="feep"')
        interact_netscape(c, "http://www.acme.com/", 'ni=ni; port=80,8080')
        interact_netscape(c, "http://www.acme.com:80/", 'nini=ni')
        interact_netscape(c, "http://www.acme.com:80/", 'foo=bar; expires=')
        interact_netscape(c, "http://www.acme.com:80/", 'spam=eggs; '
                          'expires="Foo Bar 25 33:22:11 3022"')

        cookie = c._cookies[".acme.com"]["/"]["spam"]
        assert cookie.domain == ".acme.com"
        assert cookie.domain_specified
        assert cookie.port == DEFAULT_HTTP_PORT
        assert not cookie.port_specified
        # case is preserved
        assert (cookie.has_nonstandard_attr("blArgh") and
                not cookie.has_nonstandard_attr("blargh"))

        cookie = c._cookies["www.acme.com"]["/"]["ni"]
        assert cookie.domain == "www.acme.com"
        assert not cookie.domain_specified
        assert cookie.port == "80,8080"
        assert cookie.port_specified

        cookie = c._cookies["www.acme.com"]["/"]["nini"]
        assert cookie.port is None
        assert not cookie.port_specified

        # invalid expires should not cause cookie to be dropped
        foo = c._cookies["www.acme.com"]["/"]["foo"]
        spam = c._cookies["www.acme.com"]["/"]["foo"]
        assert foo.expires is None
        assert spam.expires is None

    def test_ns_parser_special_names(self):
        # names such as 'expires' are not special in first name=value pair
        # of Set-Cookie: header
        from mechanize import CookieJar

        c = CookieJar()
        interact_netscape(c, "http://www.acme.com/", 'expires=eggs')
        interact_netscape(c, "http://www.acme.com/", 'version=eggs; spam=eggs')

        cookies = c._cookies["www.acme.com"]["/"]
        self.assert_('expires' in cookies)
        self.assert_('version' in cookies)

    def test_expires(self):
        from mechanize._util import time2netscape
        from mechanize import CookieJar

        # if expires is in future, keep cookie...
        c = CookieJar()
        future = time2netscape(time.time() + 3600)
        interact_netscape(c, "http://www.acme.com/",
                          'spam="bar"; expires=%s' % future)
        assert len(c) == 1
        now = time2netscape(time.time() - 1)
        # ... and if in past or present, discard it
        interact_netscape(c, "http://www.acme.com/",
                          'foo="eggs"; expires=%s' % now)
        h = interact_netscape(c, "http://www.acme.com/")
        assert len(c) == 1
        assert h.find('spam="bar"') != -1 and h.find("foo") == -1

        # max-age takes precedence over expires, and zero max-age is request to
        # delete both new cookie and any old matching cookie
        interact_netscape(c, "http://www.acme.com/",
                          'eggs="bar"; expires=%s' % future)
        interact_netscape(c, "http://www.acme.com/",
                          'bar="bar"; expires=%s' % future)
        assert len(c) == 3
        interact_netscape(c, "http://www.acme.com/", 'eggs="bar"; '
                          'expires=%s; max-age=0' % future)
        interact_netscape(c, "http://www.acme.com/", 'bar="bar"; '
                          'max-age=0; expires=%s' % future)
        h = interact_netscape(c, "http://www.acme.com/")
        assert len(c) == 1

        # test expiry at end of session for cookies with no expires attribute
        interact_netscape(c, "http://www.rhubarb.net/", 'whum="fizz"')
        assert len(c) == 2
        c.clear_session_cookies()
        assert len(c) == 1
        assert h.find('spam="bar"') != -1

        # XXX RFC 2965 expiry rules (some apply to V0 too)

    def test_default_path(self):
        from mechanize import CookieJar, DefaultCookiePolicy

        # RFC 2965
        pol = DefaultCookiePolicy(rfc2965=True)

        c = CookieJar(pol)
        interact_2965(c, "http://www.acme.com/", 'spam="bar"; Version="1"')
        assert "/" in c._cookies["www.acme.com"]

        c = CookieJar(pol)
        interact_2965(c, "http://www.acme.com/blah", 'eggs="bar"; Version="1"')
        assert "/" in c._cookies["www.acme.com"]

        c = CookieJar(pol)
        interact_2965(c, "http://www.acme.com/blah/rhubarb",
                      'eggs="bar"; Version="1"')
        assert "/blah/" in c._cookies["www.acme.com"]

        c = CookieJar(pol)
        interact_2965(c, "http://www.acme.com/blah/rhubarb/",
                      'eggs="bar"; Version="1"')
        assert "/blah/rhubarb/" in c._cookies["www.acme.com"]

        # Netscape

        c = CookieJar()
        interact_netscape(c, "http://www.acme.com/", 'spam="bar"')
        assert "/" in c._cookies["www.acme.com"]

        c = CookieJar()
        interact_netscape(c, "http://www.acme.com/blah", 'eggs="bar"')
        assert "/" in c._cookies["www.acme.com"]

        c = CookieJar()
        interact_netscape(c, "http://www.acme.com/blah/rhubarb", 'eggs="bar"')
        assert "/blah" in c._cookies["www.acme.com"]

        c = CookieJar()
        interact_netscape(c, "http://www.acme.com/blah/rhubarb/", 'eggs="bar"')
        assert "/blah/rhubarb" in c._cookies["www.acme.com"]

    def test_default_path_with_query(self):
        cj = mechanize.CookieJar()
        uri = "http://example.com/?spam/eggs"
        value = 'eggs="bar"'
        interact_netscape(cj, uri, value)
        # default path does not include query, so is "/", not "/?spam"
        self.assertIn("/", cj._cookies["example.com"])
        # cookie is sent back to the same URI
        self.assertEqual(interact_netscape(cj, uri), value)

    def test_escape_path(self):
        from mechanize._clientcookie import escape_path
        cases = [
            # quoted safe
            ("/foo%2f/bar", "/foo%2F/bar"),
            ("/foo%2F/bar", "/foo%2F/bar"),
            # quoted %
            ("/foo%%/bar", "/foo%%/bar"),
            # quoted unsafe
            ("/fo%19o/bar", "/fo%19o/bar"),
            ("/fo%7do/bar", "/fo%7Do/bar"),
            # unquoted safe
            ("/foo/bar&", "/foo/bar&"),
            ("/foo//bar", "/foo//bar"),
            ("\176/foo/bar", "\176/foo/bar"),
            # unquoted unsafe
            ("/foo\031/bar", "/foo%19/bar"),
            ("/\175foo/bar", "/%7Dfoo/bar"),
            # unicode
            (u"/foo/bar\uabcd", "/foo/bar%EA%AF%8D"),  # UTF-8 encoded
        ]
        for arg, result in cases:
            self.assert_(escape_path(arg) == result)

    def test_request_path(self):
        from mechanize._clientcookie import request_path
        # with parameters
        req = Request("http://www.example.com/rheum/rhaponticum;"
                      "foo=bar;sing=song?apples=pears&spam=eggs#ni")
        self.assertEquals(
            request_path(req), "/rheum/rhaponticum;foo=bar;sing=song")
        # without parameters
        req = Request("http://www.example.com/rheum/rhaponticum?"
                      "apples=pears&spam=eggs#ni")
        self.assertEquals(request_path(req), "/rheum/rhaponticum")
        # missing final slash
        req = Request("http://www.example.com")
        self.assert_(request_path(req) == "/")

    def test_request_port(self):
        from mechanize._clientcookie import request_port, DEFAULT_HTTP_PORT
        req = Request(
            "http://www.acme.com:1234/", headers={"Host": "www.acme.com:4321"})
        assert request_port(req) == "1234"
        req = Request(
            "http://www.acme.com/", headers={"Host": "www.acme.com:4321"})
        assert request_port(req) == DEFAULT_HTTP_PORT

    def test_request_host_lc(self):
        from mechanize._clientcookie import request_host_lc
        # this request is illegal (RFC2616, 14.2.3)
        req = Request("http://1.1.1.1/", headers={"Host": "www.acme.com:80"})
        # libwww-perl wants this response, but that seems wrong (RFC 2616,
        # section 5.2, point 1., and RFC 2965 section 1, paragraph 3)
        #assert request_host_lc(req) == "www.acme.com"
        assert request_host_lc(req) == "1.1.1.1"
        req = Request(
            "http://www.acme.com/", headers={"Host": "irrelevant.com"})
        assert request_host_lc(req) == "www.acme.com"
        # not actually sure this one is valid Request object, so maybe should
        # remove test for no host in url in request_host_lc function?
        req = Request("/resource.html", headers={"Host": "www.acme.com"})
        assert request_host_lc(req) == "www.acme.com"
        # port shouldn't be in request-host
        req = Request(
            "http://www.acme.com:2345/resource.html",
            headers={"Host": "www.acme.com:5432"})
        assert request_host_lc(req) == "www.acme.com"
        # the _lc function lower-cases the result
        req = Request("http://EXAMPLE.com")
        assert request_host_lc(req) == "example.com"

    def test_effective_request_host(self):
        from mechanize import effective_request_host
        self.assertEquals(
            effective_request_host(Request("http://www.EXAMPLE.com/spam")),
            "www.example.com")
        self.assertEquals(
            effective_request_host(Request("http://bob/spam")), "bob.local")

    def test_is_HDN(self):
        from mechanize._clientcookie import is_HDN
        assert is_HDN("foo.bar.com")
        assert is_HDN("1foo2.3bar4.5com")
        assert not is_HDN("192.168.1.1")
        assert not is_HDN("")
        assert not is_HDN(".")
        assert not is_HDN(".foo.bar.com")
        assert not is_HDN("..foo")
        assert not is_HDN("foo.")

    def test_reach(self):
        from mechanize._clientcookie import reach
        assert reach("www.acme.com") == ".acme.com"
        assert reach("acme.com") == "acme.com"
        assert reach("acme.local") == ".local"
        assert reach(".local") == ".local"
        assert reach(".com") == ".com"
        assert reach(".") == "."
        assert reach("") == ""
        assert reach("192.168.0.1") == "192.168.0.1"

    def test_domain_match(self):
        from mechanize._clientcookie import domain_match, user_domain_match
        assert domain_match("192.168.1.1", "192.168.1.1")
        assert not domain_match("192.168.1.1", ".168.1.1")
        assert domain_match("x.y.com", "x.Y.com")
        assert domain_match("x.y.com", ".Y.com")
        assert not domain_match("x.y.com", "Y.com")
        assert domain_match("a.b.c.com", ".c.com")
        assert not domain_match(".c.com", "a.b.c.com")
        assert domain_match("example.local", ".local")
        assert not domain_match("blah.blah", "")
        assert not domain_match("", ".rhubarb.rhubarb")
        assert domain_match("", "")

        assert user_domain_match("acme.com", "acme.com")
        assert not user_domain_match("acme.com", ".acme.com")
        assert user_domain_match("rhubarb.acme.com", ".acme.com")
        assert user_domain_match("www.rhubarb.acme.com", ".acme.com")
        assert user_domain_match("x.y.com", "x.Y.com")
        assert user_domain_match("x.y.com", ".Y.com")
        assert not user_domain_match("x.y.com", "Y.com")
        assert user_domain_match("y.com", "Y.com")
        assert not user_domain_match(".y.com", "Y.com")
        assert user_domain_match(".y.com", ".Y.com")
        assert user_domain_match("x.y.com", ".com")
        assert not user_domain_match("x.y.com", "com")
        assert not user_domain_match("x.y.com", "m")
        assert not user_domain_match("x.y.com", ".m")
        assert not user_domain_match("x.y.com", "")
        assert not user_domain_match("x.y.com", ".")
        assert user_domain_match("192.168.1.1", "192.168.1.1")
        # not both HDNs, so must string-compare equal to match
        assert not user_domain_match("192.168.1.1", ".168.1.1")
        assert not user_domain_match("192.168.1.1", ".")
        # empty string is a special case
        assert not user_domain_match("192.168.1.1", "")

    def test_wrong_domain(self):
        """Cookies whose ERH does not domain-match the domain are rejected.

        ERH = effective request-host.

        """
        # XXX far from complete
        from mechanize import CookieJar
        c = CookieJar()
        interact_2965(c, "http://www.nasty.com/",
                      'foo=bar; domain=friendly.org; Version="1"')
        assert len(c) == 0

    def test_strict_domain(self):
        # Cookies whose domain is a country-code tld like .co.uk should
        # not be set if CookiePolicy.strict_domain is true.
        from mechanize import CookieJar, DefaultCookiePolicy

        cp = DefaultCookiePolicy(strict_domain=True)
        cj = CookieJar(policy=cp)
        interact_netscape(cj, "http://example.co.uk/", 'no=problemo')
        interact_netscape(cj, "http://example.co.uk/",
                          'okey=dokey; Domain=.example.co.uk')
        self.assertEquals(len(cj), 2)
        for pseudo_tld in [".co.uk", ".org.za", ".tx.us", ".name.us"]:
            interact_netscape(cj, "http://example.%s/" % pseudo_tld,
                              'spam=eggs; Domain=.co.uk')
            self.assertEquals(len(cj), 2)
        # XXXX This should be compared with the Konqueror (kcookiejar.cpp) and
        # Mozilla implementations.

    def test_two_component_domain_ns(self):
        # Netscape: .www.bar.com, www.bar.com, .bar.com, bar.com, no domain should
        #  all get accepted, as should .acme.com, acme.com and no domain for
        #  2-component domains like acme.com.
        from mechanize import CookieJar, DefaultCookiePolicy

        c = CookieJar()

        # two-component V0 domain is OK
        interact_netscape(c, "http://foo.net/", 'ns=bar')
        assert len(c) == 1
        assert c._cookies["foo.net"]["/"]["ns"].value == "bar"
        assert interact_netscape(c, "http://foo.net/") == "ns=bar"
        # *will* be returned to any other domain (unlike RFC 2965)...
        assert interact_netscape(c, "http://www.foo.net/") == "ns=bar"
        # ...unless requested otherwise
        pol = DefaultCookiePolicy(
            strict_ns_domain=DefaultCookiePolicy.DomainStrictNonDomain)
        c.set_policy(pol)
        assert interact_netscape(c, "http://www.foo.net/") == ""

        # unlike RFC 2965, even explicit two-component domain is OK,
        # because .foo.net matches foo.net
        interact_netscape(c, "http://foo.net/foo/",
                          'spam1=eggs; domain=foo.net')
        # even if starts with a dot -- in NS rules, .foo.net matches foo.net!
        interact_netscape(c, "http://foo.net/foo/bar/",
                          'spam2=eggs; domain=.foo.net')
        assert len(c) == 3
        assert c._cookies[".foo.net"]["/foo"]["spam1"].value == "eggs"
        assert c._cookies[".foo.net"]["/foo/bar"]["spam2"].value == "eggs"
        assert interact_netscape(c, "http://foo.net/foo/bar/") == \
            "spam2=eggs; spam1=eggs; ns=bar"

        # top-level domain is too general
        interact_netscape(c, "http://foo.net/", 'nini="ni"; domain=.net')
        assert len(c) == 3

        # Netscape protocol doesn't allow non-special top level domains (such
        # as co.uk) in the domain attribute unless there are at least three
        # dots in it.
        # Oh yes it does!  Real implementations don't check this, and real
        # cookies (of course) rely on that behaviour.
        interact_netscape(c, "http://foo.co.uk", 'nasty=trick; domain=.co.uk')
        ##         assert len(c) == 2
        assert len(c) == 4

    def test_two_component_domain_rfc2965(self):
        from mechanize import CookieJar, DefaultCookiePolicy

        pol = DefaultCookiePolicy(rfc2965=True)
        c = CookieJar(pol)

        # two-component V1 domain is OK
        interact_2965(c, "http://foo.net/", 'foo=bar; Version="1"')
        assert len(c) == 1
        assert c._cookies["foo.net"]["/"]["foo"].value == "bar"
        assert interact_2965(c, "http://foo.net/") == "$Version=1; foo=bar"
        # won't be returned to any other domain (because domain was implied)
        assert interact_2965(c, "http://www.foo.net/") == ""

        # unless domain is given explicitly, because then it must be
        # rewritten to start with a dot: foo.net --> .foo.net, which does
        # not domain-match foo.net
        interact_2965(c, "http://foo.net/foo",
                      'spam=eggs; domain=foo.net; path=/foo; Version="1"')
        assert len(c) == 1
        assert interact_2965(c, "http://foo.net/foo") == "$Version=1; foo=bar"

        # explicit foo.net from three-component domain www.foo.net *does* get
        # set, because .foo.net domain-matches .foo.net
        interact_2965(c, "http://www.foo.net/foo/",
                      'spam=eggs; domain=foo.net; Version="1"')
        assert c._cookies[".foo.net"]["/foo/"]["spam"].value == "eggs"
        assert len(c) == 2
        assert interact_2965(c, "http://foo.net/foo/") == "$Version=1; foo=bar"
        assert interact_2965(c, "http://www.foo.net/foo/") == \
            '$Version=1; spam=eggs; $Domain="foo.net"'

        # top-level domain is too general
        interact_2965(c, "http://foo.net/",
                      'ni="ni"; domain=".net"; Version="1"')
        assert len(c) == 2

        # RFC 2965 doesn't require blocking this
        interact_2965(c, "http://foo.co.uk/",
                      'nasty=trick; domain=.co.uk; Version="1"')
        assert len(c) == 3

    def test_domain_allow(self):
        from mechanize import CookieJar, DefaultCookiePolicy

        c = CookieJar(policy=DefaultCookiePolicy(
            blocked_domains=["acme.com"], allowed_domains=["www.acme.com"]))

        req = Request("http://acme.com/")
        headers = ["Set-Cookie: CUSTOMER=WILE_E_COYOTE; path=/"]
        res = FakeResponse(headers, "http://acme.com/")
        c.extract_cookies(res, req)
        assert len(c) == 0

        req = Request("http://www.acme.com/")
        res = FakeResponse(headers, "http://www.acme.com/")
        c.extract_cookies(res, req)
        assert len(c) == 1

        req = Request("http://www.coyote.com/")
        res = FakeResponse(headers, "http://www.coyote.com/")
        c.extract_cookies(res, req)
        assert len(c) == 1

        # set a cookie with non-allowed domain...
        req = Request("http://www.coyote.com/")
        res = FakeResponse(headers, "http://www.coyote.com/")
        cookies = c.make_cookies(res, req)
        c.set_cookie(cookies[0])
        assert len(c) == 2
        # ... and check is doesn't get returned
        c.add_cookie_header(req)
        assert not req.has_header("Cookie")

    def test_domain_block(self):
        from mechanize import CookieJar, DefaultCookiePolicy

        #import logging; logging.getLogger("mechanize").setLevel(logging.DEBUG)

        pol = DefaultCookiePolicy(rfc2965=True, blocked_domains=[".acme.com"])
        c = CookieJar(policy=pol)
        headers = ["Set-Cookie: CUSTOMER=WILE_E_COYOTE; path=/"]

        req = Request("http://www.acme.com/")
        res = FakeResponse(headers, "http://www.acme.com/")
        c.extract_cookies(res, req)
        assert len(c) == 0

        pol.set_blocked_domains(["acme.com"])
        c.extract_cookies(res, req)
        assert len(c) == 1

        c.clear()
        req = Request("http://www.roadrunner.net/")
        res = FakeResponse(headers, "http://www.roadrunner.net/")
        c.extract_cookies(res, req)
        assert len(c) == 1
        req = Request("http://www.roadrunner.net/")
        c.add_cookie_header(req)
        assert (req.has_header("Cookie") and req.has_header("Cookie2"))

        c.clear()
        pol.set_blocked_domains([".acme.com"])
        c.extract_cookies(res, req)
        assert len(c) == 1

        # set a cookie with blocked domain...
        req = Request("http://www.acme.com/")
        res = FakeResponse(headers, "http://www.acme.com/")
        cookies = c.make_cookies(res, req)
        c.set_cookie(cookies[0])
        assert len(c) == 2
        # ... and check it doesn't get returned
        c.add_cookie_header(req)
        assert not req.has_header("Cookie")

    def test_secure(self):
        from mechanize import CookieJar, DefaultCookiePolicy

        for ns in True, False:
            for whitespace in " ", "":
                c = CookieJar()
                if ns:
                    pol = DefaultCookiePolicy(rfc2965=False)
                    int = interact_netscape
                    vs = ""
                else:
                    pol = DefaultCookiePolicy(rfc2965=True)
                    int = interact_2965
                    vs = "; Version=1"
                c.set_policy(pol)
                url = "http://www.acme.com/"
                int(c, url, "foo1=bar%s%s" % (vs, whitespace))
                int(c, url, "foo2=bar%s; secure%s" % (vs, whitespace))
                assert not c._cookies["www.acme.com"]["/"]["foo1"].secure, \
                    "non-secure cookie registered secure"
                assert c._cookies["www.acme.com"]["/"]["foo2"].secure, \
                    "secure cookie registered non-secure"

    def test_quote_cookie_value(self):
        from mechanize import CookieJar, DefaultCookiePolicy
        c = CookieJar(policy=DefaultCookiePolicy(rfc2965=True))
        interact_2965(c, "http://www.acme.com/", r'foo=\b"a"r; Version=1')
        h = interact_2965(c, "http://www.acme.com/")
        assert h == r'$Version=1; foo=\\b\"a\"r'

    def test_missing_final_slash(self):
        # Missing slash from request URL's abs_path should be assumed present.
        from mechanize import CookieJar, Request, DefaultCookiePolicy
        url = "http://www.acme.com"
        c = CookieJar(DefaultCookiePolicy(rfc2965=True))
        interact_2965(c, url, "foo=bar; Version=1")
        req = Request(url)
        assert len(c) == 1
        c.add_cookie_header(req)
        assert req.has_header("Cookie")

    def test_domain_mirror(self):
        from mechanize import CookieJar, DefaultCookiePolicy

        pol = DefaultCookiePolicy(rfc2965=True)

        c = CookieJar(pol)
        url = "http://foo.bar.com/"
        interact_2965(c, url, "spam=eggs; Version=1")
        h = interact_2965(c, url)
        assert h.find( "Domain") == -1, \
            "absent domain returned with domain present"

        c = CookieJar(pol)
        url = "http://foo.bar.com/"
        interact_2965(c, url, 'spam=eggs; Version=1; Domain=.bar.com')
        h = interact_2965(c, url)
        assert h.find('$Domain=".bar.com"') != -1, \
            "domain not returned"

        c = CookieJar(pol)
        url = "http://foo.bar.com/"
        # note missing initial dot in Domain
        interact_2965(c, url, 'spam=eggs; Version=1; Domain=bar.com')
        h = interact_2965(c, url)
        assert h.find('$Domain="bar.com"') != -1, \
            "domain not returned"

    def test_path_mirror(self):
        from mechanize import CookieJar, DefaultCookiePolicy

        pol = DefaultCookiePolicy(rfc2965=True)

        c = CookieJar(pol)
        url = "http://foo.bar.com/"
        interact_2965(c, url, "spam=eggs; Version=1")
        h = interact_2965(c, url)
        assert h.find("Path") == -1, \
            "absent path returned with path present"

        c = CookieJar(pol)
        url = "http://foo.bar.com/"
        interact_2965(c, url, 'spam=eggs; Version=1; Path=/')
        h = interact_2965(c, url)
        assert h.find('$Path="/"') != -1, "path not returned"

    def test_port_mirror(self):
        from mechanize import CookieJar, DefaultCookiePolicy

        pol = DefaultCookiePolicy(rfc2965=True)

        c = CookieJar(pol)
        url = "http://foo.bar.com/"
        interact_2965(c, url, "spam=eggs; Version=1")
        h = interact_2965(c, url)
        assert h.find("Port") == -1, \
            "absent port returned with port present"

        c = CookieJar(pol)
        url = "http://foo.bar.com/"
        interact_2965(c, url, "spam=eggs; Version=1; Port")
        h = interact_2965(c, url)
        assert re.search("\$Port([^=]|$)", h), \
            "port with no value not returned with no value"

        c = CookieJar(pol)
        url = "http://foo.bar.com/"
        interact_2965(c, url, 'spam=eggs; Version=1; Port="80"')
        h = interact_2965(c, url)
        assert h.find('$Port="80"') != -1, \
            "port with single value not returned with single value"

        c = CookieJar(pol)
        url = "http://foo.bar.com/"
        interact_2965(c, url, 'spam=eggs; Version=1; Port="80,8080"')
        h = interact_2965(c, url)
        assert h.find('$Port="80,8080"') != -1, \
            "port with multiple values not returned with multiple values"

    def test_no_return_comment(self):
        from mechanize import CookieJar, DefaultCookiePolicy

        c = CookieJar(DefaultCookiePolicy(rfc2965=True))
        url = "http://foo.bar.com/"
        interact_2965(c, url, 'spam=eggs; Version=1; '
                      'Comment="does anybody read these?"; '
                      'CommentURL="http://foo.bar.net/comment.html"')
        h = interact_2965(c, url)
        assert h.find("Comment") == -1, \
            "Comment or CommentURL cookie-attributes returned to server"

# just pondering security here -- this isn't really a test (yet)
# def test_hack(self):
##         from mechanize import CookieJar

##         c = CookieJar()
# interact_netscape(c, "http://victim.mall.com/",
# 'prefs="foo"')
# interact_netscape(c, "http://cracker.mall.com/",
# 'prefs="bar"; Domain=.mall.com')
# interact_netscape(c, "http://cracker.mall.com/",
# '$Version="1"; Domain=.mall.com')
##         h = interact_netscape(c, "http://victim.mall.com/")
# print h

    def test_Cookie_iterator(self):
        from mechanize import CookieJar, Cookie, DefaultCookiePolicy

        cs = CookieJar(DefaultCookiePolicy(rfc2965=True))
        # add some random cookies
        interact_2965(cs, "http://blah.spam.org/", 'foo=eggs; Version=1; '
                      'Comment="does anybody read these?"; '
                      'CommentURL="http://foo.bar.net/comment.html"')
        interact_netscape(cs, "http://www.acme.com/blah/", "spam=bar; secure")
        interact_2965(cs, "http://www.acme.com/blah/",
                      "foo=bar; secure; Version=1")
        interact_2965(cs, "http://www.acme.com/blah/",
                      "foo=bar; path=/; Version=1")
        interact_2965(cs, "http://www.sol.no",
                      r'bang=wallop; version=1; domain=".sol.no"; '
                      r'port="90,100, 80,8080"; '
                      r'max-age=100; Comment = "Just kidding! (\"|\\\\) "')

        versions = [1, 1, 1, 0, 1]
        names = ["bang", "foo", "foo", "spam", "foo"]
        domains = [
            ".sol.no", "blah.spam.org", "www.acme.com", "www.acme.com",
            "www.acme.com"
        ]
        paths = ["/", "/", "/", "/blah", "/blah/"]

        # sequential iteration
        for i in range(4):
            i = 0
            for c in cs:
                # assert isinstance(c, Cookie)
                assert c.version == versions[i]
                assert c.name == names[i]
                assert c.domain == domains[i]
                assert c.path == paths[i]
                i = i + 1

        self.assertRaises(IndexError, lambda cs=cs: cs[5])

    def test_parse_ns_headers(self):
        from mechanize._headersutil import parse_ns_headers

        # missing domain value (invalid cookie)
        assert parse_ns_headers(["foo=bar; path=/; domain"]) == [[
            ("foo", "bar"), ("path", "/"), ("domain", None), ("version", "0")
        ]]
        # invalid expires value
        assert parse_ns_headers(
            ["foo=bar; expires=Foo Bar 12 33:22:11 2000"]) == \
            [[("foo", "bar"), ("expires", None), ("version", "0")]]
        # missing cookie name (valid cookie)
        assert parse_ns_headers(["foo"]) == [[("foo", None), ("version", "0")]]
        # shouldn't add version if header is empty
        assert parse_ns_headers([""]) == []

    def test_bad_cookie_header(self):
        def cookiejar_from_cookie_headers(headers):
            from mechanize import CookieJar, Request
            c = CookieJar()
            req = Request("http://www.example.com/")
            r = FakeResponse(headers, "http://www.example.com/")
            c.extract_cookies(r, req)
            return c

        # none of these bad headers should cause an exception to be raised
        for headers in [
            ["Set-Cookie: "],  # actually, nothing wrong with this
            ["Set-Cookie2: "],  # ditto
                # missing domain value
            ["Set-Cookie2: a=foo; path=/; Version=1; domain"],
                # bad max-age
            ["Set-Cookie: b=foo; max-age=oops"],
                # bad version
            ["Set-Cookie: b=foo; version=spam"],
        ]:
            c = cookiejar_from_cookie_headers(headers)
            # these bad cookies shouldn't be set
            assert len(c) == 0

        # cookie with invalid expires is treated as session cookie
        headers = ["Set-Cookie: c=foo; expires=Foo Bar 12 33:22:11 2000"]
        c = cookiejar_from_cookie_headers(headers)
        cookie = c._cookies["www.example.com"]["/"]["c"]
        assert cookie.expires is None

        # cookie with unset path should have path=/
        headers = ["Set-Cookie: c=foo; path; expires=Foo Bar 12 33:22:11 2000"]
        c = cookiejar_from_cookie_headers(headers)
        assert ('www.example.com' in c._cookies and
                '/' in c._cookies['www.example.com'])

    def test_cookies_for_request(self):
        from mechanize import CookieJar, Request

        cj = CookieJar()
        interact_netscape(cj, "http://example.com/", "short=path")
        interact_netscape(cj, "http://example.com/longer/path", "longer=path")
        for_short_path = cj.cookies_for_request(Request("http://example.com/"))
        self.assertEquals([cookie.name for cookie in for_short_path],
                          ["short"])
        for_long_path = cj.cookies_for_request(
            Request("http://example.com/longer/path"))
        self.assertEquals([cookie.name for cookie in for_long_path],
                          ["longer", "short"])


class CookieJarPersistenceTests(TempfileTestMixin, unittest.TestCase):

    def _interact(self, cj):
        year_plus_one = time.localtime(time.time())[0] + 1
        interact_2965(cj, "http://www.acme.com/",
                      "foo1=bar; max-age=100; Version=1")
        interact_2965(cj, "http://www.acme.com/",
                      'foo2=bar; port="80"; max-age=100; Discard; Version=1')
        interact_2965(cj, "http://www.acme.com/",
                      "foo3=bar; secure; Version=1")

        expires = "expires=09-Nov-%d 23:12:40 GMT" % (year_plus_one, )
        interact_netscape(cj, "http://www.foo.com/", "fooa=bar; %s" % expires)
        interact_netscape(cj, "http://www.foo.com/",
                          "foob=bar; Domain=.foo.com; %s" % expires)
        interact_netscape(cj, "http://www.foo.com/",
                          "fooc=bar; Domain=www.foo.com; %s" % expires)

    def test_firefox3_cookiejar_restore(self):
        try:
            from mechanize import Firefox3CookieJar
        except ImportError:
            pass
        else:
            from mechanize import DefaultCookiePolicy
            filename = self.mktemp()

            def create_cookiejar():
                hide_experimental_warnings()
                try:
                    cj = Firefox3CookieJar(
                        filename, policy=DefaultCookiePolicy(rfc2965=True))
                finally:
                    reset_experimental_warnings()
                cj.connect()
                return cj

            cj = create_cookiejar()
            self._interact(cj)
            self.assertEquals(len(cj), 6)
            cj.close()
            cj = create_cookiejar()
            self.assert_("name='foo1', value='bar'" in repr(cj))
            self.assertEquals(len(cj), 4)

    def test_firefox3_cookiejar_iteration(self):
        try:
            from mechanize import Firefox3CookieJar
        except ImportError:
            pass
        else:
            from mechanize import DefaultCookiePolicy
            filename = self.mktemp()
            hide_experimental_warnings()
            try:
                cj = Firefox3CookieJar(
                    filename, policy=DefaultCookiePolicy(rfc2965=True))
            finally:
                reset_experimental_warnings()
            cj.connect()
            self._interact(cj)
            summary = "\n".join([str(cookie) for cookie in cj])
            self.assertEquals(summary, """\
<Cookie foo2=bar for www.acme.com:80/>
<Cookie foo3=bar for www.acme.com/>
<Cookie foo1=bar for www.acme.com/>
<Cookie fooa=bar for www.foo.com/>
<Cookie foob=bar for .foo.com/>
<Cookie fooc=bar for .www.foo.com/>""")

    def test_firefox3_cookiejar_clear(self):
        try:
            from mechanize import Firefox3CookieJar
        except ImportError:
            pass
        else:
            from mechanize import DefaultCookiePolicy
            filename = self.mktemp()
            hide_experimental_warnings()
            try:
                cj = Firefox3CookieJar(
                    filename, policy=DefaultCookiePolicy(rfc2965=True))
            finally:
                reset_experimental_warnings()
            cj.connect()
            self._interact(cj)
            cj.clear("www.acme.com", "/", "foo2")

            def summary():
                return "\n".join([str(cookie) for cookie in cj])

            self.assertEquals(summary(), """\
<Cookie foo3=bar for www.acme.com/>
<Cookie foo1=bar for www.acme.com/>
<Cookie fooa=bar for www.foo.com/>
<Cookie foob=bar for .foo.com/>
<Cookie fooc=bar for .www.foo.com/>""")
            cj.clear("www.acme.com")
            self.assertEquals(summary(), """\
<Cookie fooa=bar for www.foo.com/>
<Cookie foob=bar for .foo.com/>
<Cookie fooc=bar for .www.foo.com/>""")
            # if name is given, so must path and domain
            self.assertRaises(
                ValueError, cj.clear, domain=".foo.com", name="foob")
            # nonexistent domain
            self.assertRaises(KeyError, cj.clear, domain=".spam.com")

    def test_firefox3_cookiejar_add_cookie_header(self):
        try:
            from mechanize import Firefox3CookieJar
        except ImportError:
            pass
        else:
            filename = self.mktemp()
            hide_experimental_warnings()
            try:
                cj = Firefox3CookieJar(filename)
            finally:
                reset_experimental_warnings()
            cj.connect()
            # Session cookies (true .discard) and persistent cookies (false
            # .discard) are stored differently.  Check they both get sent.
            year_plus_one = time.localtime(time.time())[0] + 1
            expires = "expires=09-Nov-%d 23:12:40 GMT" % (year_plus_one, )
            interact_netscape(cj, "http://www.foo.com/", "fooa=bar")
            interact_netscape(cj, "http://www.foo.com/",
                              "foob=bar; %s" % expires)
            ca, cb = cj
            self.assert_(ca.discard)
            self.assertFalse(cb.discard)
            request = Request("http://www.foo.com/")
            cj.add_cookie_header(request)
            self.assertEquals(
                request.get_header("Cookie"), "fooa=bar; foob=bar")

    def test_mozilla_cookiejar(self):
        # Save / load Mozilla/Netscape cookie file format.
        from mechanize import MozillaCookieJar, DefaultCookiePolicy
        filename = tempfile.mktemp()
        c = MozillaCookieJar(
            filename, policy=DefaultCookiePolicy(rfc2965=True))
        self._interact(c)

        def save_and_restore(cj, ignore_discard, filename=filename):
            from mechanize import MozillaCookieJar, DefaultCookiePolicy
            try:
                cj.save(ignore_discard=ignore_discard)
                new_c = MozillaCookieJar(
                    filename, DefaultCookiePolicy(rfc2965=True))
                new_c.load(ignore_discard=ignore_discard)
            finally:
                try:
                    os.unlink(filename)
                except OSError:
                    pass
            return new_c

        new_c = save_and_restore(c, True)
        assert len(new_c) == 6  # none discarded
        assert repr(new_c).find("name='foo1', value='bar'") != -1

        new_c = save_and_restore(c, False)
        assert len(new_c) == 4  # 2 of them discarded on save
        assert repr(new_c).find("name='foo1', value='bar'") != -1

    def test_mozilla_cookiejar_embedded_tab(self):
        import _MozillaCookieJar
        _MozillaCookieJar._warn_unhandled_exception = lambda: None
        from mechanize import MozillaCookieJar
        filename = tempfile.mktemp()
        fh = open(filename, "w")
        try:
            fh.write(MozillaCookieJar.header + "\n" +
                     "a.com\tFALSE\t/\tFALSE\t\tname\tval\tstillthevalue\n"
                     "a.com\tFALSE\t/\tFALSE\t\tname2\tvalue\n")
            fh.close()
            cj = MozillaCookieJar(filename)
            cj.revert(ignore_discard=True)
            cookies = cj._cookies["a.com"]["/"]
            self.assertEquals(cookies["name"].value, "val\tstillthevalue")
            self.assertEquals(cookies["name2"].value, "value")
        finally:
            try:
                os.remove(filename)
            except IOError as exc:
                if exc.errno != errno.ENOENT:
                    raise

    def test_mozilla_cookiejar_initial_dot_violation(self):
        from mechanize import MozillaCookieJar, LoadError
        filename = tempfile.mktemp()
        fh = open(filename, "w")
        try:
            fh.write(MozillaCookieJar.header + "\n" +
                     ".a.com\tFALSE\t/\tFALSE\t\tname\tvalue\n")
            fh.close()
            cj = MozillaCookieJar(filename)
            self.assertRaises(LoadError, cj.revert, ignore_discard=True)
        finally:
            try:
                os.remove(filename)
            except IOError as exc:
                if exc.errno != errno.ENOENT:
                    raise


class LWPCookieTests(unittest.TestCase, TempfileTestMixin):
    # Tests taken from libwww-perl, with a few modifications.

    def test_netscape_example_1(self):
        from mechanize import CookieJar, Request, DefaultCookiePolicy

        #-------------------------------------------------------------------
        # First we check that it works for the original example at
        # http://www.netscape.com/newsref/std/cookie_spec.html

        # Client requests a document, and receives in the response:
        #
        #       Set-Cookie: CUSTOMER=WILE_E_COYOTE; path=/; expires=Wednesday, 09-Nov-99 23:12:40 GMT
        #
        # When client requests a URL in path "/" on this server, it sends:
        #
        #       Cookie: CUSTOMER=WILE_E_COYOTE
        #
        # Client requests a document, and receives in the response:
        #
        #       Set-Cookie: PART_NUMBER=ROCKET_LAUNCHER_0001; path=/
        #
        # When client requests a URL in path "/" on this server, it sends:
        #
        #       Cookie: CUSTOMER=WILE_E_COYOTE; PART_NUMBER=ROCKET_LAUNCHER_0001
        #
        # Client receives:
        #
        #       Set-Cookie: SHIPPING=FEDEX; path=/fo
        #
        # When client requests a URL in path "/" on this server, it sends:
        #
        #       Cookie: CUSTOMER=WILE_E_COYOTE; PART_NUMBER=ROCKET_LAUNCHER_0001
        #
        # When client requests a URL in path "/foo" on this server, it sends:
        #
        #       Cookie: CUSTOMER=WILE_E_COYOTE; PART_NUMBER=ROCKET_LAUNCHER_0001; SHIPPING=FEDEX
        #
        # The last Cookie is buggy, because both specifications say that the
        # most specific cookie must be sent first.  SHIPPING=FEDEX is the
        # most specific and should thus be first.

        year_plus_one = time.localtime(time.time())[0] + 1

        headers = []

        c = CookieJar(DefaultCookiePolicy(rfc2965=True))

        # req = Request("http://1.1.1.1/",
        #              headers={"Host": "www.acme.com:80"})
        req = Request(
            "http://www.acme.com:80/", headers={"Host": "www.acme.com:80"})

        headers.append("Set-Cookie: CUSTOMER=WILE_E_COYOTE; path=/ ; "
                       "expires=Wednesday, 09-Nov-%d 23:12:40 GMT" %
                       year_plus_one)
        res = FakeResponse(headers, "http://www.acme.com/")
        c.extract_cookies(res, req)

        req = Request("http://www.acme.com/")
        c.add_cookie_header(req)

        assert (req.get_header("Cookie") == "CUSTOMER=WILE_E_COYOTE" and
                req.get_header("Cookie2") == '$Version="1"')

        headers.append("Set-Cookie: PART_NUMBER=ROCKET_LAUNCHER_0001; path=/")
        res = FakeResponse(headers, "http://www.acme.com/")
        c.extract_cookies(res, req)

        req = Request("http://www.acme.com/foo/bar")
        c.add_cookie_header(req)

        h = req.get_header("Cookie")
        assert (h.find("PART_NUMBER=ROCKET_LAUNCHER_0001") != -1 and
                h.find("CUSTOMER=WILE_E_COYOTE") != -1)

        headers.append('Set-Cookie: SHIPPING=FEDEX; path=/foo')
        res = FakeResponse(headers, "http://www.acme.com")
        c.extract_cookies(res, req)

        req = Request("http://www.acme.com/")
        c.add_cookie_header(req)

        h = req.get_header("Cookie")
        assert (h.find("PART_NUMBER=ROCKET_LAUNCHER_0001") != -1 and
                h.find("CUSTOMER=WILE_E_COYOTE") != -1 and
                not h.find("SHIPPING=FEDEX") != -1)

        req = Request("http://www.acme.com/foo/")
        c.add_cookie_header(req)

        h = req.get_header("Cookie")
        assert (h.find("PART_NUMBER=ROCKET_LAUNCHER_0001") != -1 and
                h.find("CUSTOMER=WILE_E_COYOTE") != -1 and
                h.startswith("SHIPPING=FEDEX;"))

    def test_netscape_example_2(self):
        from mechanize import CookieJar, Request

        # Second Example transaction sequence:
        #
        # Assume all mappings from above have been cleared.
        #
        # Client receives:
        #
        #       Set-Cookie: PART_NUMBER=ROCKET_LAUNCHER_0001; path=/
        #
        # When client requests a URL in path "/" on this server, it sends:
        #
        #       Cookie: PART_NUMBER=ROCKET_LAUNCHER_0001
        #
        # Client receives:
        #
        #       Set-Cookie: PART_NUMBER=RIDING_ROCKET_0023; path=/ammo
        #
        # When client requests a URL in path "/ammo" on this server, it sends:
        #
        #       Cookie: PART_NUMBER=RIDING_ROCKET_0023; PART_NUMBER=ROCKET_LAUNCHER_0001
        #
        #       NOTE: There are two name/value pairs named "PART_NUMBER" due to
        # the inheritance of the "/" mapping in addition to the "/ammo"
        # mapping.

        c = CookieJar()
        headers = []

        req = Request("http://www.acme.com/")
        headers.append("Set-Cookie: PART_NUMBER=ROCKET_LAUNCHER_0001; path=/")
        res = FakeResponse(headers, "http://www.acme.com/")

        c.extract_cookies(res, req)

        req = Request("http://www.acme.com/")
        c.add_cookie_header(req)

        assert (req.get_header("Cookie") == "PART_NUMBER=ROCKET_LAUNCHER_0001")

        headers.append(
            "Set-Cookie: PART_NUMBER=RIDING_ROCKET_0023; path=/ammo")
        res = FakeResponse(headers, "http://www.acme.com/")
        c.extract_cookies(res, req)

        req = Request("http://www.acme.com/ammo")
        c.add_cookie_header(req)

        assert re.search(r"PART_NUMBER=RIDING_ROCKET_0023;\s*"
                         "PART_NUMBER=ROCKET_LAUNCHER_0001",
                         req.get_header("Cookie"))

    def test_ietf_example_1(self):
        from mechanize import CookieJar, DefaultCookiePolicy
        #-------------------------------------------------------------------
        # Then we test with the examples from draft-ietf-http-state-man-mec-03.txt
        #
        # 5.  EXAMPLES

        c = CookieJar(DefaultCookiePolicy(rfc2965=True))

        #
        # 5.1  Example 1
        #
        # Most detail of request and response headers has been omitted.  Assume
        # the user agent has no stored cookies.
        #
        #   1.  User Agent -> Server
        #
        #       POST /acme/login HTTP/1.1
        #       [form data]
        #
        #       User identifies self via a form.
        #
        #   2.  Server -> User Agent
        #
        #       HTTP/1.1 200 OK
        #       Set-Cookie2: Customer="WILE_E_COYOTE"; Version="1"; Path="/acme"
        #
        #       Cookie reflects user's identity.

        cookie = interact_2965(
            c, 'http://www.acme.com/acme/login',
            'Customer="WILE_E_COYOTE"; Version="1"; Path="/acme"')
        assert not cookie

        #
        #   3.  User Agent -> Server
        #
        #       POST /acme/pickitem HTTP/1.1
        #       Cookie: $Version="1"; Customer="WILE_E_COYOTE"; $Path="/acme"
        #       [form data]
        #
        #       User selects an item for ``shopping basket.''
        #
        #   4.  Server -> User Agent
        #
        #       HTTP/1.1 200 OK
        #       Set-Cookie2: Part_Number="Rocket_Launcher_0001"; Version="1";
        #               Path="/acme"
        #
        #       Shopping basket contains an item.

        cookie = interact_2965(c, 'http://www.acme.com/acme/pickitem',
                               'Part_Number="Rocket_Launcher_0001"; '
                               'Version="1"; Path="/acme"')
        assert re.search(
            r'^\$Version="?1"?; Customer="?WILE_E_COYOTE"?; \$Path="/acme"$',
            cookie)

        #
        #   5.  User Agent -> Server
        #
        #       POST /acme/shipping HTTP/1.1
        #       Cookie: $Version="1";
        #               Customer="WILE_E_COYOTE"; $Path="/acme";
        #               Part_Number="Rocket_Launcher_0001"; $Path="/acme"
        #       [form data]
        #
        #       User selects shipping method from form.
        #
        #   6.  Server -> User Agent
        #
        #       HTTP/1.1 200 OK
        #       Set-Cookie2: Shipping="FedEx"; Version="1"; Path="/acme"
        #
        #       New cookie reflects shipping method.

        cookie = interact_2965(c, "http://www.acme.com/acme/shipping",
                               'Shipping="FedEx"; Version="1"; Path="/acme"')

        assert (re.search(r'^\$Version="?1"?;', cookie) and re.search(
            r'Part_Number="?Rocket_Launcher_0001"?;'
            '\s*\$Path="\/acme"', cookie) and re.search(
                r'Customer="?WILE_E_COYOTE"?;\s*\$Path="\/acme"', cookie))

        #
        #   7.  User Agent -> Server
        #
        #       POST /acme/process HTTP/1.1
        #       Cookie: $Version="1";
        #               Customer="WILE_E_COYOTE"; $Path="/acme";
        #               Part_Number="Rocket_Launcher_0001"; $Path="/acme";
        #               Shipping="FedEx"; $Path="/acme"
        #       [form data]
        #
        #       User chooses to process order.
        #
        #   8.  Server -> User Agent
        #
        #       HTTP/1.1 200 OK
        #
        #       Transaction is complete.

        cookie = interact_2965(c, "http://www.acme.com/acme/process")
        assert (re.search(r'Shipping="?FedEx"?;\s*\$Path="\/acme"', cookie) and
                cookie.find("WILE_E_COYOTE") != -1)

        #
        # The user agent makes a series of requests on the origin server, after
        # each of which it receives a new cookie.  All the cookies have the same
        # Path attribute and (default) domain.  Because the request URLs all have
        # /acme as a prefix, and that matches the Path attribute, each request
        # contains all the cookies received so far.

    def test_ietf_example_2(self):
        from mechanize import CookieJar, DefaultCookiePolicy

        # 5.2  Example 2
        #
        # This example illustrates the effect of the Path attribute.  All detail
        # of request and response headers has been omitted.  Assume the user agent
        # has no stored cookies.

        c = CookieJar(DefaultCookiePolicy(rfc2965=True))

        # Imagine the user agent has received, in response to earlier requests,
        # the response headers
        #
        # Set-Cookie2: Part_Number="Rocket_Launcher_0001"; Version="1";
        #         Path="/acme"
        #
        # and
        #
        # Set-Cookie2: Part_Number="Riding_Rocket_0023"; Version="1";
        #         Path="/acme/ammo"

        interact_2965(
            c, "http://www.acme.com/acme/ammo/specific",
            'Part_Number="Rocket_Launcher_0001"; Version="1"; Path="/acme"',
            'Part_Number="Riding_Rocket_0023"; Version="1"; Path="/acme/ammo"')

        # A subsequent request by the user agent to the (same) server for URLs of
        # the form /acme/ammo/...  would include the following request header:
        #
        # Cookie: $Version="1";
        #         Part_Number="Riding_Rocket_0023"; $Path="/acme/ammo";
        #         Part_Number="Rocket_Launcher_0001"; $Path="/acme"
        #
        # Note that the NAME=VALUE pair for the cookie with the more specific Path
        # attribute, /acme/ammo, comes before the one with the less specific Path
        # attribute, /acme.  Further note that the same cookie name appears more
        # than once.

        cookie = interact_2965(c, "http://www.acme.com/acme/ammo/...")
        assert re.search(r"Riding_Rocket_0023.*Rocket_Launcher_0001", cookie)

        # A subsequent request by the user agent to the (same) server for a URL of
        # the form /acme/parts/ would include the following request header:
        #
        # Cookie: $Version="1"; Part_Number="Rocket_Launcher_0001"; $Path="/acme"
        #
        # Here, the second cookie's Path attribute /acme/ammo is not a prefix of
        # the request URL, /acme/parts/, so the cookie does not get forwarded to
        # the server.

        cookie = interact_2965(c, "http://www.acme.com/acme/parts/")
        assert (cookie.find("Rocket_Launcher_0001") != -1 and
                not cookie.find("Riding_Rocket_0023") != -1)

    def test_rejection(self):
        # Test rejection of Set-Cookie2 responses based on domain, path, port.
        from mechanize import LWPCookieJar, DefaultCookiePolicy

        pol = DefaultCookiePolicy(rfc2965=True)

        c = LWPCookieJar(policy=pol)

        # illegal domain (no embedded dots)
        cookie = interact_2965(c, "http://www.acme.com",
                               'foo=bar; domain=".com"; version=1')
        assert not c

        # legal domain
        cookie = interact_2965(c, "http://www.acme.com",
                               'ping=pong; domain="acme.com"; version=1')
        assert len(c) == 1

        # illegal domain (host prefix "www.a" contains a dot)
        cookie = interact_2965(c, "http://www.a.acme.com",
                               'whiz=bang; domain="acme.com"; version=1')
        assert len(c) == 1

        # legal domain
        cookie = interact_2965(c, "http://www.a.acme.com",
                               'wow=flutter; domain=".a.acme.com"; version=1')
        assert len(c) == 2

        # can't partially match an IP-address
        cookie = interact_2965(c, "http://125.125.125.125",
                               'zzzz=ping; domain="125.125.125"; version=1')
        assert len(c) == 2

        # illegal path (must be prefix of request path)
        cookie = interact_2965(c, "http://www.sol.no",
                               'blah=rhubarb; domain=".sol.no"; path="/foo"; '
                               'version=1')
        assert len(c) == 2

        # legal path
        cookie = interact_2965(c, "http://www.sol.no/foo/bar",
                               'bing=bong; domain=".sol.no"; path="/foo"; '
                               'version=1')
        assert len(c) == 3

        # illegal port (request-port not in list)
        cookie = interact_2965(c, "http://www.sol.no",
                               'whiz=ffft; domain=".sol.no"; port="90,100"; '
                               'version=1')
        assert len(c) == 3

        # legal port
        cookie = interact_2965(
            c, "http://www.sol.no",
            r'bang=wallop; version=1; domain=".sol.no"; '
            r'port="90,100, 80,8080"; '
            r'max-age=100; Comment = "Just kidding! (\"|\\\\) "')
        assert len(c) == 4

        # port attribute without any value (current port)
        cookie = interact_2965(c, "http://www.sol.no",
                               'foo9=bar; version=1; domain=".sol.no"; port; '
                               'max-age=100;')
        cookie
        assert len(c) == 5

        # encoded path
        # LWP has this test, but unescaping allowed path characters seems
        # like a bad idea, so I think this should fail:
        # cookie = interact_2965(c, "http://www.sol.no/foo/",
        # r'foo8=bar; version=1; path="/%66oo"')
        # but this is OK, because '<' is not an allowed HTTP URL path
        # character:
        interact_2965(c, "http://www.sol.no/<oo/",
                      r'foo8=bar; version=1; path="/%3coo"')
        assert len(c) == 6

        # save and restore
        filename = tempfile.mktemp()

        try:
            c.save(filename, ignore_discard=True)
            old = repr(c)

            c = LWPCookieJar(policy=pol)
            c.load(filename, ignore_discard=True)
        finally:
            try:
                os.unlink(filename)
            except OSError:
                pass

        assert old == repr(c)

    def test_url_encoding(self):
        # Try some URL encodings of the PATHs.
        # (the behaviour here has changed from libwww-perl)
        from mechanize import CookieJar, DefaultCookiePolicy

        c = CookieJar(DefaultCookiePolicy(rfc2965=True))

        interact_2965(c, "http://www.acme.com/foo%2f%25/%3c%3c%0Anew%E5/%E5",
                      "foo  =   bar; version    =   1")

        cookie = interact_2965(
            c, "http://www.acme.com/foo%2f%25/<<%0anew\345/\346\370\345",
            'bar=baz; path="/foo/"; version=1')
        version_re = re.compile(r'^\$version=\"?1\"?', re.I)
        assert (cookie.find("foo=bar") != -1 and version_re.search(cookie))

        cookie = interact_2965(
            c, "http://www.acme.com/foo/%25/<<%0anew\345/\346\370\345")
        assert not cookie

        # unicode URL doesn't raise exception, as it used to!
        cookie = interact_2965(c, u"http://www.acme.com/\xfc")

    def test_netscape_misc(self):
        # Some additional Netscape cookies tests.
        from mechanize import CookieJar, Request

        c = CookieJar()
        headers = []
        req = Request("http://foo.bar.acme.com/foo")

        # Netscape allows a host part that contains dots
        headers.append("Set-Cookie: Customer=WILE_E_COYOTE; domain=.acme.com")
        res = FakeResponse(headers, "http://www.acme.com/foo")
        c.extract_cookies(res, req)

        # and that the domain is the same as the host without adding a leading
        # dot to the domain.  Should not quote even if strange chars are used
        # in the cookie value.
        headers.append("Set-Cookie: PART_NUMBER=3,4; domain=foo.bar.acme.com")
        res = FakeResponse(headers, "http://www.acme.com/foo")
        c.extract_cookies(res, req)

        req = Request("http://foo.bar.acme.com/foo")
        c.add_cookie_header(req)
        assert (req.get_header("Cookie").find("PART_NUMBER=3,4") != -1 and
                req.get_header("Cookie").find("Customer=WILE_E_COYOTE") != -1)

    def test_intranet_domains_2965(self):
        # Test handling of local intranet hostnames without a dot.
        from mechanize import CookieJar, DefaultCookiePolicy

        c = CookieJar(DefaultCookiePolicy(rfc2965=True))
        interact_2965(c, "http://example/",
                      "foo1=bar; PORT; Discard; Version=1;")
        cookie = interact_2965(c, "http://example/",
                               'foo2=bar; domain=".local"; Version=1')
        assert cookie.find("foo1=bar") >= 0

        interact_2965(c, "http://example/", 'foo3=bar; Version=1')
        cookie = interact_2965(c, "http://example/")
        assert cookie.find("foo2=bar") >= 0 and len(c) == 3

    def test_intranet_domains_ns(self):
        from mechanize import CookieJar, DefaultCookiePolicy

        c = CookieJar(DefaultCookiePolicy(rfc2965=False))
        interact_netscape(c, "http://example/", "foo1=bar")
        cookie = interact_netscape(c, "http://example/",
                                   'foo2=bar; domain=.local')
        assert len(c) == 2
        assert cookie.find("foo1=bar") >= 0

        cookie = interact_netscape(c, "http://example/")
        assert cookie.find("foo2=bar") >= 0 and len(c) == 2

    def test_empty_path(self):
        from mechanize import CookieJar, Request, DefaultCookiePolicy

        # Test for empty path
        # Broken web-server ORION/1.3.38 returns to the client response like
        #
        #       Set-Cookie: JSESSIONID=ABCDERANDOM123; Path=
        #
        # ie. with Path set to nothing.
        # In this case, extract_cookies() must set cookie to / (root)
        c = CookieJar(DefaultCookiePolicy(rfc2965=True))
        headers = []

        req = Request("http://www.ants.com/")
        headers.append("Set-Cookie: JSESSIONID=ABCDERANDOM123; Path=")
        res = FakeResponse(headers, "http://www.ants.com/")
        c.extract_cookies(res, req)

        req = Request("http://www.ants.com/")
        c.add_cookie_header(req)

        assert (req.get_header("Cookie") == "JSESSIONID=ABCDERANDOM123" and
                req.get_header("Cookie2") == '$Version="1"')

        # missing path in the request URI
        req = Request("http://www.ants.com:8080")
        c.add_cookie_header(req)

        assert (req.get_header("Cookie") == "JSESSIONID=ABCDERANDOM123" and
                req.get_header("Cookie2") == '$Version="1"')

# The correctness of this test is undefined, in the absence of RFC 2965 errata.
# def test_netscape_rfc2965_interop(self):
# Test mixing of Set-Cookie and Set-Cookie2 headers.
##         from mechanize import CookieJar

# Example from http://www.trip.com/trs/trip/flighttracker/flight_tracker_home.xsl
# which gives up these headers:
##         #
# HTTP/1.1 200 OK
# Connection: close
# Date: Fri, 20 Jul 2001 19:54:58 GMT
# Server: Apache/1.3.19 (Unix) ApacheJServ/1.1.2
# Content-Type: text/html
# Content-Type: text/html; charset=iso-8859-1
# Link: </trip/stylesheet.css>; rel="stylesheet"; type="text/css"
# Servlet-Engine: Tomcat Web Server/3.2.1 (JSP 1.1; Servlet 2.2; Java 1.3.0; SunOS 5.8 sparc; java.vendor=Sun Microsystems Inc.)
# Set-Cookie: trip.appServer=1111-0000-x-024;Domain=.trip.com;Path=/
# Set-Cookie: JSESSIONID=fkumjm7nt1.JS24;Path=/trs
# Set-Cookie2: JSESSIONID=fkumjm7nt1.JS24;Version=1;Discard;Path="/trs"
# Title: TRIP.com Travel - FlightTRACKER
# X-Meta-Description: Trip.com privacy policy
# X-Meta-Keywords: privacy policy

# req = mechanize.Request(
# 'http://www.trip.com/trs/trip/flighttracker/flight_tracker_home.xsl')
##         headers = []
##         headers.append("Set-Cookie: trip.appServer=1111-0000-x-024;Domain=.trip.com;Path=/")
##         headers.append("Set-Cookie: JSESSIONID=fkumjm7nt1.JS24;Path=/trs")
##         headers.append('Set-Cookie2: JSESSIONID=fkumjm7nt1.JS24;Version=1;Discard;Path="/trs"')
# res = FakeResponse(
# headers,
# 'http://www.trip.com/trs/trip/flighttracker/flight_tracker_home.xsl')
# print res

##         c = CookieJar()
##         c.extract_cookies(res, req)
# print c
# print str(c)
# print """Set-Cookie3: trip.appServer="1111-0000-x-024"; path="/"; domain=".trip.com"; path_spec; discard; version=0
# Set-Cookie3: JSESSIONID="fkumjm7nt1.JS24"; path="/trs"; domain="www.trip.com"; path_spec; discard; version=1
# """
# assert c.as_lwp_str() == """Set-Cookie3: trip.appServer="1111-0000-x-024"; path="/"; domain=".trip.com"; path_spec; discard; version=0
# Set-Cookie3: JSESSIONID="fkumjm7nt1.JS24"; path="/trs"; domain="www.trip.com"; path_spec; discard; version=1
# """

    def test_session_cookies(self):
        from mechanize import CookieJar, Request

        year_plus_one = time.localtime(time.time())[0] + 1

        # Check session cookies are deleted properly by
        # CookieJar.clear_session_cookies method

        req = Request('http://www.perlmeister.com/scripts')
        headers = []
        headers.append("Set-Cookie: s1=session;Path=/scripts")
        headers.append("Set-Cookie: p1=perm; Domain=.perlmeister.com;"
                       "Path=/;expires=Fri, 02-Feb-%d 23:24:20 GMT" %
                       year_plus_one)
        headers.append("Set-Cookie: p2=perm;Path=/;expires=Fri, "
                       "02-Feb-%d 23:24:20 GMT" % year_plus_one)
        headers.append("Set-Cookie: s2=session;Path=/scripts;"
                       "Domain=.perlmeister.com")
        headers.append('Set-Cookie2: s3=session;Version=1;Discard;Path="/"')
        res = FakeResponse(headers, 'http://www.perlmeister.com/scripts')

        c = CookieJar()
        c.extract_cookies(res, req)
        # How many session/permanent cookies do we have?
        counter = {
            "session_after": 0,
            "perm_after": 0,
            "session_before": 0,
            "perm_before": 0
        }
        for cookie in c:
            key = "%s_before" % cookie.value
            counter[key] = counter[key] + 1
        c.clear_session_cookies()
        # How many now?
        for cookie in c:
            key = "%s_after" % cookie.value
            counter[key] = counter[key] + 1

        assert not (
            # a permanent cookie got lost accidently
            counter["perm_after"] != counter["perm_before"] or
            # a session cookie hasn't been cleared
            counter["session_after"] != 0 or
            # we didn't have session cookies in the first place
            counter["session_before"] == 0)

if __name__ == "__main__":
    import unittest
    unittest.main()
