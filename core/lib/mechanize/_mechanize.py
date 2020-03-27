"""Stateful programmatic WWW navigation, after Perl's WWW::Mechanize.

Copyright 2003-2006 John J. Lee <jjl@pobox.com>
Copyright 2003 Andy Lester (original Perl code)

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD or ZPL 2.1 licenses (see the file LICENSE
included with the distribution).

"""
from __future__ import absolute_import

import copy
import os
import re

from . import _request, _response, _rfc3986, _sockettimeout, _urllib2_fork
from ._clientcookie import Cookie
from ._headersutil import normalize_header_name
from ._html import Factory
from ._useragent import UserAgentBase
from .polyglot import pathname2url, HTTPError, is_string, iteritems


class BrowserStateError(Exception):
    pass


class LinkNotFoundError(Exception):
    pass


class FormNotFoundError(Exception):
    pass


def sanepathname2url(path):
    urlpath = pathname2url(path)
    if os.name == "nt" and urlpath.startswith("///"):
        urlpath = urlpath[2:]
    # XXX don't ask me about the mac...
    return urlpath


class History:
    """

    Though this will become public, the implied interface is not yet stable.

    """

    def __init__(self):
        self._history = []  # LIFO

    def add(self, request, response):
        self._history.append((request, response))

    def back(self, n, _response):
        response = _response  # XXX move Browser._response into this class?
        while n > 0 or response is None:
            try:
                request, response = self._history.pop()
            except IndexError:
                raise BrowserStateError("already at start of history")
            n -= 1
        return request, response

    def clear(self):
        del self._history[:]

    def close(self):
        for request, response in self._history:
            if response is not None:
                response.close()
        del self._history[:]

    def __copy__(self):
        ans = self.__class__()
        ans._history = self._history[:]
        return ans


class HTTPRefererProcessor(_urllib2_fork.BaseHandler):
    def http_request(self, request):
        # See RFC 2616 14.36.  The only times we know the source of the
        # request URI has a URI associated with it are redirect, and
        # Browser.click() / Browser.submit() / Browser.follow_link().
        # Otherwise, it's the user's job to add any Referer header before
        # .open()ing.
        if hasattr(request, "redirect_dict"):
            request = self.parent._add_referer_header(
                request, origin_request=False)
        return request

    https_request = http_request


