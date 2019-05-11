
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import re
import traceback
import sys
from random import choice

try:
	# Python 3
	from urllib import request
	from html.parser import HTMLParser # keep it to avoid warning
	from urllib.parse import quote, unquote
	# local
	from core.useragents import user_agents # works in tests
	try:
		from html import unescape  # Python 3.4+
	except ImportError:
		pass
except ImportError:
	pass

# placeholder
isPython2 = sys.version.startswith('2')


def download(query, num_results):
	"""
	downloads HTML after google search
	"""
	# https://stackoverflow.com/questions/11818362/how-to-deal-with-unicode-string-in-url-in-python3
	name = quote(query)

	name  = name.replace(' ','+')
	url = 'http://www.google.com/search?q=' + name
	if num_results != 10:
		url += '&num=' + str(num_results)  # adding this param might hint Google towards a bot
	req = request.Request(url, headers={
		'User-Agent' : choice(user_agents),
		# 'Referer': 'google.com'
	})
	try:
		response = request.urlopen(req)
	except Exception:  # catch connection issues
		# may also catch 503 rate limit exceed
		print('ERROR\n')
		traceback.print_exc()
		return ''
	# response.read is bytes in Py 3
	if isPython2:
		# trick: decode unicode as early as possible
		data = response.read().decode('utf8', errors='ignore')
	else:
		data = str(response.read(), 'utf-8', errors='ignore')
	# print(data)
	return data


def is_url(url):
	"""
	checks if :url is a url
	"""
	regex = r'((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)'
	return re.match(regex, url) is not None


def prune_html(text):
	"""
	https://stackoverflow.com/a/42461722/2295672
	"""
	text = re.sub(r'<.*?>', '', text)
	return text


def convert_unicode(text):
	"""
	converts unicode HTML to real Unicode
	"""
	if isPython2:
		h = HTMLParser()
		s = h.unescape(text)
	else:
		try:
			s = unescape(text)
		except Exception:
			# Python 3.3 and below
			# https://stackoverflow.com/a/2360639/2295672
			s = HTMLParser().unescape(text)
	return s


def search(query, num_results=10):
	"""
	searches google for :query and returns a list of tuples
	of the format (name, url)
	"""
	data = download(query, num_results)
	results = re.findall(r'\<h3.*?\>.*?\<\/h3\>', data, re.IGNORECASE)
	if results is None or len(results) == 0:
		print('No results where found. Did the rate limit exceed?')
		return []
	# search has results
	links = []
	for r in results:
		mtch = re.match(r'.*?a\s*?href=\"(.*?)\".*?\>(.*?)\<\/a\>.*$', r, flags=re.IGNORECASE)
		if mtch is None:
			continue
		# parse url
		url = mtch.group(1)
		# clean url https://github.com/aviaryan/pythons/blob/master/Others/GoogleSearchLinks.py
		url = re.sub(r'^.*?=', '', url, count=1) # prefixed over urls \url=q?
		url = re.sub(r'\&amp.*$', '', url, count=1) # suffixed google things
		url = unquote(url)
		# url = re.sub(r'\%.*$', '', url) # NOT SAFE, causes issues with Youtube watch url
		# parse name
		name = prune_html(mtch.group(2))
		name = convert_unicode(name)
		# append to links
		if is_url(url): # can be google images result
			links.append((name, url))
	return links


def gsearch(target):
	"""
	CLI endpoint to run the program
	"""
	print(target)
	#query=t.name.replace('http://','').replace('https://','')
	results = search(target)
	# output
	if type(results) == list:
		ct = 1
		for r in results:
			print(str(ct) + '.', r[0] + '\n  ' + r[1])
			ct += 1
	else:
		print(results)