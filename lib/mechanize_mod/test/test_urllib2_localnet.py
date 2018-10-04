#!/usr/bin/env python

"""Functional tests from the Python standard library test suite."""

import mimetools
import threading
import urlparse
import mechanize
import BaseHTTPServer
import unittest

from mechanize._testcase import TestCase
from mechanize._urllib2_fork import md5_digest

import testprogram


# Loopback http server infrastructure

class LoopbackHttpServer(BaseHTTPServer.HTTPServer):
    """HTTP server w/ a few modifications that make it useful for
    loopback testing purposes.
    """

    def __init__(self, server_address, RequestHandlerClass):
        BaseHTTPServer.HTTPServer.__init__(self,
                                           server_address,
                                           RequestHandlerClass)

        # Set the timeout of our listening socket really low so
        # that we can stop the server easily.
        self.socket.settimeout(1.0)

    def get_request(self):
        """BaseHTTPServer method, overridden."""

        request, client_address = self.socket.accept()

        # It's a loopback connection, so setting the timeout
        # really low shouldn't affect anything, but should make
        # deadlocks less likely to occur.
        request.settimeout(10.0)

        return (request, client_address)


class LoopbackHttpServerThread(threading.Thread):
    """Stoppable thread that runs a loopback http server."""

    def __init__(self, handle_request=None):
        threading.Thread.__init__(self)
        self._stop = False
        self.ready = threading.Event()
        self._request_handler = None
        if handle_request is None:
            handle_request = self._handle_request
        self.httpd = LoopbackHttpServer(('127.0.0.1', 0), handle_request)
        # print "Serving HTTP on %s port %s" % (self.httpd.server_name,
        #                                      self.httpd.server_port)
        self.port = self.httpd.server_port

    def set_request_handler(self, request_handler):
        self._request_handler = request_handler

    def _handle_request(self, *args, **kwds):
        self._request_handler.handle_request(*args, **kwds)
        return self._request_handler

    def stop(self):
        """Stops the webserver if it's currently running."""

        # Set the stop flag.
        self._stop = True

        self.join()

    def run(self):
        self.ready.set()
        while not self._stop:
            self.httpd.handle_request()

# Authentication infrastructure


class DigestAuthHandler:
    """Handler for performing digest authentication."""

    def __init__(self):
        self._request_num = 0
        self._nonces = []
        self._users = {}
        self._realm_name = "Test Realm"
        self._qop = "auth"

    def set_qop(self, qop):
        self._qop = qop

    def set_users(self, users):
        assert isinstance(users, dict)
        self._users = users

    def set_realm(self, realm):
        self._realm_name = realm

    def _generate_nonce(self):
        self._request_num += 1
        nonce = md5_digest(str(self._request_num))
        self._nonces.append(nonce)
        return nonce

    def _create_auth_dict(self, auth_str):
        first_space_index = auth_str.find(" ")
        auth_str = auth_str[first_space_index + 1:]

        parts = auth_str.split(",")

        auth_dict = {}
        for part in parts:
            name, value = part.split("=")
            name = name.strip()
            if value[0] == '"' and value[-1] == '"':
                value = value[1:-1]
            else:
                value = value.strip()
            auth_dict[name] = value
        return auth_dict

    def _validate_auth(self, auth_dict, password, method, uri):
        final_dict = {}
        final_dict.update(auth_dict)
        final_dict["password"] = password
        final_dict["method"] = method
        final_dict["uri"] = uri
        HA1_str = "%(username)s:%(realm)s:%(password)s" % final_dict
        HA1 = md5_digest(HA1_str)
        HA2_str = "%(method)s:%(uri)s" % final_dict
        HA2 = md5_digest(HA2_str)
        final_dict["HA1"] = HA1
        final_dict["HA2"] = HA2
        response_str = "%(HA1)s:%(nonce)s:%(nc)s:" \
                       "%(cnonce)s:%(qop)s:%(HA2)s" % final_dict
        response = md5_digest(response_str)

        return response == auth_dict["response"]

    def _return_auth_challenge(self, request_handler):
        request_handler.send_response(407, "Proxy Authentication Required")
        request_handler.send_header("Content-Type", "text/html")
        request_handler.send_header(
            'Proxy-Authenticate', 'Digest realm="%s", '
            'qop="%s",'
            'nonce="%s", ' %
            (self._realm_name, self._qop, self._generate_nonce()))
        # XXX: Not sure if we're supposed to add this next header or
        # not.
        #request_handler.send_header('Connection', 'close')
        request_handler.end_headers()
        request_handler.wfile.write("Proxy Authentication Required.")
        return False

    def handle_request(self, request_handler):
        """Performs digest authentication on the given HTTP request
        handler.  Returns True if authentication was successful, False
        otherwise.

        If no users have been set, then digest auth is effectively
        disabled and this method will always return True.
        """

        if len(self._users) == 0:
            return True

        if 'Proxy-Authorization' not in request_handler.headers:
            return self._return_auth_challenge(request_handler)
        else:
            auth_dict = self._create_auth_dict(
                request_handler.headers['Proxy-Authorization']
            )
            if auth_dict["username"] in self._users:
                password = self._users[auth_dict["username"]]
            else:
                return self._return_auth_challenge(request_handler)
            if not auth_dict.get("nonce") in self._nonces:
                return self._return_auth_challenge(request_handler)
            else:
                self._nonces.remove(auth_dict["nonce"])

            auth_validated = False

            # MSIE uses short_path in its validation, but mechanize uses the
            # full path, so we're going to see if either of them works here.

            for path in [request_handler.path, request_handler.short_path]:
                if self._validate_auth(auth_dict,
                                       password,
                                       request_handler.command,
                                       path):
                    auth_validated = True

            if not auth_validated:
                return self._return_auth_challenge(request_handler)
            return True

