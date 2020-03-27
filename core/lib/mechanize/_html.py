from __future__ import absolute_import

import codecs
import copy
import re

from ._form import parse_forms
from ._headersutil import is_html as _is_html
from ._headersutil import split_header_words
from ._rfc3986 import clean_url, urljoin
from .polyglot import is_string

DEFAULT_ENCODING = "utf-8"
_encoding_pats = (
    # XML declaration
    r'<\?[^<>]+encoding\s*=\s*[\'"](.*?)[\'"][^<>]*>',
    # HTML 5 charset
    r'''<meta\s+charset=['"]([-_a-z0-9]+)['"][^<>]*>(?:\s*</meta>){0,1}''',
    # HTML 4 Pragma directive
    r'''<meta\s+?[^<>]*?content\s*=\s*['"][^'"]*?charset=([-_a-z0-9]+)[^'"]*?['"][^<>]*>(?:\s*</meta>){0,1}''',
)


def compile_pats(binary):
    for raw in _encoding_pats:
        if binary:
            raw = raw.encode('ascii')
        yield re.compile(raw, flags=re.IGNORECASE)


class LazyEncodingPats(object):

    def __call__(self, binary=False):
        attr = 'binary_pats' if binary else 'unicode_pats'
        pats = getattr(self, attr, None)
        if pats is None:
            pats = tuple(compile_pats(binary))
            setattr(self, attr, pats)
        for pat in pats:
            yield pat


lazy_encoding_pats = LazyEncodingPats()


def find_declared_encoding(raw, limit=50*1024):
    prefix = raw[:limit]
    is_binary = isinstance(raw, bytes)
    for pat in lazy_encoding_pats(is_binary):
        m = pat.search(prefix)
        if m is not None:
            ans = m.group(1)
            if is_binary:
                ans = ans.decode('ascii', 'replace')
                return ans


def elem_text(elem):
    if elem.text:
        yield elem.text
    for child in elem:
        for text in elem_text(child):
            yield text
        if child.tail:
            yield child.tail


def iterlinks(root, base_url):
    link_tags = {"a": "href", "area": "href", "iframe": "src"}
    for tag in root.iter('*'):
        if not is_string(tag.tag):
            continue
        q = tag.tag.lower()
        attr = link_tags.get(q)
        if attr is not None:
            val = tag.get(attr)
            if val:
                url = clean_url(val)
                yield Link(base_url, url,
                           compress_whitespace(u''.join(elem_text(tag))), q,
                           tag.items())
        elif q == 'base':
            href = tag.get('href')
            if href:
                base_url = href


def compress_whitespace(text):
    return re.sub(r'\s+', ' ', text or '').strip()


def get_encoding_from_response(response, verify=True):
    # HTTPEquivProcessor may be in use, so both HTTP and HTTP-EQUIV
    # headers may be in the response.  HTTP-EQUIV headers come last,
    # so try in order from first to last.
    if response:
        for ct in response.info().getheaders("content-type"):
            for k, v in split_header_words([ct])[0]:
                if k == "charset":
                    if not verify:
                        return v
                    try:
                        codecs.lookup(v)
                        return v
                    except LookupError:
                        continue


class EncodingFinder:
    def __init__(self, default_encoding):
        self._default_encoding = default_encoding

    def encoding(self, response):
        return get_encoding_from_response(response) or self._default_encoding


class ResponseTypeFinder:
    def __init__(self, allow_xhtml):
        self._allow_xhtml = allow_xhtml

    def is_html(self, response, encoding):
        ct_hdrs = response.info().getheaders("content-type")
        url = response.geturl()
        # XXX encoding
        return _is_html(ct_hdrs, url, self._allow_xhtml)


class Link:
    '''
    A link in a HTML document

    :ivar absolute_url: The absolutized link URL
    :ivar url: The link URL
    :ivar base_url: The base URL against which this link is resolved
    :ivar text: The link text
    :ivar tag: The link tag name
    :ivar attrs: The tag attributes

    '''
    def __init__(self, base_url, url, text, tag, attrs):
        assert None not in [url, tag, attrs]
        self.base_url = base_url
        self.absolute_url = urljoin(base_url, url)
        self.url, self.text, self.tag, self.attrs = url, text, tag, attrs
        self.text = self.text

    def __eq__(self, other):
        try:
            for name in "url", "text", "tag":
                if getattr(self, name) != getattr(other, name):
                    return False
            if dict(self.attrs) != dict(other.attrs):
                return False
        except AttributeError:
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Link(base_url=%r, url=%r, text=%r, tag=%r, attrs=%r)" % (
            self.base_url, self.url, self.text, self.tag, self.attrs)


