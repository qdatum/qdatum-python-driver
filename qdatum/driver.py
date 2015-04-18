from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import str
from builtins import object
from future import standard_library
standard_library.install_aliases()
import json
import requests
import urllib
import logging
from requests_futures.sessions import FuturesSession

from functools import wraps
from qdatum.errors import *

standard_library.install_aliases()

logger = logging.getLogger(__name__)
__version__ = '0.0.5'


class ResponseParser(object):
    def __init__(self, rsp):
        self.rsp = rsp

    def parse(self, raw=False):
        if self.rsp.status_code in [200, 201]:
            if raw is True:
                return self.rsp

            if self.rsp.headers['content-type'] == 'application/json':
                data = self.rsp.json()
                logger.debug('RESPONSE: %s', json.dumps(data))
            else:
                data = self.rsp.text
                logger.debug('RESPONSE: %s', self.rsp.text)

            logger.info('STATUS_CODE: %s', self.rsp.status_code)
            if data is None:
                raise QdatumApiError('empty response from server')
            return data
        elif self.rsp.status_code == 400:
            raise QdatumBadRequestError(self.rsp)
        elif self.rsp.status_code == 404:
            raise QdatumPageNotFoundError(self.rsp)
        elif self.rsp.status_code in [401]:
            raise QdatumNoAuth(self.rsp)
        else:
            raise QdatumApiError(
                'Unknown status code from server: ' + str(self.rsp.status_code))


class Session(object):
    def __init__(self, token=None, api_endpoint=None, async=False):
        if async is True:
            self.session = FuturesSession()
        else:
            self.session = requests.Session()

        self.api_endpoint = api_endpoint
        self.token = token

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        del self.session

    def _request(func):
        @wraps(func)
        def wrapped(inst, *args, **kwargs):
            try:
                return func(inst, *args, **kwargs)
            except requests.exceptions.ConnectionError:
                raise QdatumApiError(
                    'connection refused, bad connection or server down')

        return wrapped

    def post(self, path, payload, stream=False):
        return self.get_response_parser(self.post_async(path, payload, stream=stream).result()).parse()

    @_request
    def post_async(self, path, payload, stream=False):
        url = self.api_endpoint + path
        headers = {'content-type': 'application/json',
                        'User-Agent': 'qdatum-python-driver; {0}'.format(__version__)}
        if self.token is not None:
            headers['Authorization'] = self.token

        logger.info('POST: %s', url)
        logger.debug(json.dumps(payload))
        return self.session.post(url, headers=headers, data=json.dumps(payload), stream=stream)

    def get(self, *argv, **kwargs):
        return self.get_response_parser(self.get_async(*argv, **kwargs).result()).parse()

    @_request
    def get_async(self, path, stream=False, **kwargs):
        url = self.api_endpoint + path
        headers = {'content-type': 'application/json',
                        'User-Agent': 'qdatum-python-driver; {0}'.format(__version__)}
        if self.token is not None:
            headers['Authorization'] = self.token

        logger.info('GET: %s => %s', url, json.dumps(kwargs))
        if len(kwargs) > 0:
            url = '{0}?{1}'.format(url, urllib.parse.urlencode(kwargs))

        return self.session.get(url, headers=headers, stream=stream)

    def put(self, *argv, **kwargs):
        return self.get_response_parser(self.put_async(*argv, **kwargs).result()).parse()

    @_request
    def put_async(self, path, payload, stream=False, **kwargs):
        url = self.api_endpoint + path
        headers = {'content-type': 'application/json' if 'mime' not in kwargs else kwargs['mime'],
                        'User-Agent': 'qdatum-python-driver; {0}'.format(__version__)}
        if self.token is not None:
            headers['Authorization'] = self.token

        logger.info('PUT: %s', url)

        return self.session.put(url, data=payload, headers=headers, stream=stream)

    def get_response_parser(self, rsp):
        return ResponseParser(rsp)


class Driver(object):
    """Wraps API calls for slightly easier use
    """

    __default_api_endpoint = 'http://api.qdatum.io/v1'

    def __init__(self, api_endpoint=None, email=None, password=None, token=None):
        self.token = token
        self.api_endpoint = api_endpoint if api_endpoint is not None else self.__default_api_endpoint
        self.session = self.create_session(async=True)

        if email is not None and password is not None:
            self.connect(email, password)

    def connect(self, email, password):
        data = self.session.post('/auth', {
            'email': email,
            'password': password
        })
        self.user = data['user']
        self.token = data['token']
        self.session.token = self.token

    def close(self):
        del self.session

    @classmethod
    def _authenticated(cls, func):
        @wraps(func)
        def wrapped(inst, *args, **kwargs):
            if inst.token is None:
                raise QdatumApiError(
                    'Tried to call a method that requires a token, but no token is available')
            return func(inst, *args, **kwargs)
        return wrapped

    def create_session(self, *args, **kwargs):
        kwargs['api_endpoint'] = self.api_endpoint
        kwargs['token'] = self.token
        return Session(*args, **kwargs)
