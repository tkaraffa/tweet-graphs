from typing import Callable, Union, Optional
import urllib.parse
import urllib.request
import urllib.error
import json
from socket import timeout
from time import sleep
from abc import ABC, abstractmethod
import os
import logging
from dataclasses import dataclass, field

from util.api_enums import APIEnums
from util.api_exceptions import ValidationException
from util.dates import DateFormatter
from util.gcp_utils import GCPUtil


@dataclass
class APIBase(ABC):
    """
    General-purpose class for making API requests.
    """

    cloud_util: Union[GCPUtil]

    tries: int = 10
    delay: int = 3
    backoff: int = 2
    timeout: int = 15
    logger: logging.Logger = None
    scheme: str = field(default=APIEnums.SCHEME.value)

    date_formatter: DateFormatter = DateFormatter()

    @property
    @abstractmethod
    def file_formatter(self):
        """Abstract property for file formatter"""

    @property
    @abstractmethod
    def filename(self) -> str:
        """Abstract method for creating file name in which to write data."""

    @property
    def exceptions(self):
        return (
            urllib.error.HTTPError,
            urllib.error.URLError,
            timeout,
            ValidationException,
        )

    @abstractmethod
    def validation_function(
        self, response: urllib.request.Request
    ) -> urllib.request.Request:
        """Abstract method for API-specific validation functions."""

    @staticmethod
    def _encode_payload(payload: dict = None) -> Optional[bytes]:
        """Encodes payload for a request."""
        if payload is not None:
            return json.dumps(payload).encode("utf-8")

    def create_request(
        self,
        host: str,
        endpoint: str,
        query: str = None,
        headers: dict = None,
        payload: dict = None,
        params: dict = None,
        safe: str = None,
    ) -> urllib.request.Request:
        """
        Construct a request with optional payload

        """
        query = (
            urllib.parse.urlencode(query, safe=safe, doseq=True)
            if query is not None
            else None
        )
        data = self._encode_payload(payload)

        components = (self.scheme, host, endpoint, params, query, None)
        url = urllib.parse.urlunparse(components)
        request = urllib.request.Request(url, headers=headers, data=data)
        return request

    def _send_request(self, request: urllib.request.Request) -> str:
        """
        Attempt to open a request, with the instantiated timeout

        Parameters
        ---------
        request: urllib.request.Request
            The request to try

        Returns
        -------
        data: str
            The decoded data from the request
        """
        with urllib.request.urlopen(request, timeout=self.timeout) as r:
            data = r.read().decode()
        return data

    def _retry_request(
        self, func: Callable, url: urllib.request.Request, **kwargs
    ) -> Union[str, None]:
        tries = self.tries
        delay = self.delay

        print(url.full_url)

        while tries > 1:
            try:
                result = func(url, **kwargs)
                # if self.validation_function(result) is False:
                #     raise self.validation_exception
                return result
            except Exception as e:
                if e in self.exceptions:
                    message = f"{str(e)}. Retrying in {delay} seconds."
                else:
                    raise e
                print(message)
                if self.logger is not None:
                    self.logger.warning(message)
                sleep(delay)
                tries -= 1
                delay *= self.backoff

    def pull_request_data(
        self, request: urllib.request.Request, **kwargs
    ) -> str:
        """
        Retry _send_request with allowable exceptions

        Parameters
        ----------
        request: urllib.request.Request
        :param request:
        :param kwargs:
        :return:
        """
        data = self._retry_request(self._send_request, request, **kwargs)
        return data

    @abstractmethod
    def get_responses():
        """Abstract method for getting API responses"""

    # this should really write to temp files
    def write_and_upload(self, bucket: str, **kwargs) -> None:
        try:
            self.file_formatter.write_file(
                data=self.data, filename=self.filename
            )
            self.cloud_util.upload_file_to_bucket(filename, bucket, **kwargs)
        except Exception as e:
            raise e
        finally:
            os.remove(filename)
