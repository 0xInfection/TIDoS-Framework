#!/usr/bin/env python

# These tests access the network.  python test.py runs a local test server and
# doesn't try to fetch anything over the internet, since the few tests here
# that do that are disabled by default since they have test tag "internet".

# thanks Moof (aka Giles Antonio Radford) for some of these

from __future__ import print_function
import copy
import errno
import os
import socket
import subprocess
import sys
import unittest
import urllib
import urllib2

import mechanize
from mechanize import CookieJar, HTTPCookieProcessor, \
    HTTPRefreshProcessor, \
    HTTPEquivProcessor, HTTPRedirectHandler
from mechanize._rfc3986 import urljoin
from mechanize._util import read_file, write_file
import mechanize._opener
import mechanize._rfc3986
import mechanize._sockettimeout
import mechanize._testcase


# from cookielib import CookieJar
# from urllib2 import build_opener, install_opener, urlopen
# from urllib2 import HTTPCookieProcessor, HTTPHandler

# from mechanize import CreateBSDDBCookieJar

# import logging
# logger = logging.getLogger("mechanize")
# logger.addHandler(logging.StreamHandler(sys.stdout))
# logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.INFO)


class TestCase(mechanize._testcase.TestCase):

    # testprogram sets self.no_proxies on each TestCase to request explicitly
    # setting proxies so that http*_proxy environment variables are ignored

    def _configure_user_agent(self, ua):
        if self.no_proxies:
            ua.set_proxies({})

    def make_browser(self):
        browser = mechanize.Browser()
        self._configure_user_agent(browser)
        return browser

    def make_user_agent(self):
        ua = mechanize.UserAgent()
        self._configure_user_agent(ua)
        return ua

    def build_opener(self, handlers=(), build_opener=None):
        handlers += (mechanize.ProxyHandler(proxies={}),)
        if build_opener is None:
            build_opener = mechanize.build_opener
        return build_opener(*handlers)

    def setUp(self):
        mechanize._testcase.TestCase.setUp(self)
        self.test_uri = urljoin(self.uri, "test_fixtures")
        self.server = self.get_cached_fixture("server")
        if self.no_proxies:
            old_opener_m = mechanize._opener._opener
            old_opener_u = urllib2._opener
            mechanize.install_opener(mechanize.build_opener(
                mechanize.ProxyHandler(proxies={})))
            urllib2.install_opener(urllib2.build_opener(
                urllib2.ProxyHandler(proxies={})))

            def revert_install():
                mechanize.install_opener(old_opener_m)
                urllib2.install_opener(old_opener_u)
            self.add_teardown(revert_install)


def sanepathname2url(path):
    urlpath = urllib.pathname2url(path)
    if os.name == "nt" and urlpath.startswith("///"):
        urlpath = urlpath[2:]
    # XXX don't ask me about the mac...
    return urlpath


class FtpTestCase(TestCase):

    def test_ftp(self):
        server = self.get_cached_fixture("ftp_server")
        browser = self.make_browser()
        path = self.make_temp_dir(dir_=server.root_path)
        file_path = os.path.join(path, "stuff")
        data = "data\nmore data"
        write_file(file_path, data)
        relative_path = os.path.join(os.path.basename(path), "stuff")
        r = browser.open("ftp://anon@localhost:%s/%s" %
                         (server.port, relative_path.replace(os.sep, '/')))
        self.assertEqual(r.read(), data)


