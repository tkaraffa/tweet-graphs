import urllib.parse
import urllib.request
import urllib.error
import json
from socket import timeout
from time import sleep
from abc import abstractmethod

from util.api_enums import APIEnums
from util.api_exceptions import ValidationException


class APIBase:
    def __init__(self) -> None:
        self.exception = (
            urllib.error.HTTPError,
            urllib.error.URLError,
            timeout,
        )
        self.tries = 10
        self.delay = 3
        self.backoff = 2
        self.logger = None
        self.timeout = 15

        self.scheme = APIEnums.SCHEME.value

    @abstractmethod
    def validation_function(self, response):
        """Abstract method for API-specific validation functions."""
        return response

    @staticmethod
    def _encode_payload(payload=None):
        if payload is not None:
            return json.dumps(payload).encode("utf-8")

    def format_url():
        pass

    def create_request(
        self,
        host,
        endpoint,
        scheme=None,
        query=None,
        headers=None,
        payload=None,
        params=None,
    ):
        scheme = scheme or self.scheme
        netloc = host
        path = endpoint
        params = params
        query = urllib.parse.urlencode(query, doseq=True) if query else None
        fragment = None
        url = urllib.parse.urlunparse(
            (scheme, netloc, path, params, query, fragment)
        )

        request = urllib.request.Request(
            url, headers=headers, data=self._encode_payload(payload)
        )
        return request

    def _send_request(self, request):
        timeout = self.timeout
        with urllib.request.urlopen(request, timeout=timeout) as r:
            data = r.read().decode()
        return data

    def _retry_request(self, func, url, **kwargs):
        tries = self.tries
        logger = self.logger
        delay = self.delay
        backoff = self.backoff

        while tries > 1:
            try:
                result = func(url, **kwargs)
                if self.validation_func is not None:
                    if self.validation_func(result) is not True:
                        raise self.ValidationException
                return result
            except Exception as e:
                if isinstance(e, ValidationException):
                    message = f"{self.validation_func.__doc__}. Retrying in {delay} seconds."
                else:
                    message = f"{str(e)}. Retrying in {delay} seconds."
                print(message)
                if logger is not None:
                    logger.warning(message)
                sleep(delay)
                tries -= 1
                delay *= backoff

    def pull_request_data(self, request, **kwargs):
        data = self._retry_request(self._send_request, request, **kwargs)
        if data:
            return data

    @staticmethod
    def write_json_file(json_data, filename="results.json"):
        with open(filename, "w+") as f:
            json.dump(json_data, f, sort_keys=True, indent=2)
