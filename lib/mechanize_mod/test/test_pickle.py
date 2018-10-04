import cPickle
import pickle

import mechanize
import mechanize._response
import mechanize._testcase


def pickle_and_unpickle(obj, implementation):
    return implementation.loads(implementation.dumps(obj))


def test_pickling(obj, check=lambda unpickled: None):
    check(pickle_and_unpickle(obj, cPickle))
    check(pickle_and_unpickle(obj, pickle))


class PickleTest(mechanize._testcase.TestCase):

    def test_pickle_cookie(self):
        from mechanize._clientcookie import cookies_equal
        cookiejar = mechanize.CookieJar()
        url = "http://example.com/"
        request = mechanize.Request(url)
        response = mechanize._response.test_response(
            headers=[("Set-Cookie", "spam=eggs")], url=url)
        [cookie] = cookiejar.make_cookies(response, request)

        def check_equality(b):
            self.assertTrue(cookies_equal(cookie, b))

        test_pickling(cookie, check_equality)

    def test_pickle_cookiejar(self):
        test_pickling(mechanize.CookieJar())


if __name__ == "__main__":
    mechanize._testcase.main()