class Browser(UserAgentBase):
    """Browser-like class with support for history, forms and links.

    :class:`BrowserStateError` is raised whenever the browser is in the wrong
    state to complete the requested operation - e.g., when :meth:`back()` is
    called when the browser history is empty, or when :meth:`follow_link()` is
    called when the current response does not contain HTML data.

    Public attributes:

    request: current request (:class:`mechanize.Request`)

    form: currently selected form (see :meth:`select_form()`)

    :param history: object implementing the :class:`mechanize.History`
                    interface.  Note this interface is still experimental
                    and may change in future. This object is owned
                    by the browser instance and must not be shared
                    among browsers.
    :param request_class: Request class to use. Defaults to
                            :class:`mechanize.Request`
    :param content_parser: A function that is responsible for parsing
        received html/xhtml content. See the builtin
        :func:`mechanize._html.content_parser()` function for details
        on the interface this function must support.

    """

    handler_classes = copy.copy(UserAgentBase.handler_classes)
    handler_classes["_referer"] = HTTPRefererProcessor
    default_features = copy.copy(UserAgentBase.default_features)
    default_features.append("_referer")

    def __init__(
            self,
            history=None,
            request_class=None,
            content_parser=None,
            allow_xhtml=False, ):
        """
        Only named arguments should be passed to this constructor.

        """
        self._handle_referer = True

        if history is None:
            history = History()
        self._history = history

        if request_class is None:
            request_class = _request.Request

        factory = Factory(allow_xhtml=allow_xhtml)
        factory.set_request_class(request_class)
        if content_parser is not None:
            factory.set_content_parser(content_parser)
        self._factory = factory
        self.request_class = request_class

        self.request = None
        self._set_response(None, False)

        # do this last to avoid __getattr__ problems
        UserAgentBase.__init__(self)

    def __copy__(self):
        '''
        Clone this browser instance. The clone will share the same, thread-safe
        cookie jar, and have all the same handlers/settings, but will not share
        any other state, making it safe to use in another thread.
        '''
        ans = self.__class__()
        self._copy_state(ans)
        ans._handle_referer = self._handle_referer
        for attr in ('_response_type_finder', '_encoding_finder',
                     '_content_parser'):
            setattr(ans._factory, attr, getattr(self._factory, attr))
        ans.request_class = self.request_class
        ans._history = copy.copy(self._history)
        return ans

    def close(self):
        UserAgentBase.close(self)
        if self._response is not None:
            self._response.close()
        if self._history is not None:
            self._history.close()
            self._history = None

        # make use after .close easy to spot
        self.form = None
        self.request = self._response = None
        self.request = self.response = self.set_response = None
        self.geturl = self.reload = self.back = None
        self.clear_history = self.set_cookie = self.links = self.forms = None
        self.viewing_html = self.encoding = self.title = None
        self.select_form = self.click = self.submit = self.click_link = None
        self.follow_link = self.find_link = None

    def set_handle_referer(self, handle):
        """Set whether to add Referer header to each request."""
        self._set_handler("_referer", handle)
        self._handle_referer = bool(handle)

    def _add_referer_header(self, request, origin_request=True):
        if self.request is None:
            return request
        scheme = request.get_type()
        original_scheme = self.request.get_type()
        if scheme not in ["http", "https"]:
            return request
        if not origin_request and not self.request.has_header("Referer"):
            return request

        if (self._handle_referer and original_scheme in ["http", "https"] and
                not (original_scheme == "https" and scheme != "https")):
            # strip URL fragment (RFC 2616 14.36)
            parts = _rfc3986.urlsplit(self.request.get_full_url())
            parts = parts[:-1] + (None, )
            referer = _rfc3986.urlunsplit(parts)
            request.add_unredirected_header("Referer", referer)
        return request

    def open_novisit(self,
                     url_or_request,
                     data=None,
                     timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        """Open a URL without visiting it.

        Browser state (including request, response, history, forms and links)
        is left unchanged by calling this function.

        The interface is the same as for :meth:`open()`.

        This is useful for things like fetching images.

        See also :meth:`retrieve()`

        """
        return self._mech_open(
            url_or_request, data, visit=False, timeout=timeout)

    def open(self,
             url_or_request,
             data=None,
             timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        '''
        Open a URL. Loads the page so that you can subsequently use
        :meth:`forms()`, :meth:`links()`, etc. on it.

        :param url_or_request: Either a URL or a :class:`mechanize.Request`
        :param dict data: data to send with a POST request
        :param timeout: Timeout in seconds
        :return: A :class:`mechanize.Response` object
        '''
        return self._mech_open(url_or_request, data, timeout=timeout)

    def _mech_open(self,
                   url,
                   data=None,
                   update_history=True,
                   visit=None,
                   timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        try:
            url.get_full_url
        except AttributeError:
            # string URL -- convert to absolute URL if required
            scheme, authority = _rfc3986.urlsplit(url)[:2]
            if scheme is None:
                # relative URL
                if self._response is None:
                    raise BrowserStateError("can't fetch relative reference: "
                                            "not viewing any document")
                url = _rfc3986.urljoin(self._response.geturl(), url)

        request = self._request(url, data, visit, timeout)
        visit = request.visit
        if visit is None:
            visit = True

        if visit:
            self._visit_request(request, update_history)

        success = True
        try:
            response = UserAgentBase.open(self, request, data)
        except HTTPError as error:
            success = False
            if error.fp is None:  # not a response
                raise
            response = error

#         except (IOError, socket.error, OSError) as error:
#             Yes, urllib2 really does raise all these :-((
#             See test_urllib2.py for examples of socket.gaierror and OSError,
#             plus note that FTPHandler raises IOError.
#             XXX I don't seem to have an example of exactly socket.error being
#              raised, only socket.gaierror...
#             I don't want to start fixing these here, though, since this is a
#             subclass of OpenerDirector, and it would break old code.  Even in
#             Python core, a fix would need some backwards-compat. hack to be
#             acceptable.
#             raise

        if visit:
            self._set_response(response, False)
            response = copy.copy(self._response)
        elif response is not None:
            response = _response.upgrade_response(response)

        if not success:
            raise response
        return response

    def __str__(self):
        text = []
        text.append("<%s " % self.__class__.__name__)
        if self._response:
            text.append("visiting %s" % self._response.geturl())
        else:
            text.append("(not visiting a URL)")
        if self.form:
            text.append("\n selected form:\n %s\n" % str(self.form))
        text.append(">")
        return "".join(text)

    def response(self):
        """Return a copy of the current response.

        The returned object has the same interface as the object returned by
        :meth:`.open()`

        """
        return copy.copy(self._response)

    def open_local_file(self, filename):
        path = sanepathname2url(os.path.abspath(filename))
        url = 'file://' + path
        return self.open(url)

    def set_response(self, response):
        """Replace current response with (a copy of) response.

        response may be None.

        This is intended mostly for HTML-preprocessing.
        """
        self._set_response(response, True)

    def _set_response(self, response, close_current):
        # sanity check, necessary but far from sufficient
        if not (response is None or
                (hasattr(response, "info") and hasattr(response, "geturl") and
                 hasattr(response, "read"))):
            raise ValueError("not a response object")

        self.form = None
        if response is not None:
            response = _response.upgrade_response(response)
        if close_current and self._response is not None:
            self._response.close()
        self._response = response
        self._factory.set_response(response)

    def visit_response(self, response, request=None):
        """Visit the response, as if it had been :meth:`open()` ed.

        Unlike :meth:`set_response()`, this updates history rather than
        replacing the current response.
        """
        if request is None:
            request = _request.Request(response.geturl())
        self._visit_request(request, True)
        self._set_response(response, False)

    def _visit_request(self, request, update_history):
        if self._response is not None:
            self._response.close()
        if self.request is not None and update_history:
            self._history.add(self.request, self._response)
        self._response = None
        # we want self.request to be assigned even if UserAgentBase.open
        # fails
        self.request = request

    def geturl(self):
        """Get URL of current document."""
        if self._response is None:
            raise BrowserStateError("not viewing any document")
        return self._response.geturl()

    def reload(self):
        """Reload current document, and return response object."""
        if self.request is None:
            raise BrowserStateError("no URL has yet been .open()ed")
        if self._response is not None:
            self._response.close()
        return self._mech_open(self.request, update_history=False)

    def back(self, n=1):
        """Go back n steps in history, and return response object.

        n: go back this number of steps (default 1 step)

        """
        if self._response is not None:
            self._response.close()
        self.request, response = self._history.back(n, self._response)
        self.set_response(response)
        if not response.read_complete:
            return self.reload()
        return copy.copy(response)

    def clear_history(self):
        self._history.clear()

    def set_cookie(self, cookie_string):
        """Set a cookie.

        Note that it is NOT necessary to call this method under ordinary
        circumstances: cookie handling is normally entirely automatic.  The
        intended use case is rather to simulate the setting of a cookie by
        client script in a web page (e.g. JavaScript).  In that case, use of
        this method is necessary because mechanize currently does not support
        JavaScript, VBScript, etc.

        The cookie is added in the same way as if it had arrived with the
        current response, as a result of the current request.  This means that,
        for example, if it is not appropriate to set the cookie based on the
        current request, no cookie will be set.

        The cookie will be returned automatically with subsequent responses
        made by the Browser instance whenever that's appropriate.

        cookie_string should be a valid value of the Set-Cookie header.

        For example:

        .. code-block:: python

            browser.set_cookie(
                "sid=abcdef; expires=Wednesday, 09-Nov-06 23:12:40 GMT")

        Currently, this method does not allow for adding RFC 2986 cookies.
        This limitation will be lifted if anybody requests it.

        See also :meth:`set_simple_cookie()` for an easier way to set cookies
        without needing to create a Set-Cookie header string.
        """
        if self._response is None:
            raise BrowserStateError("not viewing any document")
        if self.request.get_type() not in ["http", "https"]:
            raise BrowserStateError("can't set cookie for non-HTTP/HTTPS "
                                    "transactions")
        cookiejar = self._ua_handlers["_cookies"].cookiejar
        response = self.response()  # copy
        headers = response.info()
        headers["Set-cookie"] = cookie_string
        cookiejar.extract_cookies(response, self.request)

    def set_simple_cookie(self, name, value, domain, path='/'):
        '''
        Similar to :meth:`set_cookie()` except that instead of using a
        cookie string, you simply specify the `name`, `value`, `domain`
        and optionally the `path`.
        The created cookie will never expire. For example:

        .. code-block:: python

            browser.set_simple_cookie('some_key', 'some_value', '.example.com',
                                      path='/some-page')
        '''
        self.cookiejar.set_cookie(
            Cookie(0, name, value, None, False, domain, True, False, path,
                   True, False, None, False, None, None, None))

    @property
    def cookiejar(self):
        ' Return the current cookiejar (:class:`mechanize.CookieJar`) or None '
        try:
            return self._ua_handlers["_cookies"].cookiejar
        except Exception:
            pass

    def set_header(self, header, value=None):
        '''
        Convenience method to set a header value in `self.addheaders`
        so that the header is sent out with all requests automatically.

        :param header: The header name, e.g. User-Agent
        :param value: The header value. If set to None the header is removed.
        '''
        found = False
        header = normalize_header_name(header)
        q = header.lower()
        remove = []
        for i, (k, v) in enumerate(tuple(self.addheaders)):
            if k.lower() == q:
                if value:
                    self.addheaders[i] = (header, value)
                    found = True
                else:
                    remove.append(i)
        if not found:
            self.addheaders.append((header, value))
        if remove:
            for i in reversed(remove):
                del self.addheaders[i]

    def links(self, **kwds):
        """Return iterable over links (:class:`mechanize.Link` objects)."""
        if not self.viewing_html():
            raise BrowserStateError("not viewing HTML")
        links = self._factory.links()
        if kwds:
            return self._filter_links(links, **kwds)
        else:
            return links

    def forms(self):
        """Return iterable over forms.

        The returned form objects implement the :class:`mechanize.HTMLForm`
        interface.

        """
        if not self.viewing_html():
            raise BrowserStateError("not viewing HTML")
        return self._factory.forms()

    def global_form(self):
        """Return the global form object, or None if the factory implementation
        did not supply one.

        The "global" form object contains all controls that are not descendants
        of any FORM element.

        The returned form object implements the :class:`mechanize.HTMLForm`
        interface.

        This is a separate method since the global form is not regarded as part
        of the sequence of forms in the document -- mostly for
        backwards-compatibility.

        """
        if not self.viewing_html():
            raise BrowserStateError("not viewing HTML")
        return self._factory.global_form

    def viewing_html(self):
        """Return whether the current response contains HTML data."""
        if self._response is None:
            raise BrowserStateError("not viewing any document")
        return self._factory.is_html

    def encoding(self):
        if self._response is None:
            raise BrowserStateError("not viewing any document")
        return self._factory.encoding

    def title(self):
        ' Return title, or None if there is no title element in the document. '
        if not self.viewing_html():
            raise BrowserStateError("not viewing HTML")
        return self._factory.title

    def select_form(self, name=None, predicate=None, nr=None, **attrs):
        """Select an HTML form for input.

        This is a bit like giving a form the "input focus" in a browser.

        If a form is selected, the Browser object supports the HTMLForm
        interface, so you can call methods like :meth:`set_value()`,
        :meth:`set()`, and :meth:`click()`.

        Another way to select a form is to assign to the .form attribute.  The
        form assigned should be one of the objects returned by the
        :meth:`forms()` method.

        If no matching form is found,
        :class:`mechanize.FormNotFoundError` is raised.

        If `name` is specified, then the form must have the indicated name.

        If `predicate` is specified, then the form must match that function.
        The predicate function is passed the :class:`mechanize.HTMLForm` as its
        single argument, and should return a boolean value indicating whether
        the form matched.

        `nr`, if supplied, is the sequence number of the form (where 0 is the
        first).  Note that control 0 is the first form matching all the other
        arguments (if supplied); it is not necessarily the first control in the
        form.  The "global form" (consisting of all form controls not contained
        in any FORM element) is considered not to be part of this sequence and
        to have no name, so will not be matched unless both name and nr are
        None.

        You can also match on any HTML attribute of the `<form>` tag by passing
        in the attribute name and value as keyword arguments. To convert HTML
        attributes into syntactically valid python keyword arguments, the
        following simple rule is used. The python keyword argument name is
        converted to an HTML attribute name by: Replacing all underscores with
        hyphens and removing any trailing underscores. You can pass in strings,
        functions or regular expression objects as the values to match. For
        example:

        .. code-block:: python

            # Match form with the exact action specified
            br.select_form(action='http://foo.com/submit.php')
            # Match form with a class attribute that contains 'login'
            br.select_form(class_=lambda x: 'login' in x)
            # Match form with a data-form-type attribute that matches a regex
            br.select_form(data_form_type=re.compile(r'a|b'))

        """
        if not self.viewing_html():
            raise BrowserStateError("not viewing HTML")
        if name is None and predicate is None and nr is None and not attrs:
            raise ValueError(
                "at least one argument must be supplied to specify form")

        global_form = self._factory.global_form
        if nr is None and name is None and predicate is not None and predicate(
                global_form):
            self.form = global_form
            return

        def attr_selector(q):
            if is_string(q):
                return lambda x: x == q
            if callable(q):
                return q
            return lambda x: q.match(x) is not None
        attrsq = {aname.rstrip('_').replace('_', '-'): attr_selector(v)
                  for aname, v in iteritems(attrs)}

        def form_attrs_match(form_attrs):
            for aname, q in iteritems(attrsq):
                val = form_attrs.get(aname)
                if val is None or not q(val):
                    return False
            return True

        orig_nr = nr
        for form in self.forms():
            if name is not None and name != form.name:
                continue
            if predicate is not None and not predicate(form):
                continue
            if nr:
                nr -= 1
                continue
            if attrs and not form_attrs_match(form.attrs):
                continue
            self.form = form
            break  # success
        else:
            # failure
            description = []
            if name is not None:
                description.append("name '%s'" % name)
            if predicate is not None:
                description.append("predicate %s" % predicate)
            if orig_nr is not None:
                description.append("nr %d" % orig_nr)
            if attrs:
                for k, v in iteritems(attrs):
                    description.append('%s = %r' % (k, v))
            description = ", ".join(description)
            raise FormNotFoundError("no form matching " + description)

    def click(self, *args, **kwds):
        """See :meth:`mechanize.HTMLForm.click()` for documentation."""
        if not self.viewing_html():
            raise BrowserStateError("not viewing HTML")
        request = self.form.click(*args, **kwds)
        return self._add_referer_header(request)

    def submit(self, *args, **kwds):
        """Submit current form.

        Arguments are as for :meth:`mechanize.HTMLForm.click()`.

        Return value is same as for :meth:`open()`.
        """
        return self.open(self.click(*args, **kwds))

    def click_link(self, link=None, **kwds):
        """Find a link and return a Request object for it.

        Arguments are as for :meth:`find_link()`, except that a link may be
        supplied as the first argument.

        """
        if not self.viewing_html():
            raise BrowserStateError("not viewing HTML")
        if not link:
            link = self.find_link(**kwds)
        else:
            if kwds:
                raise ValueError(
                    "either pass a Link, or keyword arguments, not both")
        request = self.request_class(link.absolute_url)
        return self._add_referer_header(request)

    def follow_link(self, link=None, **kwds):
        """Find a link and :meth:`open()` it.

        Arguments are as for :meth:`click_link()`.

        Return value is same as for :meth:`open()`.

        """
        return self.open(self.click_link(link, **kwds))

    def find_link(self,
                  text=None,
                  text_regex=None,
                  name=None,
                  name_regex=None,
                  url=None,
                  url_regex=None,
                  tag=None,
                  predicate=None,
                  nr=0):
        """Find a link in current page.

        Links are returned as :class:`mechanize.Link` objects. Examples:

        .. code-block:: python

            # Return third link that .search()-matches the regexp "python" (by
            # ".search()-matches", I mean that the regular expression method
            # .search() is used, rather than .match()).
            find_link(text_regex=re.compile("python"), nr=2)

            # Return first http link in the current page that points to
            # somewhere on python.org whose link text (after tags have been
            # removed) is exactly "monty python".
            find_link(text="monty python",
                    url_regex=re.compile("http.*python.org"))

            # Return first link with exactly three HTML attributes.
            find_link(predicate=lambda link: len(link.attrs) == 3)

        Links include anchors `<a>`, image maps `<area>`, and frames
        `<iframe>`.

        All arguments must be passed by keyword, not position.  Zero or more
        arguments may be supplied.  In order to find a link, all arguments
        supplied must match.

        If a matching link is not found, :class:`mechanize.LinkNotFoundError`
        is raised.

        :param text: link text between link tags: e.g. <a href="blah">this
            bit</a> with whitespace compressed.
        :param text_regex: link text between tag (as defined above) must match
            the regular expression object or regular expression string passed
            as this argument, if supplied
        :param name: as for text and text_regex, but matched
            against the name HTML attribute of the link tag
        :param url: as for text and text_regex, but matched against the
            URL of the link tag (note this matches against Link.url, which is a
            relative or absolute URL according to how it was written in the
            HTML)
        :param tag: element name of opening tag, e.g. "a"
        :param predicate: a function taking a Link object as its single
            argument, returning a boolean result, indicating whether the links
        :param nr: matches the nth link that matches all other
            criteria (default 0)

        """
        try:
            return next(self._filter_links(
                self._factory.links(), text, text_regex, name, name_regex, url,
                url_regex, tag, predicate, nr))
        except StopIteration:
            raise LinkNotFoundError()

    def __getattr__(self, name):
        # pass through _form.HTMLForm methods and attributes
        form = self.__dict__.get("form")
        if form is None:
            raise AttributeError(
                "%s instance has no attribute %s (perhaps you forgot to "
                ".select_form()?)" % (self.__class__, name))
        return getattr(form, name)

    def __getitem__(self, name):
        if self.form is None:
            raise BrowserStateError('No form selected')
        return self.form[name]

    def __setitem__(self, name, val):
        if self.form is None:
            raise BrowserStateError('No form selected')
        self.form[name] = val

    def _filter_links(self,
                      links,
                      text=None,
                      text_regex=None,
                      name=None,
                      name_regex=None,
                      url=None,
                      url_regex=None,
                      tag=None,
                      predicate=None,
                      nr=0):
        if not self.viewing_html():
            raise BrowserStateError("not viewing HTML")

        orig_nr = nr

        for link in links:
            if url is not None and url != link.url:
                continue
            if url_regex is not None and not re.search(url_regex, link.url):
                continue
            if (text is not None and (link.text is None or text != link.text)):
                continue
            if (
                    text_regex is not None and (
                        link.text is None or not re.search(
                            text_regex, link.text))):
                continue
            if name is not None and name != dict(link.attrs).get("name"):
                continue
            if name_regex is not None:
                link_name = dict(link.attrs).get("name")
                if link_name is None or not re.search(name_regex, link_name):
                    continue
            if tag is not None and tag != link.tag:
                continue
            if predicate is not None and not predicate(link):
                continue
            if nr:
                nr -= 1
                continue
            yield link
            nr = orig_nr
