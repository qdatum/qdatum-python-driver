import json

__all__ = [
    "QdatumApiError", "QdatumBadRequestError", "QdatumNoAuth"
]


class QdatumApiError(Exception):

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def to_json(self):
        rsp = dict(self.payload if hasattr(self, 'payload') else ())
        rsp['error'] = self.message
        return rsp

    def __str__(self):
        return self.message + ' ' + json.dumps(self.payload or ())


class QdatumBadRequestError(QdatumApiError):

    def __init__(self, response):
        QdatumApiError.__init__(self, 'Bad Request')
        try:
            self.payload = {'response': response.json()}
        except ValueError:
            self.payload = {'response': response.text}


class QdatumNoAuth(QdatumApiError):

    def __init__(self, response):
        QdatumApiError.__init__(self, 'Not authorized')
        try:
            self.payload = {'response': response.json()}
        except ValueError:
            self.payload = {'response': response.text}
