#!/usr/bin/env python

# Python bindings to the Google search engine
# Copyright (c) 2009-2016, Mario Vilas
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice,this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

__all__ = [

    # Main search function.
    'search',

    # Specialized search functions.
    'search_images', 'search_news',
    'search_videos', 'search_shop',
    'search_books', 'search_apps',

    # Shortcut for "get lucky" search.
    'lucky',

    # Computations based on the number of Google hits.
    'hits', 'ngd',

    # Miscellaneous utility functions.
    'get_random_user_agent',
]

import os
import random
import sys
import time
import math

if sys.version_info[0] > 2:
    from http.cookiejar import LWPCookieJar
    from urllib.request import Request, urlopen
    from urllib.parse import quote_plus, urlparse, parse_qs
else:
    from cookielib import LWPCookieJar
    from urllib import quote_plus
    from urllib2 import Request, urlopen
    from urlparse import urlparse, parse_qs

try:
    from bs4 import BeautifulSoup
    is_bs4 = True
except ImportError:
    from BeautifulSoup import BeautifulSoup
    is_bs4 = False

# URL templates to make Google searches.
url_home = "https://www.google.%(tld)s/"
url_search = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&" \
             "btnG=Google+Search&tbs=%(tbs)s&safe=%(safe)s&tbm=%(tpe)s"
url_next_page = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&" \
                "start=%(start)d&tbs=%(tbs)s&safe=%(safe)s&tbm=%(tpe)s"
url_search_num = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&" \
                 "num=%(num)d&btnG=Google+Search&tbs=%(tbs)s&safe=%(safe)s&" \
                 "tbm=%(tpe)s"
url_next_page_num = "https://www.google.%(tld)s/search?hl=%(lang)s&" \
                    "q=%(query)s&num=%(num)d&start=%(start)d&tbs=%(tbs)s&" \
                    "safe=%(safe)s&tbm=%(tpe)s"

# Cookie jar. Stored at the user's home folder.
home_folder = os.getenv('HOME')
if not home_folder:
    home_folder = os.getenv('USERHOME')
    if not home_folder:
        home_folder = '.'   # Use the current folder on error.
cookie_jar = LWPCookieJar(os.path.join(home_folder, '.google-cookie'))
try:
    cookie_jar.load()
except Exception:
    pass

# Default user agent, unless instructed by the user to change it.
USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'

# Load the list of valid user agents from the install folder.
install_folder = os.path.abspath(os.path.split(__file__)[0])
user_agents_file = os.path.join(install_folder, 'user_agents.txt')
try:
    with open(user_agents_file) as fp:
        user_agents_list = [_.strip() for _ in fp.readlines()]
except Exception:
    user_agents_list = [USER_AGENT]


# Get a random user agent.
def get_random_user_agent():
    """
    Get a random user agent string.

    @rtype:  str
    @return: Random user agent string.
    """
    return random.choice(user_agents_list)


# Request the given URL and return the response page, using the cookie jar.
def get_page(url, user_agent=None):
    """
    Request the given URL and return the response page, using the cookie jar.

    @type  url: str
    @param url: URL to retrieve.

    @type  user_agent: str
    @param user_agent: User agent for the HTTP requests. Use C{None} for the
        default.

    @rtype:  str
    @return: Web page retrieved for the given URL.

    @raise IOError: An exception is raised on error.
    @raise urllib2.URLError: An exception is raised on error.
    @raise urllib2.HTTPError: An exception is raised on error.
    """
    if user_agent is None:
        user_agent = USER_AGENT
    request = Request(url)
    request.add_header('User-Agent', USER_AGENT)
    cookie_jar.add_cookie_header(request)
    response = urlopen(request)
    cookie_jar.extract_cookies(response, request)
    html = response.read()
    response.close()
    cookie_jar.save()
    return html


# Filter links found in the Google result pages HTML code.
# Returns None if the link doesn't yield a valid result.
def filter_result(link):
    try:

        # Valid results are absolute URLs not pointing to a Google domain
        # like images.google.com or googleusercontent.com
        o = urlparse(link, 'http')
        if o.netloc and 'google' not in o.netloc:
            return link

        # Decode hidden URLs.
        if link.startswith('/url?'):
            link = parse_qs(o.query)['q'][0]

            # Valid results are absolute URLs not pointing to a Google domain
            # like images.google.com or googleusercontent.com
            o = urlparse(link, 'http')
            if o.netloc and 'google' not in o.netloc:
                return link

    # Otherwise, or on error, return None.
    except Exception:
        pass
    return None


# Shortcut to search images
# Beware, this does not return the image link.
def search_images(query, tld='com', lang='en', tbs='0', safe='off', num=10,
                  start=0, stop=None, pause=2.0, domains=None,
                  only_standard=False, extra_params={}):
    return search(query, tld, lang, tbs, safe, num, start, stop, domains,
                  pause, only_standard, extra_params, tpe='isch')


