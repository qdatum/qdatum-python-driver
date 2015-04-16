import json
import requests
import urllib
import logging

from functools import wraps
from qdatum.errors import *

logger = logging.getLogger(__name__)
VERSION = '0.0.2'


class Query():

    def __init__(self, path, api_endpoint=None, token=None, stream=False, **kwargs):
        self.api_endpoint = api_endpoint
        self.url = self.api_endpoint + path
        self.stream = stream
        self.headers = {'content-type': 'application/json',
                        'User-Agent': 'qdatum-python-driver; {0}'.format(VERSION)}
        if token is not None:
            self.headers['Authorization'] = token

    def __request(func):
        @wraps(func)
        def wrapped(inst, *args, **kwargs):
            try:
                response = func(inst, *args, **kwargs)
                if response.status_code in [200, 201]:
                    if inst.stream is True:
                        return response

                    if response.headers['content-type'] == 'application/json':
                        data = response.json()
                        logger.debug('RESPONSE: %s', json.dumps(data))
                    else:
                        data = response.text
                        logger.debug('RESPONSE: %s', response.text)

                    logger.info('STATUS_CODE: %s', response.status_code)
                    if data is None:
                        raise QdatumApiError('empty response from server')
                    return data
                elif response.status_code in [400, 404]:
                    raise QdatumBadRequestError(response)
                elif response.status_code in [401]:
                    raise QdatumNoAuth(response)
                else:
                    raise QdatumApiError(
                        'Unknown status code from server: ' + str(response.status_code))
            except requests.exceptions.ConnectionError:
                raise QdatumApiError(
                    'connection refused, bad connection or server down')

        return wrapped

    @__request
    def post(self, payload):
        logger.info('POST: %s', self.url)
        logger.debug(json.dumps(payload))
        return requests.post(self.url, data=json.dumps(payload), headers=self.headers)

    @__request
    def get(self, **kwargs):
        logger.info('GET: %s => %s', self.url, json.dumps(kwargs))
        if len(kwargs) > 0:
            self.url = self.url + '?' + urllib.parse.urlencode(kwargs)

        return requests.get(self.url, stream=self.stream, headers=self.headers)

    @__request
    def put_stream(self, pusher):
        self.headers['content-type'] = pusher.get_mime()
        logger.info('PUT_STREAM: %s', self.url)
        s = requests.Session()
        req = requests.Request('PUT', self.url, headers=self.headers, data=pusher.read())
        rsp = s.send(req.prepare(), stream=True)
        return rsp


class Driver():
    """Wraps API calls for slightly easier use
    """

    __default_api_endpoint = 'http://api.qdatum.io/v1'

    def __init__(self, api_endpoint=None, email=None, password=None, token=None):
        self.token = token
        self.api_endpoint = api_endpoint if api_endpoint is not None else self.__default_api_endpoint
        if email is not None and password is not None:
            self.connect(email, password)

    def connect(self, email, password):
        data = self.query('/auth').post({
            'email': email,
            'password': password
        })
        self.user = data['user']
        self.token = data['token']

    @classmethod
    def _authenticated(cls, func):
        @wraps(func)
        def wrapped(inst, *args, **kwargs):
            if inst.token is None:
                raise QdatumApiError(
                    'Tried to call a method that requires a token, but no token is available')
            return func(inst, *args, **kwargs)
        return wrapped

    def query(self, *args, **kwargs):
        kwargs['api_endpoint'] = self.api_endpoint
        kwargs['token'] = self.token
        return Query(*args, **kwargs)
