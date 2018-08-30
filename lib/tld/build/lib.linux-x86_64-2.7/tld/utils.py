from __future__ import unicode_literals

import codecs

from six import PY3, text_type
from six.moves.urllib.parse import urlsplit
from six.moves.urllib.request import urlopen

from .conf import get_setting
from .exceptions import (
    TldBadUrl,
    TldDomainNotFound,
    TldImproperlyConfigured,
    TldIOError,
)
from .helpers import project_dir

__title__ = 'tld.utils'
__author__ = 'Artur Barseghyan'
__copyright__ = '2013-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'get_fld',
    'get_tld',
    'get_tld_names',
    'process_url',
    'Result',
    'update_tld_names',
    'parse_tld',
)

tld_names = None


class Result(object):
    """Container."""

    __slots__ = ('subdomain', 'domain', 'tld', '__fld', 'parsed_url')

    def __init__(self, tld, domain, subdomain, parsed_url):
        self.tld = tld
        self.domain = domain
        self.subdomain = subdomain
        self.parsed_url = parsed_url
        self.__fld = "{0}.{1}".format(self.domain, self.tld)

    @property
    def extension(self):
        """Alias of ``tld``.

        :return str:
        """
        return self.tld
    suffix = extension

    @property
    def fld(self):
        """First level domain.

        :return:
        :rtype: str
        """
        return self.__fld

    def __unicode__(self):
        if PY3:
            return self.tld
        else:
            try:
                return self.tld.encode('utf8')
            except UnicodeEncodeError:
                return self.tld
    __repr__ = __unicode__
    __str__ = __unicode__

    @property
    def __dict__(self):
        """Mimic __dict__ functionality.

        :return:
        :rtype: dict
        """
        return {
            'tld': self.tld,
            'domain': self.domain,
            'subdomain': self.subdomain,
            'fld': self.fld,
            'parsed_url': self.parsed_url,
        }


class TrieNode(object):
    """Class representing a single Trie node."""

    __slots__ = ('children', 'exception', 'leaf', 'private')

    def __init__(self):
        self.children = None
        self.exception = None
        self.leaf = False
        self.private = False


class Trie(object):
    """An adhoc Trie data structure to store tlds in reverse notation order."""

    def __init__(self):
        self.root = TrieNode()
        self.__nodes = 0

    def __len__(self):
        return self.__nodes

    def add(self, tld, private=False):
        node = self.root

        # Iterating over the tld parts in reverse order
        for part in reversed(tld.split('.')):

            if part.startswith('!'):
                node.exception = part[1:]
                break

            # To save up some RAM, we initialize the children dict only
            # when strictly necessary
            if node.children is None:
                node.children = {}

            child = node.children.get(part)

            if child is None:
                child = TrieNode()

            node.children[part] = child

            node = child

        node.leaf = True

        if private:
            node.private = True

        self.__nodes += 1


def update_tld_names(fail_silently=False):
    """Update the local copy of TLDs file.

    :param fail_silently: If set to True, no exceptions is raised on
        failure but boolean False returned.
    :type fail_silently: bool
    :return: True on success, False on failure.
    :rtype: bool
    """
    tld_names_source_url = get_setting('NAMES_SOURCE_URL')
    tld_names_local_path = get_setting('NAMES_LOCAL_PATH')
    try:
        remote_file = urlopen(tld_names_source_url)
        local_file = codecs.open(
            project_dir(tld_names_local_path),
            'wb',
            encoding='utf8'
        )
        local_file.write(remote_file.read().decode('utf8'))
        local_file.close()
        remote_file.close()
    except Exception as err:
        if fail_silently:
            return False
        raise TldIOError(err)

    return True


