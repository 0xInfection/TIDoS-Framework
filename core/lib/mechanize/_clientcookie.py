from __future__ import absolute_import

import re
import time
from .polyglot import (
    Cookie as _Cookie, CookieJar as CJ, MozillaCookieJar as MCJ, request_host
    as request_host_lc, DEFAULT_HTTP_PORT, CookiePolicy, DefaultCookiePolicy,
    FileCookieJar, LoadError, LWPCookieJar, _debug, domain_match,
    eff_request_host, escape_path, is_HDN, lwp_cookie_str, reach, request_path,
    request_port, user_domain_match, iteritems)

__all__ = [
    'DEFAULT_HTTP_PORT', 'CookiePolicy', 'DefaultCookiePolicy',
    'request_host_lc', 'MozillaCookieJar', 'escape_path', 'is_HDN',
    'request_port', 'LWPCookieJar', 'LoadError', 'reach', 'FileCookieJar',
    'lwp_cookie_str', 'domain_match', 'request_path', 'user_domain_match'
]


def effective_request_host(request):
    """Return the effective request-host, as defined by RFC 2965."""
    return eff_request_host(request)[1]


def request_is_unverifiable(request):
    try:
        return request.is_unverifiable()
    except AttributeError:
        if hasattr(request, "unverifiable"):
            return request.unverifiable
        else:
            raise


def cookies_equal(a, b):
    return all(getattr(a, x) == getattr(b, x) for x in Cookie._attrs)


class Cookie(_Cookie):
    _attrs = ("version", "name", "value", "port", "port_specified", "domain",
              "domain_specified", "domain_initial_dot", "path",
              "path_specified", "secure", "expires", "discard", "comment",
              "comment_url", "rfc2109", "_rest")

    def __eq__(self, other):
        return all(getattr(self, a) == getattr(other, a) for a in self._attrs)

    def __ne__(self, other):
        return not (self == other)