# Shortcut to search news
def search_news(query, tld='com', lang='en', tbs='0', safe='off', num=10,
                start=0, stop=None, domains=None, pause=2.0,
                only_standard=False, extra_params={}):
    return search(query, tld, lang, tbs, safe, num, start, stop, domains,
                  pause, only_standard, extra_params, tpe='nws')


# Shortcut to search videos
def search_videos(query, tld='com', lang='en', tbs='0', safe='off', num=10,
                  start=0, stop=None, domains=None, pause=2.0,
                  only_standard=False, extra_params={}):
    return search(query, tld, lang, tbs, safe, num, start, stop, domains,
                  pause, only_standard, extra_params, tpe='vid')


# Shortcut to search shop
def search_shop(query, tld='com', lang='en', tbs='0', safe='off', num=10,
                start=0, stop=None, domains=None, pause=2.0,
                only_standard=False, extra_params={}):
    return search(query, tld, lang, tbs, safe, num, start, stop, domains,
                  pause, only_standard, extra_params, tpe='shop')


# Shortcut to search books
def search_books(query, tld='com', lang='en', tbs='0', safe='off', num=10,
                 start=0, stop=None, domains=None, pause=2.0,
                 only_standard=False, extra_params={}):
    return search(query, tld, lang, tbs, safe, num, start, stop, domains,
                  pause, only_standard, extra_params, tpe='bks')


# Shortcut to search apps
def search_apps(query, tld='com', lang='en', tbs='0', safe='off', num=10,
                start=0, stop=None, domains=None, pause=2.0,
                only_standard=False, extra_params={}):
    return search(query, tld, lang, tbs, safe, num, start, stop, domains,
                  pause, only_standard, extra_params, tpe='app')


# Shortcut to single-item search. Evaluates the iterator to return the single
# URL as a string.
def lucky(query, tld='com', lang='en', tbs='0', safe='off',
          only_standard=False, extra_params={}, tpe=''):
    gen = search(query, tld, lang, tbs, safe, 1, 0, 1, 0., only_standard,
                 extra_params, tpe)
    return next(gen)


# Returns a generator that yields URLs.
def search(query, tld='com', lang='en', tbs='0', safe='off', num=10, start=0,
           stop=None, domains=None, pause=2.0, only_standard=False,
           extra_params={}, tpe='', user_agent=None):
    """
    Search the given query string using Google.

    @type  query: str
    @param query: Query string. Must NOT be url-encoded.

    @type  tld: str
    @param tld: Top level domain.

    @type  lang: str
    @param lang: Language.

    @type  tbs: str
    @param tbs: Time limits (i.e "qdr:h" => last hour,
        "qdr:d" => last 24 hours, "qdr:m" => last month).

    @type  safe: str
    @param safe: Safe search.

    @type  num: int
    @param num: Number of results per page.

    @type  start: int
    @param start: First result to retrieve.

    @type  stop: int
    @param stop: Last result to retrieve.
            Use C{None} to keep searching forever.

    @type  domains: list
    @param domains: A list of web domains to constrain the search.

    @type  pause: float
    @param pause: Lapse to wait between HTTP requests.
        A lapse too long will make the search slow, but a lapse too short may
        cause Google to block your IP. Your mileage may vary!

    @type  only_standard: bool
    @param only_standard: If C{True}, only returns the standard results from
        each page. If C{False}, it returns every possible link from each page,
        except for those that point back to Google itself. Defaults to C{False}
        for backwards compatibility with older versions of this module.

    @type  extra_params: dict
    @param extra_params: A dictionary of extra HTTP GET parameters, which must
        be URL encoded. For example if you don't want google to filter similar
        results you can set the extra_params to {'filter': '0'} which will
        append '&filter=0' to every query.

    @type  tpe: str
    @param tpe: Search type (images, videos, news, shopping, books, apps)
            Use the following values {videos: 'vid', images: 'isch',
                                      news: 'nws', shopping: 'shop',
                                      books: 'bks', applications: 'app'}

    @type  user_agent: str
    @param user_agent: User agent for the HTTP requests. Use C{None} for the
        default.

    @rtype:  generator
    @return: Generator (iterator) that yields found URLs. If the C{stop}
        parameter is C{None} the iterator will loop forever.
    """
    # Set of hashes for the results found.
    # This is used to avoid repeated results.
    hashes = set()

    # Prepare domain list if it exists.
    if domains:
        domain_query = '+OR+'.join('site:' + domain for domain in domains)
    else:
        domain_query = ''

    # Prepare the search string.
    query = quote_plus(query + '+' + domain_query)

    # Check extra_params for overlapping
    for builtin_param in ('hl', 'q', 'btnG', 'tbs', 'safe', 'tbm'):
        if builtin_param in extra_params.keys():
            raise ValueError(
                'GET parameter "%s" is overlapping with \
                the built-in GET parameter',
                builtin_param
            )

    # Grab the cookie from the home page.
    get_page(url_home % vars())

    # Prepare the URL of the first request.
    if start:
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()
    else:
        if num == 10:
            url = url_search % vars()
        else:
            url = url_search_num % vars()

    # Loop until we reach the maximum result, if any (otherwise, loop forever).
    while not stop or start < stop:

        try:  # Is it python<3?
            iter_extra_params = extra_params.iteritems()
        except AttributeError:  # Or python>3?
            iter_extra_params = extra_params.items()
        # Append extra GET_parameters to URL
        for k, v in iter_extra_params:
            url += url + ('&%s=%s' % (k, v))

        # Sleep between requests.
        time.sleep(pause)

        # Request the Google Search results page.
        html = get_page(url)

        # Parse the response and process every anchored URL.
        if is_bs4:
            soup = BeautifulSoup(html, 'html.parser')
        else:
            soup = BeautifulSoup(html)
        anchors = soup.find(id='search').findAll('a')
        for a in anchors:

            # Leave only the "standard" results if requested.
            # Otherwise grab all possible links.
            if only_standard and (
                    not a.parent or a.parent.name.lower() != "h3"):
                continue

            # Get the URL from the anchor tag.
            try:
                link = a['href']
            except KeyError:
                continue

            # Filter invalid links and links pointing to Google itself.
            link = filter_result(link)
            if not link:
                continue

            # Discard repeated results.
            h = hash(link)
            if h in hashes:
                continue
            hashes.add(h)

            # Yield the result.
            yield link

        # End if there are no more results.
        if not soup.find(id='nav'):
            break

        # Prepare the URL for the next request.
        start += num
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()


