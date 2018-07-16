import mechanize._clientcookie
import mechanize._testcase


def cookie_args(
    version=1, name="spam", value="eggs",
    port="80", port_specified=True,
    domain="example.com", domain_specified=False, domain_initial_dot=False,
    path="/", path_specified=False,
    secure=False,
    expires=0,
    discard=True,
    comment=None,
    comment_url=None,
    rest={},
    rfc2109=False,
):
    return locals()


def make_cookie(*args, **kwds):
    return mechanize._clientcookie.Cookie(**cookie_args(*args, **kwds))


class Test(mechanize._testcase.TestCase):

    def test_equality(self):
        # not using assertNotEqual here since operator used varies across
        # Python versions
        self.assertEqual(make_cookie(), make_cookie())
        self.assertFalse(make_cookie(name="ham") == make_cookie())

    def test_inequality(self):
        # not using assertNotEqual here since operator used varies across
        # Python versions
        self.assertTrue(make_cookie(name="ham") != make_cookie())
        self.assertFalse(make_cookie() != make_cookie())

    def test_all_state_included(self):
        def non_equal_value(value):
            if value is None:
                new_value = "80"
            elif isinstance(value, basestring):
                new_value = value + "1"
            elif isinstance(value, bool):
                new_value = not value
            elif isinstance(value, dict):
                new_value = dict(value)
                new_value["spam"] = "eggs"
            elif isinstance(value, int):
                new_value = value + 1
            else:
                assert False, value
            assert new_value != value, value
            return new_value
        cookie = make_cookie()
        for arg, default_value in cookie_args().iteritems():
            new_value = non_equal_value(default_value)
            self.assertNotEqual(make_cookie(**{arg: new_value}), cookie)
