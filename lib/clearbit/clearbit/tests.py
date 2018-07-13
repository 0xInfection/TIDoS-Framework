import sys
import unittest

if sys.version_info > (3, 3):
    from unittest.mock import patch
else:
    from mock import patch

import clearbit
from clearbit import *

clearbit.key = 'k'

class TestResource(unittest.TestCase):
    @patch('clearbit.resource.requests')
    def test_clearbit_key(self, requests):
        Resource.get('http://x.clearbit.com/test', key='mykey')
        requests.get.assert_called_with('http://x.clearbit.com/test', params={}, auth=('mykey', ''))

    @patch('clearbit.resource.requests')
    def test_stream(self, requests):
        Resource.get('http://x.clearbit.com/test', stream=True)
        requests.get.assert_called_with('http://x-stream.clearbit.com/test', params={}, auth=('k', ''))

class TestPerson(unittest.TestCase):
    @patch('clearbit.resource.requests')
    def test_webhook_url(self, requests):
        Person.find(email='user@example.com', webhook_url='http://webhook.com/webhook')
        requests.get.assert_called_with('https://person.clearbit.com/v2/people/find', params={'email': 'user@example.com', 'webhook_url': 'http://webhook.com/webhook'}, auth=('k', ''))

    @patch('clearbit.resource.requests')
    def test_webhook_id(self, requests):
        Person.find(email='user@example.com', webhook_id='myid')
        requests.get.assert_called_with('https://person.clearbit.com/v2/people/find', params={'email': 'user@example.com', 'webhook_id': 'myid'}, auth=('k', ''))

    @patch('clearbit.resource.requests')
    def test_subscribe(self, requests):
        Person.find(email='user@example.com', subscribe=True)
        requests.get.assert_called_with('https://person.clearbit.com/v2/people/find', params={'email': 'user@example.com', 'subscribe': True}, auth=('k', ''))

    @patch('clearbit.resource.requests')
    def test_endpoint(self, requests):
        Person.find(email='user@example.com')
        requests.get.assert_called_with('https://person.clearbit.com/v2/people/find', params={'email': 'user@example.com'}, auth=('k', ''))

    @patch('clearbit.resource.requests')
    def test_find_by_id(self, requests):
        Person.find(id='theid')
        requests.get.assert_called_with('https://person.clearbit.com/v2/people/theid', params={}, auth=('k', ''))

    @patch('clearbit.resource.requests')
    def test_flag(self, requests):
        person = Person(id='theid')
        person.flag(given_name='John')
        requests.post.assert_called_with('https://person.clearbit.com/v2/people/theid/flag', json={'given_name': 'John'}, auth=('k', ''))

class TestCompany(unittest.TestCase):
    @patch('clearbit.resource.requests')
    def test_webhook_url(self, requests):
        Company.find(domain='example.com', webhook_url='http://webhook.com/webhook')
        requests.get.assert_called_with('https://company.clearbit.com/v2/companies/find', params={'domain': 'example.com', 'webhook_url': 'http://webhook.com/webhook'}, auth=('k', ''))

    @patch('clearbit.resource.requests')
    def test_webhook_id(self, requests):
        Company.find(domain='example.com', webhook_id='myid')
        requests.get.assert_called_with('https://company.clearbit.com/v2/companies/find', params={'domain': 'example.com', 'webhook_id': 'myid'}, auth=('k', ''))

    @patch('clearbit.resource.requests')
    def test_subscribe(self, requests):
        Company.find(domain='example.com', subscribe=True)
        requests.get.assert_called_with('https://company.clearbit.com/v2/companies/find', params={'domain': 'example.com', 'subscribe': True}, auth=('k', ''))

    @patch('clearbit.resource.requests')
    def test_endpoint(self, requests):
        Company.find(domain='example.com')
        requests.get.assert_called_with('https://company.clearbit.com/v2/companies/find', params={'domain': 'example.com'}, auth=('k', ''))

    @patch('clearbit.resource.requests')
    def test_find_by_id(self, requests):
        Company.find(id='theid')
        requests.get.assert_called_with('https://company.clearbit.com/v2/companies/theid', params={}, auth=('k', ''))

    @patch('clearbit.resource.requests')
    def test_flag(self, requests):
        company = Company(id='theid')
        company.flag(name='ACME Inc')
        requests.post.assert_called_with('https://company.clearbit.com/v2/companies/theid/flag', json={'name': 'ACME Inc'}, auth=('k', ''))

class TestEnrichment(unittest.TestCase):
    @patch('clearbit.resource.requests')
    def test_webhook_url(self, requests):
        Enrichment.find(email='user@example.com', webhook_url='http://webhook.com/webhook')
        requests.get.assert_called_with('https://person.clearbit.com/v2/combined/find', params={'email': 'user@example.com', 'webhook_url': 'http://webhook.com/webhook'}, auth=('k', ''))

    @patch('clearbit.resource.requests')
    def test_webhook_id(self, requests):
        Enrichment.find(email='user@example.com', webhook_id='myid')
        requests.get.assert_called_with('https://person.clearbit.com/v2/combined/find', params={'email': 'user@example.com', 'webhook_id': 'myid'}, auth=('k', ''))

    @patch('clearbit.resource.requests')
    def test_subscribe(self, requests):
        Enrichment.find(email='user@example.com', subscribe=True)
        requests.get.assert_called_with('https://person.clearbit.com/v2/combined/find', params={'email': 'user@example.com', 'subscribe': True}, auth=('k', ''))

    @patch('clearbit.resource.requests')
    def test_endpoint(self, requests):
        Enrichment.find(email='user@example.com')
        requests.get.assert_called_with('https://person.clearbit.com/v2/combined/find', params={'email': 'user@example.com'}, auth=('k', ''))

class TestProspector(unittest.TestCase):
    @patch('clearbit.resource.requests')
    def test_search(self, requests):
        Prospector.search(domain='example.com')
        requests.get.assert_called_with('https://prospector.clearbit.com/v1/people/search', params={'domain': 'example.com'}, auth=('k', ''))

    @patch('clearbit.resource.requests')
    def test_search_titles(self, requests):
        Prospector.search(domain='example.com', titles=['Sales Director', 'Marketing Director'])
        requests.get.assert_called_with('https://prospector.clearbit.com/v1/people/search', params={'domain': 'example.com', 'titles[]': ['Sales Director', 'Marketing Director']}, auth=('k', ''))

class TestNameToDomain(unittest.TestCase):
    @patch('clearbit.resource.requests')
    def test_find(self, requests):
        NameToDomain.find(name='Uber')
        requests.get.assert_called_with('https://company.clearbit.com/v1/domains/find', params={'name': 'Uber'}, auth=('k', ''))

if __name__ == '__main__':
    unittest.main()