def get_tld_names(fail_silently=False, retry_count=0):
    """Build the ``tlds`` list if empty. Recursive.

    :param fail_silently: If set to True, no exceptions are raised and None
        is returned on failure.
    :param retry_count: If greater than 1, we raise an exception in order
        to avoid infinite loops.
    :type fail_silently: bool
    :type retry_count: int
    :return: List of TLD names
    :type: iterable
    """
    tld_names_local_path = get_setting('NAMES_LOCAL_PATH')

    if retry_count > 1:
        if fail_silently:
            return None
        else:
            raise TldIOError

    global tld_names

    # If already loaded, return
    if tld_names is not None:
        return tld_names

    local_file = None
    try:
        # Load the TLD names file
        local_file = codecs.open(project_dir(tld_names_local_path),
                                 'r',
                                 encoding='utf8')
        tld_names = Trie()
        # Make a list of it all, strip all garbage
        private_section = False

        for line in local_file:
            if '===BEGIN PRIVATE DOMAINS===' in line:
                private_section = True

            # Puny code tlds
            if '// xn--' in line:
                line = line.split(' (', 1)[0][3:]

            if line[0] == '/' or line[0] == '\n':
                continue

            tld_names.add(u'{0}'.format(line.strip()), private=private_section)

        local_file.close()
    except IOError as err:
        update_tld_names()  # Grab the file
        # Increment ``retry_count`` in order to avoid infinite loops
        retry_count += 1
        return get_tld_names(fail_silently, retry_count)  # Run again
    except Exception as err:
        try:
            local_file.close()
        except Exception:
            pass

        if fail_silently:
            return None
        else:
            raise err

    return tld_names


def process_url(url,
                fail_silently=False,
                fix_protocol=False,
                search_public=True,
                search_private=True):
    """Process URL.

    :param url:
    :param fail_silently:
    :param fix_protocol:
    :param search_public:
    :param search_private:
    :return:
    """
    if not (search_public or search_private):
        raise TldImproperlyConfigured(
            "Either `search_public` or `search_private` (or both) shall be "
            "set to True."
        )

    url = url.lower()

    if fix_protocol:
        if (
            not url.startswith('//')
            and not (url.startswith('http://') or url.startswith('https://'))
        ):
            url = 'https://{}'.format(url)

    tld_names = get_tld_names(fail_silently=fail_silently)  # Init

    # Get parsed URL as we might need it later
    parsed_url = urlsplit(url)
    # Get (sub) domain name
    domain_name = parsed_url.netloc

    # Handling auth
    if '@' in domain_name:
        domain_name = domain_name.split('@', 1)[-1]

    # Handling port
    domain_name = domain_name.split(':', 1)[0]

    if not domain_name:
        if fail_silently:
            return None, None, parsed_url
        else:
            raise TldBadUrl(url=url)

    domain_parts = domain_name.split('.')

    # Now we query our Trie iterating on the domain parts in reverse order
    node = tld_names.root
    tld_length = 0
    for i in reversed(range(len(domain_parts))):
        part = domain_parts[i]

        # Cannot go deeper
        if node.children is None:
            break

        # Exception
        if part == node.exception:
            break

        child = node.children.get(part)

        # Wildcards
        if child is None:
            child = node.children.get('*')

        # If the current part is not in current node's children, we can stop
        if child is None:
            break

        # Else we move deeper and increment our tld offset
        tld_length += 1
        node = child

    # Checking the node we finished on is a leaf and is one we allow
    if (
        (not node.leaf) or
        (not search_public and not node.private) or
        (not search_private and node.private)
    ):
        if fail_silently:
            return None, None, parsed_url
        else:
            raise TldDomainNotFound(domain_name=domain_name)

    non_zero_i = max(1, len(domain_parts) - tld_length)

    return domain_parts, non_zero_i, parsed_url


