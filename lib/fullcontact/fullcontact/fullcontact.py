import json
import logging
import requests
import sys
if sys.version_info[0] < 3:
    import urllib
else:
    import urllib.parse as urllib

log = logging.getLogger(__name__)


class FullContact(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.fullcontact.com/v2/'
        self.get_endpoints = {
            'person': 'person.json',
            'company': 'company/lookup.json',
            'company_search': 'company/search.json',
            'disposable': 'email/disposable.json',
            'name_normalizer': 'name/normalizer.json',
            'name_deducer': 'name/deducer.json',
            'name_similarity': 'name/similarity.json',
            'name_stats': 'name/stats.json',
            'name_parser': 'name/parser.json',
            'address_locationNormalizer': 'address/locationNormalizer.json',
            'address_locationEnrichment': 'address/locationEnrichment.json',
            'account_stats': 'stats.json'
        }
        self.post_endpoints = {
            'batch': 'batch.json'
        }

        for endpoint in self.get_endpoints:
            method = lambda endpoint=endpoint, **kwargs: self.api_get(endpoint, **kwargs)
            setattr(self, endpoint, method)

    def api_get(self, endpoint, **kwargs):
        """ Makes a FullContact API call

        Formats and submits a request to the specified endpoint, appending
        any key-value pairs passed in kwargs as a url query parameter.

        Args:
            endpoint: shortname of the API endpoint to use.
            strict: if True, throw an error
            **kwargs: a dict of query parameters to append to the request.

        Returns:
            A Requests object containing the result of the API call. Interact
            with the return value of this function as you would with any
            other Requests object.

        Raises:
            KeyError: the specified endpoint was not recognized. Check the
                docs.
            Requests.Exceptions.*: an error was raised by the Requests
                module.
        """

        headers = {'X-FullContact-APIKey': self.api_key}
        endpoint = self.base_url + self.get_endpoints[endpoint]
        return requests.get(endpoint, params=kwargs, headers=headers)

    def _prepare_batch_url(self, b):
        """ Format a url to submit to the batch API

        Args:
            b: a tuple of (str, dict) containing the endpoint for
                the request and a dict of url parameters (note:
                the api key doesn't need to be included for
                individual requests within a batch since it is
                appended to the batch API call.

        Returns:
            A formatted url to append to the batch request's payload.
        """
        ep = self.get_endpoints[b[0]]
        qu = urllib.urlencode(b[1])
        batch_url = '{0}{1}?{2}'.format(self.base_url, ep, qu)
        log.debug('Prepared batch url: {0}'.format(batch_url))

        return batch_url

    def api_batch(self, batch_calls):
        """ Submit a batch request to the fullcontact API

        You may POST up to 20 requests per call the batch endpoint,
        although this limit is not enforced by the function. Responding
        to invalid requests will be handled by the API and should be
        coded against outside this module.

        Args:
            batch_calls: a list of tuples of (str, dict) identifying
                endpoint to make a GET request to as well as the
                parameters to append to that request.

        Returns:
            A Requests object containing the results of all batched
            requests contained in the batch_calls list.

        Resources:
            https://www.fullcontact.com/developer/docs/batch/

        """
        payload = [self._prepare_batch_url(b) for b in batch_calls]
        headers = {'content-type': 'application/json',
                   'X-FullContact-APIKey': self.api_key}
        data = json.dumps({'requests': payload})
        endpoint = self.base_url + self.post_endpoints['batch']

        return requests.post(endpoint, data=data, headers=headers)

    def query_emails(self, *emails):
        """
        Accept one or many email addresses, and place a single or batch query
        for all to fetch contact information. Returns a list of results.
        """
        # TODO: Validate emails?
        if len(emails) == 0:
            raise ValueError("Must provide at least one email to use.")
        elif len(emails) == 1:
            # Single API call
            r = self.api_get('person', email=emails[0]).json()
            o = {emails[0]: r}
        else:
            # Batch API call
            r = self.api_batch([('person', {'email': e}) for e in emails])
            responses = r.json()['responses']
            o = {}
            for e in emails:
                req = self._prepare_batch_url(('person', {'email': e}))
                if req in responses:
                    o[e] = responses[req]
        # API returns 404 for absent data.. restful, but may break batch?
        # r.raise_for_status()
        return o