def content_parser(data,
                   url=None,
                   response_info=None,
                   transport_encoding=None,
                   default_encoding=DEFAULT_ENCODING,
                   is_html=True):
    '''
    Parse data (a bytes object) into an etree representation such as
    :py:mod:`xml.etree.ElementTree` or `lxml.etree`

    :param bytes data: The data to parse
    :param url: The URL of the document being parsed or None
    :param response_info: Information about the document
        (contains all HTTP headers as :class:`HTTPMessage`)
    :param transport_encoding: The character encoding for the document being
        parsed as specified in the HTTP headers or None.
    :param default_encoding: The character encoding to use if no encoding
        could be detected and no transport_encoding is specified
    :param is_html: If the document is to be parsed as HTML.
    '''
    if not is_html:
        return
    try:
        from html5_parser import parse
    except Exception:
        from html5lib import parse
        kw = {'namespaceHTMLElements': False}
        if transport_encoding and isinstance(data, bytes):
            kw['transport_encoding'] = transport_encoding
        return parse(data, **kw)
    else:
        return parse(data, transport_encoding=transport_encoding)


def get_title(root):
    for title in root.iter('title'):
        text = compress_whitespace(title.text)
        if text:
            return text


lazy = object()


class Factory:
    """Factory for forms, links, etc.

    This interface may expand in future.

    Public methods:

    set_request_class(request_class)
    set_response(response)
    forms()
    links()

    Public attributes:

    Note that accessing these attributes may raise ParseError.

    encoding: string specifying the encoding of response if it contains a text
     document (this value is left unspecified for documents that do not have
     an encoding, e.g. an image file)
    is_html: true if response contains an HTML document (XHTML may be
     regarded as HTML too)
    title: page title, or None if no title or not HTML
    global_form: form object containing all controls that are not descendants
     of any FORM element, or None if the forms_factory does not support
     supplying a global form

    """

    def __init__(
            self,
            default_encoding=DEFAULT_ENCODING,
            allow_xhtml=False, ):
        """

        Pass keyword arguments only.

        """
        self._encoding_finder = EncodingFinder(default_encoding)
        self.form_encoding = default_encoding
        self._response_type_finder = ResponseTypeFinder(
            allow_xhtml=allow_xhtml)
        self._content_parser = content_parser
        self._current_forms = self._current_links = self._current_title = lazy
        self._current_global_form = self._root = lazy
        self._raw_data = b''
        self.is_html, self.encoding = False, DEFAULT_ENCODING

        self.set_response(None)

    def set_content_parser(self, val):
        self._content_parser = val

    def set_request_class(self, request_class):
        """Set request class (mechanize.Request by default).

        HTMLForm instances returned by .forms() will return instances of this
        class when .click()ed.

        """
        self._request_class = request_class

    def set_response(self, response):
        """Set response.

        The response must either be None or implement the same interface as
        objects returned by mechanize.urlopen().

        """
        self._response = copy.copy(response)
        self._current_forms = self._current_links = self._current_title = lazy
        self._current_global_form = self._root = lazy
        self.encoding = self._encoding_finder.encoding(self._response)
        self.is_html = self._response_type_finder.is_html(
            self._response, self.encoding) if self._response else False

    @property
    def root(self):
        if self._root is lazy:
            response = self._response
            raw = self._response.read() if self._response else b''
            default_encoding = self._encoding_finder._default_encoding
            transport_encoding = get_encoding_from_response(response, verify=False)
            declared_encoding = find_declared_encoding(raw)
            self.form_encoding = declared_encoding or transport_encoding or default_encoding
            self._root = self._content_parser(
                raw,
                url=response.geturl() if response else None,
                response_info=response.info() if response else None,
                default_encoding=default_encoding,
                is_html=self.is_html,
                transport_encoding=transport_encoding)
        return self._root

    @property
    def title(self):
        if self._current_title is lazy:
            self._current_title = get_title(
                self.root) if self.root is not None else None
        return self._current_title or u''

    @property
    def global_form(self):
        if self._current_global_form is lazy:
            self.forms()
        return self._current_global_form

    def forms(self):
        """ Return tuple of HTMLForm-like objects. """
        # this implementation sets .global_form as a side-effect
        if self._current_forms is lazy:
            self._current_forms, self._current_global_form = self._get_forms()
        return self._current_forms

    def links(self):
        """Return tuple of mechanize.Link-like objects.  """
        if self._current_links is lazy:
            self._current_links = self._get_links()
        return self._get_links()

    def _get_links(self):
        if self.root is None:
            return ()
        return tuple(iterlinks(self.root, self._response.geturl()))

    def _get_forms(self):
        if self.root is None:
            return (), None
        return parse_forms(self.root,
                           self._response.geturl(), self._request_class, encoding=self.form_encoding)