class SocketTimeoutTest(TestCase):

    # the timeout tests in this module aren't full functional tests: in order
    # to speed things up, don't actually call .settimeout on the socket.  XXX
    # allow running the tests against a slow server with a real timeout

    def _monkey_patch_socket(self):
        class Delegator(object):

            def __init__(self, delegate):
                self._delegate = delegate

            def __getattr__(self, name):
                return getattr(self._delegate, name)

        assertEquals = self.assertEquals

        class TimeoutLog(object):
            AnyValue = object()

            def __init__(self):
                self._nr_sockets = 0
                self._timeouts = []
                self.start()

            def start(self):
                self._monitoring = True

            def stop(self):
                self._monitoring = False

            def socket_created(self):
                if self._monitoring:
                    self._nr_sockets += 1

            def settimeout_called(self, timeout):
                if self._monitoring:
                    self._timeouts.append(timeout)

            def verify(self, value=AnyValue):
                if sys.version_info[:2] < (2, 6):
                    # per-connection timeout not supported in Python 2.5
                    self.verify_default()
                else:
                    assertEquals(len(self._timeouts), self._nr_sockets)
                    if value is not self.AnyValue:
                        for timeout in self._timeouts:
                            assertEquals(timeout, value)

            def verify_default(self):
                assertEquals(len(self._timeouts), 0)

        log = TimeoutLog()

        def settimeout(timeout):
            log.settimeout_called(timeout)
        orig_socket = socket.socket

        def make_socket(*args, **kwds):
            sock = Delegator(orig_socket(*args, **kwds))
            log.socket_created()
            sock.settimeout = settimeout
            return sock
        self.monkey_patch(socket, "socket", make_socket)
        return log