# Returns only the number of Google hits for the given search query.
# This is the number reported by Google itself, NOT by scraping.
def hits(query, tld='com', lang='en', tbs='0', safe='off',
         domains=None, extra_params={}, tpe='', user_agent=None):
    """
    Search the given query string using Google and return the number of hits.

    @note: This is the number reported by Google itself, NOT by scraping.

    @type  query: str
    @param query: Query string. Must NOT be url-encoded.

    @type  tld: str
    @param tld: Top level domain.

    @type  lang: str
    @param lang: Language.

    @type  tbs: str
    @param tbs: Time limits (i.e "qdr:h" => last hour,
            "qdr:d" => last 24 hours, "qdr:m" => last month).

    @type  safe: str
    @param safe: Safe search.

    @type  domains: list
    @param domains: A list of web domains to constrain the search.

    @type  extra_params: dict
    @param extra_params: A dictionary of extra HTTP GET parameters, which must
        be URL encoded. For example if you don't want google to filter similar
        results you can set the extra_params to {'filter': '0'} which will
        append '&filter=0' to every query.

    @type  tpe: str
    @param tpe: Search type (images, videos, news, shopping, books, apps)
            Use the following values {videos: 'vid', images: 'isch',
                                      news: 'nws', shopping: 'shop',
                                      books: 'bks', applications: 'app'}

    @type  user_agent: str
    @param user_agent: User agent for the HTTP requests. Use C{None} for the
            default.

    @rtype:  int
    @return: Number of Google hits for the given search query.
    """

    # Prepare domain list if it exists.
    if domains:
        domain_query = '+OR+'.join('site:' + domain for domain in domains)
    else:
        domain_query = ''

    # Prepare the search string.
    query = quote_plus(query + '+' + domain_query)

    # Check extra_params for overlapping
    for builtin_param in ('hl', 'q', 'btnG', 'tbs', 'safe', 'tbm'):
        if builtin_param in extra_params.keys():
            raise ValueError(
                'GET parameter "%s" is overlapping with \
                the built-in GET parameter',
                builtin_param
            )

    # Grab the cookie from the home page.
    get_page(url_home % vars())

    # Prepare the URL of the first (and in this cases ONLY) request.
    url = url_search % vars()

    try:  # Is it python<3?
        iter_extra_params = extra_params.iteritems()
    except AttributeError:  # Or python>3?
        iter_extra_params = extra_params.items()
    # Append extra GET_parameters to URL
    for k, v in iter_extra_params:
        url += url + ('&%s=%s' % (k, v))

    # Request the Google Search results page.
    html = get_page(url)

    # Parse the response.
    if is_bs4:
        soup = BeautifulSoup(html, 'html.parser')
    else:
        soup = BeautifulSoup(html)

    # Get the number of hits.
    tag = soup.find_all(attrs={"class": "sd", "id": "resultStats"})[0]
    return int(tag.text.split()[1].replace(',', ''))


def ngd(term1, term2):
    """ Return the Normalized Google distance between words.

    For more info, refer to:
    https://en.wikipedia.org/wiki/Normalized_Google_distance

    @type  term1: str
    @param term1: First term to compare.

    @type  term1: str
    @param term1: Second term to compare.

    @rtype: float
    @return: Normalized Google distance between words.
    """

    lhits1 = math.log10(hits(term1))
    lhits2 = math.log10(hits(term2))
    lhits_mix = math.log10(hits('"' + term1 + '" "' + term2 + '"'))
    npages = hits('the')
    fix = 1000

    lN = math.log10(npages * fix)
    numerator = max([lhits1, lhits2]) - lhits_mix
    denomin = lN - min([lhits1, lhits2])

    return numerator / denomin
