#!/usr/bin/env python

from unittest import TestCase

import mechanize

from test_browser import make_mock_handler


class UserAgentTests(TestCase):

    def _get_handler_from_ua(self, ua, name):
        handler = ua._ua_handlers.get(name)
        self.assertTrue(handler in ua.handlers)
        return handler

    def test_set_proxies(self):
        ua = mechanize.UserAgentBase()
        def proxy_bypass(hostname):
            return False
        proxies = {"http": "http://spam"}
        ua.set_proxies(proxies, proxy_bypass)
        proxy_handler = self._get_handler_from_ua(ua, "_proxy")
        self.assertTrue(proxy_handler._proxy_bypass is proxy_bypass)
        self.assertTrue(proxy_handler.proxies, proxies)

    def test_set_handled_schemes(self):
        class MockHandlerClass(make_mock_handler()):

            def __call__(self): return self
        class BlahHandlerClass(MockHandlerClass):
            pass
        class BlahProcessorClass(MockHandlerClass):
            pass
        BlahHandler = BlahHandlerClass([("blah_open", None)])
        BlahProcessor = BlahProcessorClass([("blah_request", None)])
        class TestUserAgent(mechanize.UserAgent):
            default_schemes = ["http"]
            default_others = []
            default_features = []
            handler_classes = mechanize.UserAgent.handler_classes.copy()
            handler_classes.update(
                {"blah": BlahHandler, "_blah": BlahProcessor})
        ua = TestUserAgent()

        self.assertEqual(list(h.__class__.__name__ for h in ua.handlers),
                         ["HTTPHandler"])
        ua.set_handled_schemes(["http", "file"])
        self.assertEqual(sorted(h.__class__.__name__ for h in ua.handlers),
                         ["FileHandler", "HTTPHandler"])
        self.assertRaises(ValueError,
                          ua.set_handled_schemes, ["blah", "non-existent"])
        self.assertRaises(ValueError,
                          ua.set_handled_schemes, ["blah", "_blah"])
        ua.set_handled_schemes(["blah"])

        req = mechanize.Request("blah://example.com/")
        r = ua.open(req)
        exp_calls = [("blah_open", (req,), {})]
        assert len(ua.calls) == len(exp_calls)
        for got, expect in zip(ua.calls, exp_calls):
            self.assertEqual(expect, got[1:])

        ua.calls = []
        req = mechanize.Request("blah://example.com/")
        ua._set_handler("_blah", True)
        r = ua.open(req)
        exp_calls = [
            ("blah_request", (req,), {}),
            ("blah_open", (req,), {})]
        assert len(ua.calls) == len(exp_calls)
        for got, expect in zip(ua.calls, exp_calls):
            self.assertEqual(expect, got[1:])
        ua._set_handler("_blah", True)


if __name__ == "__main__":
    import unittest
    unittest.main()
