import requests
import json
from urllib import parse
from requests.exceptions import RequestException

import figure
from figure import error


def _build_api_url(url, query):
    scheme, netloc, path, base_query, fragment = parse.urlsplit(url)

    if base_query:
        query = '%s&%s' % (base_query, query)

    return parse.urlunsplit((scheme, netloc, path, query, fragment))


class APIRequestor(object):

    def __init__(self, token, api_base=None):

        self.api_base = api_base or figure.api_base
        self.token = token

    def __set_content_type(self, headers, ctype):
        headers.update({'Content-Type': ctype})

    def __set_authorization(self, headers, token):
        headers.update(
            {'Authorization': 'Bearer {:s}'.format(token)})

    def __get(self, url, headers, timeout, data=None, files=None):
        return requests.get(url, headers=headers, timeout=timeout)

    def __post(self, url, headers, timeout, data, files=None):
        return requests.post(url, data=data, files=files, headers=headers, timeout=timeout)

    def __put(self, url, headers, timeout, data=None, files=None):
        return requests.put(url, data=data, files=files, headers=headers, timeout=timeout)

    def __patch(self, url, headers, timeout, data=None, files=None):
        return requests.patch(url, data=data, headers=headers, timeout=timeout)

    def __head(self, url, headers, timeout, data=None, files=None):
        return requests.head(url, headers=headers, timeout=timeout)


    def _handle_api_error(self, rbody, rcode):

        if rcode == 400:
            raise error.BadRequestError(status=rcode, body=rbody)

        if rcode == 401:
            raise error.AuthenticationError(status=rcode, body=rbody)

        if rcode == 403:
            raise error.AuthorizationError(status=rcode, body=rbody)

        if rcode == 404:
            raise error.NotFoundError(status=rcode, body=rbody)

        if rcode == 405:
            raise error.MethodNotAllowedError(status=rcode, body=rbody)

        if rcode == 429:
            raise error.RateLimitError(status=rcode, body=rbody)

        if rcode == 500:
            raise error.InternalServerError(status=rcode, body=rbody)

        if rcode == 502:
            raise error.APIConnectionError(status=rcode, body=rbody)

        if rcode == 503:
            raise error.APIConnectionError(status=rcode, body=rbody)

        raise error.FigureError(message="Something went wrong", status=rcode)

    def _interpret_response(self, rbody, rcode):
        if not (200 <= rcode < 300):
            self._handle_api_error(rbody, rcode)
        try:
            resp = json.loads(rbody)
        except Exception:
            raise error.FigureError("Invalid response body from API", rcode, rbody)
        return resp

    def request(self, method, url, data=None, files=None, query=None, headers=None, timeout=60):
        """
        Mechanism for issuing an API call
        """
        headers = headers or {}

        if self.token:
            my_token = self.token
        else:
            from figure import token
            my_token = token

        if my_token:
            self.__set_authorization(headers, my_token)

        METHODS = {
            'get': self.__get,
            'post': self.__post,
            'put': self.__put,
            'head': self.__head,
            'patch': self.__patch
        }
        request_method = METHODS[method.lower()]

        abs_url = parse.urljoin(self.api_base, url)

        encoded_query = parse.urlencode(query or {})

        abs_url = _build_api_url(abs_url, encoded_query)

        try:
            response = request_method(abs_url, data=data, files=files, headers=headers, timeout=timeout)
            response.encoding = 'utf-8'
        except RequestException:
            raise error.APIConnectionError()

        return self._interpret_response(response.text, response.status_code)