class CookieJar(CJ):

    def __getstate__(self):
        ans = self.__dict__.copy()
        del ans['_cookies_lock']
        return ans

    def __setstate__(self, val):
        for k, v in iteritems(val):
            setattr(self, k, v)

    def cookies_for_request(self, request):
        """Return a list of cookies to be returned to server.

        The returned list of cookie instances is sorted in the order they
        should appear in the Cookie: header for return to the server.

        See add_cookie_header.__doc__ for the interface required of the
        request argument.
        """
        with self._cookies_lock:
            self._policy._now = self._now = int(time.time())
            cookies = self._cookies_for_request(request)

            # add cookies in order of most specific (i.e. longest) path first
            def key(x):
                return len(x.path)

            cookies.sort(key=key, reverse=True)
            return cookies

    def get_policy(self):
        return self._policy

    def _normalized_cookie_tuples(self, attrs_set):
        """Return list of tuples containing normalised cookie information.

        attrs_set is the list of lists of key,value pairs extracted from
        the Set-Cookie or Set-Cookie2 headers.

        Tuples are name, value, standard, rest, where name and value are the
        cookie name and value, standard is a dictionary containing the standard
        cookie-attributes (discard, secure, version, expires or max-age,
        domain, path and port) and rest is a dictionary containing the rest of
        the cookie-attributes.

        """
        cookie_tuples = []

        boolean_attrs = "discard", "secure"
        value_attrs = ("version", "expires", "max-age", "domain", "path",
                       "port", "comment", "commenturl")

        for cookie_attrs in attrs_set:
            name, value = cookie_attrs[0]

            # Build dictionary of standard cookie-attributes (standard) and
            # dictionary of other cookie-attributes (rest).

            # Note: expiry time is normalised to seconds since epoch.  V0
            # cookies should have the Expires cookie-attribute, and V1 cookies
            # should have Max-Age, but since V1 includes RFC 2109 cookies (and
            # since V0 cookies may be a mish-mash of Netscape and RFC 2109), we
            # accept either (but prefer Max-Age).
            max_age_set = False

            bad_cookie = False

            standard = {}
            rest = {}
            for k, v in cookie_attrs[1:]:
                lc = k.lower()
                # don't lose case distinction for unknown fields
                if lc in value_attrs or lc in boolean_attrs:
                    k = lc
                if k in boolean_attrs and v is None:
                    # boolean cookie-attribute is present, but has no value
                    # (like "discard", rather than "port=80")
                    v = True
                if k in standard:
                    # only first value is significant
                    continue
                if k == "domain":
                    if v is None:
                        _debug("   missing value for domain attribute")
                        bad_cookie = True
                        break
                    # RFC 2965 section 3.3.3
                    v = v.lower()
                if k == "expires":
                    if max_age_set:
                        # Prefer max-age to expires (like Mozilla)
                        continue
                    if v is None:
                        _debug("   missing or invalid value for expires "
                               "attribute: treating as session cookie")
                        continue
                if k == "max-age":
                    max_age_set = True
                    try:
                        v = int(v)
                    except ValueError:
                        _debug("   missing or invalid (non-numeric) value for "
                               "max-age attribute")
                        bad_cookie = True
                        break
                    # convert RFC 2965 Max-Age to seconds since epoch
                    # XXX Strictly you're supposed to follow RFC 2616
                    #   age-calculation rules.  Remember that zero Max-Age
                    #   is a request to discard (old and new) cookie, though.
                    k = "expires"
                    v = self._now + v
                if not v and k == 'path':
                    # Added by Kovid, not in stdlib implementation
                    v = '/'
                if (k in value_attrs) or (k in boolean_attrs):
                    if (v is None and
                            k not in ("port", "comment", "commenturl")):
                        _debug("   missing value for %s attribute" % k)
                        bad_cookie = True
                        break
                    standard[k] = v
                else:
                    rest[k] = v

            if bad_cookie:
                continue

            cookie_tuples.append((name, value, standard, rest))

        return cookie_tuples

    def __getitem__(self, i):
        for q, ans in enumerate(self):
            if q == i:
                return ans
        raise IndexError()


class MozillaCookieJar(MCJ):

    def _really_load(self, f, filename, ignore_discard, ignore_expires):
        now = time.time()

        magic = f.readline()
        if not re.search(self.magic_re, magic):
            f.close()
            raise LoadError(
                "%r does not look like a Netscape format cookies file" %
                filename)

        try:
            while 1:
                line = f.readline()
                if line == "":
                    break

                # last field may be absent, so keep any trailing tab
                if line.endswith("\n"):
                    line = line[:-1]

                # skip comments and blank lines XXX what is $ for?
                if (line.strip().startswith(("#", "$")) or line.strip() == ""):
                    continue

                (domain, domain_specified, path, secure, expires, name,
                 value) = line.split("\t", 6)  # Changed by Kovid
                secure = (secure == "TRUE")
                domain_specified = (domain_specified == "TRUE")
                if name == "":
                    # cookies.txt regards 'Set-Cookie: foo' as a cookie
                    # with no name, whereas cookielib regards it as a
                    # cookie with no value.
                    name = value
                    value = None

                initial_dot = domain.startswith(".")
                if domain_specified != initial_dot:
                    raise ValueError()
                assert domain_specified == initial_dot

                discard = False
                if expires == "":
                    expires = None
                    discard = True

                # assume path_specified is false
                c = Cookie(0, name, value, None, False, domain,
                           domain_specified, initial_dot, path, False, secure,
                           expires, discard, None, None, {})
                if not ignore_discard and c.discard:
                    continue
                if not ignore_expires and c.is_expired(now):
                    continue
                self.set_cookie(c)

        except IOError:
            raise
        except Exception:
            raise LoadError("invalid Netscape format cookies file %r: %r" %
                            (filename, line))