class SimpleTests(SocketTimeoutTest):
    # thanks Moof (aka Giles Antonio Radford)

    def setUp(self):
        super(SimpleTests, self).setUp()
        self.browser = self.make_browser()

    def test_simple(self):
        self.browser.open(self.test_uri)
        self.assertEqual(self.browser.title(), 'Python bits')
        # relative URL
        self.browser.open('/mechanize/')
        self.assertEqual(self.browser.title(), 'mechanize')

    def test_basic_auth(self):
        uri = urljoin(self.uri, "basic_auth")
        self.assertRaises(mechanize.URLError, self.browser.open, uri)
        self.browser.add_password(uri, "john", "john")
        self.browser.open(uri)
        self.assertEqual(self.browser.title(), 'Basic Auth Protected Area')

    def test_digest_auth(self):
        uri = urljoin(self.uri, "digest_auth")
        self.assertRaises(mechanize.URLError, self.browser.open, uri)
        self.browser.add_password(uri, "digestuser", "digestuser")
        self.browser.open(uri)
        self.assertEqual(self.browser.title(), 'Digest Auth Protected Area')

    def test_open_with_default_timeout(self):
        timeout_log = self._monkey_patch_socket()
        self.browser.open(self.test_uri)
        self.assertEqual(self.browser.title(), 'Python bits')
        timeout_log.verify_default()

    def test_open_with_timeout(self):
        timeout_log = self._monkey_patch_socket()
        timeout = 10.
        self.browser.open(self.test_uri, timeout=timeout)
        self.assertEqual(self.browser.title(), 'Python bits')
        timeout_log.verify(timeout)

    def test_urlopen_with_default_timeout(self):
        timeout_log = self._monkey_patch_socket()
        response = mechanize.urlopen(self.test_uri)
        self.assert_contains(response.read(), "Python bits")
        timeout_log.verify_default()

    def test_urlopen_with_timeout(self):
        timeout_log = self._monkey_patch_socket()
        timeout = 10.
        response = mechanize.urlopen(self.test_uri, timeout=timeout)
        self.assert_contains(response.read(), "Python bits")
        timeout_log.verify(timeout)

    def test_redirect_with_timeout(self):
        timeout_log = self._monkey_patch_socket()
        timeout = 10.
        # 301 redirect due to missing final '/'
        req = mechanize.Request(urljoin(self.test_uri, "test_fixtures"),
                                timeout=timeout)
        r = self.browser.open(req)
        self.assert_("GeneralFAQ.html" in r.read(2048))
        timeout_log.verify(timeout)

    def test_302_and_404(self):
        # the combination of 302 and 404 (/redirected is configured to redirect
        # to a non-existent URL /nonexistent) has caused problems in the past
        # due to accidental double-wrapping of the error response
        self.assertRaises(
            mechanize.HTTPError,
            self.browser.open, urljoin(self.uri, "/redirected"),
        )

    def test_reread(self):
        # closing response shouldn't stop methods working (this happens also to
        # be true for e.g. mechanize.OpenerDirector when mechanize's own
        # handlers are in use, but is guaranteed to be true for
        # mechanize.Browser)
        r = self.browser.open(self.uri)
        data = r.read()
        r.close()
        r.seek(0)
        self.assertEqual(r.read(), data)
        self.assertEqual(self.browser.response().read(), data)

    def test_error_recovery(self):
        self.assertRaises(mechanize.URLError, self.browser.open,
                          'file:///c|thisnoexistyiufheiurgbueirgbue')
        self.browser.open(self.test_uri)
        self.assertEqual(self.browser.title(), 'Python bits')

    def test_redirect(self):
        # 301 redirect due to missing final '/'

        class ObservingHandler(mechanize.BaseHandler):

            def __init__(self):
                self.codes = []

            def http_response(self, request, response):
                self.codes.append(response.code)
                return response

        self.browser.add_handler(ObservingHandler())
        for br in self.browser, copy.copy(self.browser):
            r = br.open(urljoin(self.uri, "redirected_good"))
            self.assertEqual(r.code, 200)
            self.assert_("GeneralFAQ.html" in r.read(2048))
            self.assertEqual([
                [c for c in h.codes if c == 302]
                for h in br.handlers_by_class(ObservingHandler)], [[302]])

    def test_refresh(self):
        def refresh_request(seconds):
            uri = urljoin(self.uri, "/cgi-bin/cookietest.cgi")
            val = urllib.quote_plus('%d; url="%s"' % (seconds, self.uri))
            return uri + ("?refresh=%s" % val)
        self.browser.set_handle_refresh(True, honor_time=False)
        r = self.browser.open(refresh_request(5))
        self.assertEqual(r.geturl(), self.uri)
        # Set a maximum refresh time of 30 seconds (these long refreshes tend
        # to be there only because the website owner wants you to see the
        # latest news, or whatever -- they're not essential to the operation of
        # the site, and not really useful or appropriate when scraping).
        refresh_uri = refresh_request(60)
        self.browser.set_handle_refresh(True, max_time=30., honor_time=True)
        r = self.browser.open(refresh_uri)
        self.assertEqual(r.geturl(), refresh_uri)
        # allow long refreshes (but don't actually wait 60 seconds)
        self.browser.set_handle_refresh(True, max_time=None, honor_time=False)
        r = self.browser.open(refresh_request(60))
        self.assertEqual(r.geturl(), self.uri)

    def test_file_url(self):
        url = "file://%s" % sanepathname2url(
            os.path.abspath(os.path.join("test", "test_functional.py")))
        r = self.browser.open(url)
        self.assert_("this string appears in this file ;-)" in r.read())

    def test_open_local_file(self):
        # Since the file: URL scheme is not well standardised, Browser has a
        # special method to open files by name, for convenience:
        path = os.path.join("test", "test_functional.py")
        response = self.browser.open_local_file(path)
        self.assertIn("this string appears in this file ;-)",
                      response.get_data())

    def test_open_novisit(self):
        def test_state(br):
            self.assert_(br.request is None)
            self.assert_(br.response() is None)
            self.assertRaises(mechanize.BrowserStateError, br.back)
        test_state(self.browser)
        uri = urljoin(self.uri, "test_fixtures")
        # note this involves a redirect, which should itself be non-visiting
        r = self.browser.open_novisit(uri)
        test_state(self.browser)
        self.assert_("GeneralFAQ.html" in r.read(2048))

        # Request argument instead of URL
        r = self.browser.open_novisit(mechanize.Request(uri))
        test_state(self.browser)
        self.assert_("GeneralFAQ.html" in r.read(2048))

    def test_non_seekable(self):
        # check everything still works without response_seek_wrapper and
        # the .seek() method on response objects
        ua = self.make_user_agent()
        ua.set_seekable_responses(False)
        ua.set_handle_equiv(False)
        response = ua.open(self.test_uri)
        self.failIf(hasattr(response, "seek"))
        data = response.read()
        self.assert_("Python bits" in data)


