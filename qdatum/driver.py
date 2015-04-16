import json
import requests
import urllib
import logging

from functools import wraps
from .errors import *

logger = logging.getLogger(__name__)


class Query():

    def __init__(self, path, api_endpoint=None, token=None, stream=False, **kwargs):
        self.api_endpoint = api_endpoint
        self.url = self.api_endpoint + path
        self.stream = stream
        self.headers = {'content-type': 'application/json',
                        'User-Agent': 'qdatum-client; 0.1-python'}
        if token is not None:
            self.headers['Authorization'] = token

    def _request(func):
        @wraps(func)
        def wrapped(inst, *args, **kwargs):
            try:
                response = func(inst, *args, **kwargs)
                if response.status_code in [200, 201]:
                    if inst.stream is True:
                        return response

                    if response.headers['content-type'] == 'application/json':
                        data = response.json()
                        logger.debug(json.dumps(data))
                    else:
                        data = response.text

                    logger.info('STATUS_CODE: %s', response.status_code)
                    if data is None:
                        raise QdatumApiError('empty response from server')
                    return data
                elif response.status_code in [400, 404]:
                    print(repr(response))
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

    @_request
    def post(self, payload):
        logger.info('POST: %s', self.url)
        logger.debug(json.dumps(payload))
        return requests.post(self.url, data=json.dumps(payload), headers=self.headers)

    @_request
    def files(self, files):
        logger.info('FILES: %s', self.url)
        data = files['file'].read()
        return requests.post(self.url, data=data, headers=self.headers)

    @_request
    def data(self, data):
        logger.info('DATA: %s', self.url)
        return requests.post(self.url, data=data.encode('utf-8'), headers=self.headers)

    @_request
    def get(self, params=None):
        logger.info('GET: %s => %s', self.url, json.dumps(params))
        if params is not None:
            self.url = self.url + '?' + urllib.parse.urlencode(params)

        return requests.get(self.url, stream=self.stream, headers=self.headers)

    @_request
    def put_stream(self, pusher):
        self.headers['content-type'] = pusher.get_mime()
        logger.info('PUT_STREAM: %s', self.url)
        s = requests.Session()
        req = requests.Request('PUT', self.url, headers=self.headers, data=pusher.read())
        prepped = req.prepare()
        rsp = s.send(prepped, stream=True)
        return rsp


class Driver():
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 2
    STATUS_PENDING = 3
    STATUS_FAILED = 9
    STATUS_DONE = 10
    STATUS_DELETED = 11

    TAP_ACCESS_PUBLIC = 1
    TAP_ACCESS_SUBSCRIBERS = 2
    TAP_ACCESS_PRIVATE = 3

    DATA_STATE_NOT_MATERIALIZED = 1
    DATA_STATE_MATERIALIZED = 2
    DATA_STATE_READ_ONLY = 3
    DATA_STATE_REQUEST_REBUILD = 4
    DATA_STATE_REBUILDING = 5
    DATA_STATE_REQUEST_TRUNCATE = 6

    """Wraps API calls for slightly easier use
    """

    def __init__(self, api_endpoint, email=None, password=None, token=None):
        self.token = token

        self.api_endpoint = api_endpoint
        if (email is not None and password is not None) or token is not None:
            self.connect(email, password, token)

    def connect(self, email, password, token):
        if token is None:
            data = self.query('/auth').post({
                'email': email,
                'password': password
            })
            self.user = data['user']
            self.token = data['token']
        else:
            self.token = token

    @classmethod
    def _authenticated(cls, func):
        @wraps(func)
        def wrapped(inst, *args, **kwargs):
            if inst.token is None:
                raise QdatumApiError(
                    'Tried to call a method that requires a user, but no user is assigned')
            return func(inst, *args, **kwargs)
        return wrapped

    def query(self, *args, **kwargs):
        kwargs['api_endpoint'] = self.api_endpoint
        kwargs['token'] = self.token
        return Query(*args, **kwargs)