def get_fld(url,
            fail_silently=False,
            fix_protocol=False,
            search_public=True,
            search_private=True,
            **kwargs):
    """Extract the first level domain.

    Extract the top level domain based on the mozilla's effective TLD names
    dat file. Returns a string. May throw ``TldBadUrl`` or
    ``TldDomainNotFound`` exceptions if there's bad URL provided or no TLD
    match found respectively.

    :param url: URL to get top level domain from.
    :param fail_silently: If set to True, no exceptions are raised and None
        is returned on failure.
    :param fix_protocol: If set to True, missing or wrong protocol is
        ignored (https is appended instead).
    :param search_public: If set to True, search in public domains.
    :param search_private: If set to True, search in private domains.
    :type url: str
    :type fail_silently: bool
    :type fix_protocol: bool
    :type search_public: bool
    :type search_private: bool
    :return: String with top level domain (if ``as_object`` argument
        is set to False) or a ``tld.utils.Result`` object (if ``as_object``
        argument is set to True); returns None on failure.
    :rtype: str
    """
    if 'as_object' in kwargs:
        raise TldImproperlyConfigured(
            "`as_object` argument is deprecated for `get_fld`. Use `get_tld` "
            "instead."
        )

    domain_parts, non_zero_i, parsed_url = process_url(
        url=url,
        fail_silently=fail_silently,
        fix_protocol=fix_protocol,
        search_public=search_public,
        search_private=search_private
    )

    if domain_parts is None:
        return None

    return text_type(".").join(domain_parts[non_zero_i-1:])


def get_tld(url,
            fail_silently=False,
            as_object=False,
            fix_protocol=False,
            search_public=True,
            search_private=True):
    """Extract the top level domain.

    Extract the top level domain based on the mozilla's effective TLD names
    dat file. Returns a string. May throw ``TldBadUrl`` or
    ``TldDomainNotFound`` exceptions if there's bad URL provided or no TLD
    match found respectively.

    :param url: URL to get top level domain from.
    :param fail_silently: If set to True, no exceptions are raised and None
        is returned on failure.
    :param as_object: If set to True, ``tld.utils.Result`` object is returned,
        ``domain``, ``suffix`` and ``tld`` properties.
    :param fix_protocol: If set to True, missing or wrong protocol is
        ignored (https is appended instead).
    :param search_public: If set to True, search in public domains.
    :param search_private: If set to True, search in private domains.
    :type url: str
    :type fail_silently: bool
    :type as_object: bool
    :type fix_protocol: bool
    :type search_public: bool
    :type search_private: bool
    :return: String with top level domain (if ``as_object`` argument
        is set to False) or a ``tld.utils.Result`` object (if ``as_object``
        argument is set to True); returns None on failure.
    :rtype: str
    """
    domain_parts, non_zero_i, parsed_url = process_url(
        url=url,
        fail_silently=fail_silently,
        fix_protocol=fix_protocol,
        search_public=search_public,
        search_private=search_private
    )

    if domain_parts is None:
        return None

    if not as_object:
        return text_type(".").join(domain_parts[non_zero_i:])

    subdomain = text_type(".").join(domain_parts[:non_zero_i-1])
    domain = text_type(".").join(
        domain_parts[non_zero_i-1:non_zero_i]
    )
    _tld = text_type(".").join(domain_parts[non_zero_i:])

    return Result(
        subdomain=subdomain,
        domain=domain,
        tld=_tld,
        parsed_url=parsed_url
    )


def parse_tld(url,
              fail_silently=False,
              fix_protocol=False,
              search_public=True,
              search_private=True):
    """Parse TLD into parts.

    :param url:
    :param fail_silently:
    :param fix_protocol:
    :param search_public:
    :param search_private:
    :return:
    :rtype: tuple
    """
    try:
        obj = get_tld(
            url,
            fail_silently=fail_silently,
            as_object=True,
            fix_protocol=fix_protocol,
            search_public=search_public,
            search_private=search_private
        )
        _tld = obj.tld
        domain = obj.domain
        subdomain = obj.subdomain

    except (
        TldBadUrl,
        TldDomainNotFound,
        TldImproperlyConfigured,
        TldIOError
    ):
        _tld = None
        domain = None
        subdomain = None

    return _tld, domain, subdomain