class ResponseTests(TestCase):

    def test_seek(self):
        br = self.make_browser()
        r = br.open(self.uri)
        html = r.read()
        r.seek(0)
        self.assertEqual(r.read(), html)

    def test_seekable_response_opener(self):
        build_opener = mechanize.OpenerFactory(
            mechanize.SeekableResponseOpener).build_opener
        opener = self.build_opener(build_opener=build_opener)
        r = opener.open(urljoin(self.uri, "test_fixtures/cctest2.txt"))
        r.read()
        r.seek(0)
        self.assertEqual(r.read(),
                         r.get_data(),
                         "Hello ClientCookie functional test suite.\n")

    def test_seek_wrapper_class_name(self):
        opener = self.make_user_agent()
        opener.set_seekable_responses(True)
        try:
            opener.open(urljoin(self.uri, "nonexistent"))
        except mechanize.HTTPError as exc:
            self.assert_("HTTPError instance" in repr(exc))

    def test_no_seek(self):
        # should be possible to turn off UserAgent's .seek() functionality
        def check_no_seek(opener):
            r = opener.open(urljoin(self.uri, "test_fixtures/cctest2.txt"))
            self.assert_(not hasattr(r, "seek"))
            try:
                opener.open(urljoin(self.uri, "nonexistent"))
            except mechanize.HTTPError as exc:
                self.assert_(not hasattr(exc, "seek"))

        # mechanize.UserAgent
        opener = self.make_user_agent()
        opener.set_handle_equiv(False)
        opener.set_seekable_responses(False)
        opener.set_debug_http(False)
        check_no_seek(opener)

        # mechanize.OpenerDirector
        opener = self.build_opener()
        check_no_seek(opener)

    def test_consistent_seek(self):
        # if we explicitly request that returned response objects have the
        # .seek() method, then raised HTTPError exceptions should also have the
        # .seek() method
        def check(opener, excs_also):
            r = opener.open(urljoin(self.uri, "test_fixtures/cctest2.txt"))
            data = r.read()
            r.seek(0)
            self.assertEqual(data, r.read(), r.get_data())
            try:
                opener.open(urljoin(self.uri, "nonexistent"))
            except mechanize.HTTPError as exc:
                data = exc.read()
                if excs_also:
                    exc.seek(0)
                    self.assertEqual(data, exc.read(), exc.get_data())
            else:
                self.assert_(False)

        opener = self.make_user_agent()
        opener.set_debug_http(False)

        # Here, only the .set_handle_equiv() causes .seek() to be present, so
        # exceptions don't necessarily support the .seek() method (and do not,
        # at present).
        opener.set_handle_equiv(True)
        opener.set_seekable_responses(False)
        check(opener, excs_also=False)

        # Here, (only) the explicit .set_seekable_responses() causes .seek() to
        # be present (different mechanism from .set_handle_equiv()).  Since
        # there's an explicit request, ALL responses are seekable, even
        # exception responses (HTTPError instances).
        opener.set_handle_equiv(False)
        opener.set_seekable_responses(True)
        check(opener, excs_also=True)

    def test_set_response(self):
        br = self.make_browser()
        r = br.open(self.test_uri)
        html = r.read()
        self.assertEqual(br.title(), "Python bits")

        newhtml = """<html><body><a href="spam">click me</a></body></html>"""

        r.set_data(newhtml)
        self.assertEqual(r.read(), newhtml)
        self.assertEqual(br.response().read(), html)
        br.response().set_data(newhtml)
        self.assertEqual(br.response().read(), html)
        self.assertEqual(list(br.links())[0].url, "http://sourceforge.net/")

        br.set_response(r)
        self.assertEqual(br.response().read(), newhtml)
        self.assertEqual(list(br.links())[0].url, "spam")

    def test_new_response(self):
        br = self.make_browser()
        data = ("<html><head><title>Test</title></head>"
                "<body><p>Hello.</p></body></html>")
        response = mechanize.make_response(
            data,
            [("Content-type", "text/html")],
            "http://example.com/",
            200,
            "OK")
        br.set_response(response)
        self.assertEqual(br.response().get_data(), data)

    def hidden_test_close_pickle_load(self):
        print ("Test test_close_pickle_load is expected to fail unless Python "
               "standard library patch http://python.org/sf/1144636 has been "
               "applied")
        import pickle

        b = self.make_browser()
        r = b.open(urljoin(self.uri, "test_fixtures/cctest2.txt"))
        r.read()

        r.close()
        r.seek(0)
        self.assertEqual(r.read(),
                         "Hello ClientCookie functional test suite.\n")

        HIGHEST_PROTOCOL = -1
        p = pickle.dumps(b, HIGHEST_PROTOCOL)
        b = pickle.loads(p)
        r = b.response()
        r.seek(0)
        self.assertEqual(r.read(),
                         "Hello ClientCookie functional test suite.\n")