# Proxy test infrastructure


class FakeProxyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """This is a 'fake proxy' that makes it look like the entire
    internet has gone down due to a sudden zombie invasion.  It main
    utility is in providing us with authentication support for
    testing.
    """

    protocol_version = "HTTP/1.0"

    def __init__(self, digest_auth_handler, *args, **kwargs):
        # This has to be set before calling our parent's __init__(), which will
        # try to call do_GET().
        self.digest_auth_handler = digest_auth_handler
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def log_message(self, format, *args):
        # Uncomment the next line for debugging.
        #sys.stderr.write(format % args)
        pass

    def do_GET(self):
        (scm, netloc, path, params, query, fragment) = urlparse.urlparse(
            self.path, 'http')
        self.short_path = path
        if self.digest_auth_handler.handle_request(self):
            self.send_response(200, "OK")
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write("You've reached %s!<BR>" % self.path)
            self.wfile.write("Our apologies, but our server is down due to "
                             "a sudden zombie invasion.")


def make_started_server(make_request_handler=None):
    server = LoopbackHttpServerThread(make_request_handler)
    server.start()
    server.ready.wait()
    return server


# Test cases


class ProxyAuthTests(TestCase):
    URL = "http://localhost"

    USER = "tester"
    PASSWD = "test123"
    REALM = "TestRealm"

    def _make_server(self, qop="auth"):
        digest_auth_handler = DigestAuthHandler()
        digest_auth_handler.set_users({self.USER: self.PASSWD})
        digest_auth_handler.set_realm(self.REALM)
        digest_auth_handler.set_qop(qop)
        def create_fake_proxy_handler(*args, **kwargs):
            return FakeProxyHandler(digest_auth_handler, *args, **kwargs)
        return make_started_server(create_fake_proxy_handler)

    def setUp(self):
        TestCase.setUp(self)
        fixture_name = "test_urllib2_localnet_ProxyAuthTests_server"
        self.register_context_manager(fixture_name,
                                      testprogram.ServerCM(self._make_server))
        server = self.get_cached_fixture(fixture_name)

        proxy_url = "http://127.0.0.1:%d" % server.port
        handler = mechanize.ProxyHandler({"http": proxy_url})
        self.proxy_digest_handler = mechanize.ProxyDigestAuthHandler()
        self.opener = mechanize.build_opener(
            handler, self.proxy_digest_handler)

    def test_proxy_with_bad_password_raises_httperror(self):
        self.proxy_digest_handler.add_password(self.REALM, self.URL,
                                               self.USER, self.PASSWD + "bad")
        self.assertRaises(mechanize.HTTPError,
                          self.opener.open,
                          self.URL)

    def test_proxy_with_no_password_raises_httperror(self):
        self.assertRaises(mechanize.HTTPError,
                          self.opener.open,
                          self.URL)

    def test_proxy_qop_auth_works(self):
        self.proxy_digest_handler.add_password(self.REALM, self.URL,
                                               self.USER, self.PASSWD)
        result = self.opener.open(self.URL)
        while result.read():
            pass
        result.close()

    def test_proxy_qop_auth_int_works_or_throws_urlerror(self):
        server = self._make_server("auth-int")
        self.add_teardown(lambda: server.stop())
        self.proxy_digest_handler.add_password(self.REALM, self.URL,
                                               self.USER, self.PASSWD)
        try:
            result = self.opener.open(self.URL)
        except mechanize.URLError:
            # It's okay if we don't support auth-int, but we certainly
            # shouldn't receive any kind of exception here other than
            # a URLError.
            result = None
        if result:
            while result.read():
                pass
            result.close()


class RecordingHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    server_version = "TestHTTP/"
    protocol_version = "HTTP/1.0"

    def __init__(self, port, get_next_response,
                 record_request, record_received_headers,
                 *args, **kwds):
        self._port = port
        self._get_next_response = get_next_response
        self._record_request = record_request
        self._record_received_headers = record_received_headers
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args, **kwds)

    def do_GET(self):
        body = self.send_head()
        if body:
            self.wfile.write(body)

    def do_POST(self):
        content_length = self.headers['Content-Length']
        post_data = self.rfile.read(int(content_length))
        self.do_GET()
        self._record_request(post_data)

    def send_head(self):
        self._record_received_headers(self.headers)
        self._record_request(self.path)
        response_code, headers, body = self._get_next_response()

        self.send_response(response_code)

        for (header, value) in headers:
            self.send_header(header, value % self._port)
        if body:
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            return body
        self.end_headers()

    def log_message(self, *args):
        pass


class FakeHTTPRequestHandler(object):

    def __init__(self, port, responses):
        self.port = port
        self._responses = responses
        self.requests = []
        self.received_headers = None

    def _get_next_response(self):
        return self._responses.pop(0)

    def _record_request(self, request):
        self.requests.append(request)

    def _record_received_headers(self, headers):
        self.received_headers = headers

    def handle_request(self, *args, **kwds):
        RecordingHTTPRequestHandler(
            self.port, self._get_next_response,
            self._record_request, self._record_received_headers,
            *args, **kwds)


