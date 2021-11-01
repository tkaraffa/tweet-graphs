import urllib.parse
import urllib.request
import urllib.error
import json
import csv
from socket import timeout
from time import sleep
from abc import abstractmethod
import os
from pathlib import Path

from util.api_enums import APIEnums, FileFormats
from util.api_exceptions import ValidationException

from util.gcs_utils import upload_file_to_bucket


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

        self.file_formats = self.file_format_functions()

    def file_format_functions(self):
        """When a new file fomatted is added, it must be added in several places:
        * in api_enums.py in FileFormats
        * in this file in a _write_<file_format>_file method
        * in this function's format_functions dictionary
        """
        formats = {i.value for i in FileFormats}
        format_functions = {
            FileFormats.CSV.value: self._write_csv_file,
            FileFormats.JSON.value: self._write_json_file,
        }

        not_implemented = formats.symmetric_difference(set(format_functions))
        if not_implemented:
            raise NotImplementedError(
                "Some formats do not have write functions implemented:"
                f"{', '.join(list(not_implemented))}"
            )
        return format_functions

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
    def _write_json_file(data, filename):
        with open(filename, "w+") as f:
            for line in data:
                json.dump(line, f)
                f.write("\n")

    @staticmethod
    def _write_csv_file(data, filename):
        with open(filename, "w+") as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def write_and_upload(self, data, filename, bucket, **kwargs):

        file_extension = Path(filename).suffix
        write_func = self.file_formats.get(file_extension)
        if not write_func:
            raise NotImplementedError(
                f"Type {type} is not implemented yet. "
                f"Only {', '.join(self.file_formats)} are supported."
            )

        write_func(data=data, filename=filename)
        upload_file_to_bucket(filename, bucket, **kwargs)
        os.remove(filename)