class FunctionalTests(SocketTimeoutTest):

    def test_referer(self):
        br = self.make_browser()
        br.set_handle_refresh(True, honor_time=False)
        referer = urljoin(self.uri, "test_fixtures/referertest.html")
        info = urljoin(self.uri, "/cgi-bin/cookietest.cgi")
        r = br.open(info)
        self.assert_(referer not in r.get_data())

        br.open(referer)
        r = br.follow_link(text="Here")
        self.assert_(referer in r.get_data())

    def test_cookies(self):
        # this test page depends on cookies, and an http-equiv refresh
        # cj = CreateBSDDBCookieJar("/home/john/db.db")
        cj = CookieJar()
        handlers = [
            HTTPCookieProcessor(cj),
            HTTPRefreshProcessor(max_time=None, honor_time=False),
            HTTPEquivProcessor(),

            HTTPRedirectHandler(),  # needed for Refresh handling in 2.4.0
            #            HTTPHandler(True),
            #            HTTPRedirectDebugProcessor(),
            #            HTTPResponseDebugProcessor(),
        ]

        opener = self.build_opener(handlers)
        r = opener.open(urljoin(self.uri, "/cgi-bin/cookietest.cgi"))
        data = r.read()
        self.assert_(data.find("Your browser supports cookies!") >= 0)
        self.assertEquals(len(cj), 2)

        # test response.seek() (added by HTTPEquivProcessor)
        r.seek(0)
        samedata = r.read()
        r.close()
        self.assertEquals(samedata, data)

    def test_robots(self):
        plain_opener = self.build_opener(
            [mechanize.HTTPRobotRulesProcessor])
        browser = self.make_browser()
        for opener in plain_opener, browser:
            opener.open(urljoin(self.uri, "robots"))
            self.assertRaises(
                mechanize.RobotExclusionError,
                opener.open, urljoin(self.uri, "norobots"))

    def _check_retrieve(self, url, filename, headers):
        from urllib import urlopen
        self.assertEqual(headers.get('Content-Type'), 'text/html')
        if self.no_proxies:
            proxies = {}
        else:
            proxies = None
        self.assertEqual(read_file(filename),
                         urlopen(url, proxies=proxies).read())

    def test_retrieve_to_named_file(self):
        url = urljoin(self.uri, "/mechanize/")
        test_filename = os.path.join(self.make_temp_dir(), "python.html")
        opener = self.build_opener()
        verif = CallbackVerifier(self)
        filename, headers = opener.retrieve(url, test_filename, verif.callback)
        self.assertEqual(filename, test_filename)
        self._check_retrieve(url, filename, headers)
        self.assert_(os.path.isfile(filename))

    def test_retrieve(self):
        # not passing an explicit filename downloads to a temporary file
        # using a Request object instead of a URL works
        url = urljoin(self.uri, "/mechanize/")
        opener = self.build_opener()
        verif = CallbackVerifier(self)
        request = mechanize.Request(url)
        filename, headers = opener.retrieve(request, reporthook=verif.callback)
        self.assertEquals(request.visit, False)
        self._check_retrieve(url, filename, headers)
        opener.close()
        # closing the opener removed the temporary file
        self.failIf(os.path.isfile(filename))

    def test_urlretrieve(self):
        timeout_log = self._monkey_patch_socket()
        timeout = 10.
        url = urljoin(self.uri, "/mechanize/")
        verif = CallbackVerifier(self)
        filename, headers = mechanize.urlretrieve(url,
                                                  reporthook=verif.callback,
                                                  timeout=timeout)
        timeout_log.stop()
        self._check_retrieve(url, filename, headers)
        timeout_log.verify(timeout)

    def test_reload_read_incomplete(self):
        browser = self.make_browser()
        r1 = browser.open(urljoin(self.uri,
                                  "test_fixtures/mechanize_reload_test.html"))
        # if we don't do anything and go straight to another page, most of the
        # last page's response won't be .read()...
        browser.open(urljoin(self.uri, "mechanize"))
        self.assert_(len(r1.get_data()) < 4097)  # we only .read() a little bit
        # ...so if we then go back, .follow_link() for a link near the end (a
        # few kb in, past the point that always gets read in HTML files because
        # of HEAD parsing) will only work if it causes a .reload()...
        r3 = browser.back()
        browser.follow_link(text="near the end")
        # ... good, no LinkNotFoundError, so we did reload.
        # we have .read() the whole file
        self.assertEqual(len(r3._seek_wrapper__cache.getvalue()), 4202)