class TestUrlopen(TestCase):
    """Tests mechanize.urlopen using the network.

    These tests are not exhaustive.  Assuming that testing using files does a
    good job overall of some of the basic interface features.  There are no
    tests exercising the optional 'data' and 'proxies' arguments.  No tests
    for transparent redirection have been written.
    """

    fixture_name = "test_urllib2_localnet_TestUrlopen_server"

    def setUp(self):
        TestCase.setUp(self)
        self.register_context_manager(
            self.fixture_name, testprogram.ServerCM(make_started_server))

    def get_server(self):
        return self.get_cached_fixture(self.fixture_name)

    def _make_request_handler(self, responses):
        server = self.get_server()
        handler = FakeHTTPRequestHandler(server.port, responses)
        server.set_request_handler(handler)
        return handler

    def test_redirection(self):
        expected_response = 'We got here...'
        responses = [
            (302, [('Location', 'http://localhost:%s/somewhere_else')], ''),
            (200, [], expected_response)
        ]

        handler = self._make_request_handler(responses)

        f = mechanize.urlopen('http://localhost:%s/' % handler.port)
        data = f.read()
        f.close()

        self.assertEquals(data, expected_response)
        self.assertEquals(handler.requests, ['/', '/somewhere_else'])

    def test_404(self):
        expected_response = 'Bad bad bad...'
        handler = self._make_request_handler([(404, [], expected_response)])

        try:
            mechanize.urlopen('http://localhost:%s/weeble' % handler.port)
        except mechanize.URLError as f:
            pass
        else:
            self.fail('404 should raise URLError')

        data = f.read()
        f.close()

        self.assertEquals(data, expected_response)
        self.assertEquals(handler.requests, ['/weeble'])

    def test_200(self):
        expected_response = 'pycon 2008...'
        handler = self._make_request_handler([(200, [], expected_response)])

        f = mechanize.urlopen('http://localhost:%s/bizarre' % handler.port)
        data = f.read()
        f.close()

        self.assertEquals(data, expected_response)
        self.assertEquals(handler.requests, ['/bizarre'])

    def test_200_with_parameters(self):
        expected_response = 'pycon 2008...'
        handler = self._make_request_handler([(200, [], expected_response)])

        f = mechanize.urlopen('http://localhost:%s/bizarre' % handler.port,
                              'get=with_feeling')
        data = f.read()
        f.close()

        self.assertEquals(data, expected_response)
        self.assertEquals(handler.requests, ['/bizarre', 'get=with_feeling'])

    def test_sending_headers(self):
        handler = self._make_request_handler([(200, [], "we don't care")])

        req = mechanize.Request("http://localhost:%s/" % handler.port,
                                headers={'Range': 'bytes=20-39'})
        mechanize.urlopen(req)
        self.assertEqual(handler.received_headers['Range'], 'bytes=20-39')

    def test_basic(self):
        handler = self._make_request_handler([(200, [], "we don't care")])

        open_url = mechanize.urlopen("http://localhost:%s" % handler.port)
        for attr in ("read", "close", "info", "geturl"):
            self.assertTrue(hasattr(open_url, attr), "object returned from "
                            "urlopen lacks the %s attribute" % attr)
        try:
            self.assertTrue(open_url.read(), "calling 'read' failed")
        finally:
            open_url.close()

    def test_info(self):
        handler = self._make_request_handler([(200, [], "we don't care")])

        open_url = mechanize.urlopen("http://localhost:%s" % handler.port)
        info_obj = open_url.info()
        self.assertTrue(isinstance(info_obj, mimetools.Message),
                        "object returned by 'info' is not an instance of "
                        "mimetools.Message")
        self.assertEqual(info_obj.getsubtype(), "plain")

    def test_geturl(self):
        # Make sure same URL as opened is returned by geturl.
        handler = self._make_request_handler([(200, [], "we don't care")])

        open_url = mechanize.urlopen("http://localhost:%s" % handler.port)
        url = open_url.geturl()
        self.assertEqual(url, "http://localhost:%s" % handler.port)

    def test_bad_address(self):
        # Make sure proper exception is raised when connecting to a bogus
        # address.
        self.assertRaises(IOError,
                          # Given that both VeriSign and various ISPs have in
                          # the past or are presently hijacking various invalid
                          # domain name requests in an attempt to boost traffic
                          # to their own sites, finding a domain name to use
                          # for this test is difficult.  RFC2606 leads one to
                          # believe that '.invalid' should work, but experience
                          # seemed to indicate otherwise.  Single character
                          # TLDs are likely to remain invalid, so this seems to
                          # be the best choice. The trailing '.' prevents a
                          # related problem: The normal DNS resolver appends
                          # the domain names from the search path if there is
                          # no '.' the end and, and if one of those domains
                          # implements a '*' rule a result is returned.
                          # However, none of this will prevent the test from
                          # failing if the ISP hijacks all invalid domain
                          # requests.  The real solution would be to be able to
                          # parameterize the framework with a mock resolver.
                          mechanize.urlopen, "http://sadflkjsasf.i.nvali.d./")


if __name__ == "__main__":
    unittest.main()