# def test_cacheftp(self):
#         from mechanize import CacheFTPHandler, build_opener
#         o = build_opener(CacheFTPHandler())
#         r = o.open("ftp://ftp.python.org/pub/www.python.org/robots.txt")
#         data1 = r.read()
# r.close()
#         r = o.open(
#         "ftp://ftp.python.org/pub/www.python.org/2.3.2/announce.txt")
#         data2 = r.read()
# r.close()
#         self.assert_(data1 != data2)


class CommandFailedError(Exception):

    def __init__(self, message, rc):
        Exception.__init__(self, message)
        self.rc = rc


def get_cmd_stdout(args, **kwargs):
    process = subprocess.Popen(args, stdout=subprocess.PIPE, **kwargs)
    stdout, stderr = process.communicate()
    rc = process.returncode
    if rc != 0:
        raise CommandFailedError(
            "Command failed with return code %i: %s:\n%s" %
            (rc, args, stderr), rc)
    else:
        return stdout


def add_to_path(env, name, value):
    old = env.get(name)
    if old is not None and old != "":
        value = old + ":" + value
    env[name] = value


class CookieJarTests(TestCase):

    def _test_cookiejar(self, make_cookiejar, commit):
        cookiejar = make_cookiejar()
        br = self.make_browser()
        # br.set_debug_http(True)
        br.set_cookiejar(cookiejar)
        br.set_handle_refresh(False)
        url = urljoin(self.uri, "/cgi-bin/cookietest.cgi")
        # no cookie was set on the first request
        html = br.open(url).read()
        self.assertEquals(html.find("Your browser supports cookies!"), -1)
        self.assertEquals(len(cookiejar), 2)
        # ... but now we have the cookie
        html = br.open(url).read()
        self.assertIn("Your browser supports cookies!", html)
        self.assertIn("Received session cookie", html)
        commit(cookiejar)

        # should still have the cookie when we load afresh
        cookiejar = make_cookiejar()
        br.set_cookiejar(cookiejar)
        html = br.open(url).read()
        self.assertIn("Your browser supports cookies!", html)
        self.assertNotIn("Received session cookie", html)

    def test_mozilla_cookiejar(self):
        filename = os.path.join(self.make_temp_dir(), "cookies.txt")

        def make_cookiejar():
            cj = mechanize.MozillaCookieJar(filename=filename)
            try:
                cj.revert()
            except IOError as exc:
                if exc.errno != errno.ENOENT:
                    raise
            return cj

        def commit(cj):
            cj.save()
        self._test_cookiejar(make_cookiejar, commit)


class CallbackVerifier:
    # for .test_urlretrieve()

    def __init__(self, testcase):
        self._count = 0
        self._testcase = testcase

    def callback(self, block_nr, block_size, total_size):
        self._testcase.assertEqual(block_nr, self._count)
        self._count = self._count + 1


if __name__ == "__main__":
    unittest.main()
