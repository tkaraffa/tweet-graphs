from typing import Callable, Union
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

from util.gcp_utils import upload_file_to_bucket


class JSONLFormat:
    """
    Mixin to add functionality for writing data to JSON files.
    """

    def __init__(self):
        super(JSONLFormat, self).__init__()
        self.jsonl_file_format = FileFormats.JSONL.value
        self.file_format_functions[
            self.jsonl_file_format
        ] = self._write_jsonl_file

    @staticmethod
    def _write_jsonl_file(data: list, filename: str) -> None:
        """
        Write data to a .jsonl file

        Paramters
        ---------
        data: list
            List of JSONL data to write
        filename: str
            Filename to write
        """
        with open(filename, "w+") as f:
            for line in data:
                json.dump(line, f)
                f.write("\n")

    @staticmethod
    def check_jsonl(filename: str) -> str:
        """
        Check that a file has the extension .jsonl

        Parameters
        ---------
        filename: str
            The filename to check

        Returns
        -------
        filename: str

        Raises
        ------
        TypeError
            if not a .jsonl file
        """
        if not filename.endswith(FileFormats.JSONL.value):
            raise TypeError(
                f"Please use {FileFormats.JSONL.value} file extension."
            )
        return filename


class CSVFormat:
    """
    Mixin to add functionality for writing data to CSV files.
    """

    def __init__(self):
        super(CSVFormat, self).__init__()
        self.csv_file_format = FileFormats.CSV.value
        self.file_format_functions[self.csv_file_format] = self._write_csv_file

    @staticmethod
    def _write_csv_file(data: list, filename: str) -> None:
        """
        Write data to a .csv file

        Paramters
        ---------
        data: list
            List of CSV data to write
        filename: str
            Filename to write
        """
        with open(filename, "w+") as f:
            writer = csv.writer(f)
            writer.writerows(data)

    @staticmethod
    def check_csv(filename: str) -> str:
        """
        Check that a file has the extension .csv

        Parameters
        ---------
        filename: str
            The filename to check

        Returns
        -------
        filename: str

        Raises
        ------
        TypeError
            if not a .csv file
        """
        if not filename.endswith(FileFormats.CSV.value):
            raise TypeError(
                f"Please use {FileFormats.CSV.value} file extension."
            )
        return filename


class APIBase(JSONLFormat, CSVFormat):
    """
    General-purpose class for making API requests.
    """

    def __init__(self) -> None:
        self.file_format_functions = dict()
        super(APIBase, self).__init__()
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
    def validation_function(
        self, response: urllib.request.Request
    ) -> urllib.request.Request:
        "Abstract method for API-specific validation functions."
        return response

    @staticmethod
    def _encode_payload(payload: dict = None) -> str:
        "Encodes payload for a request."
        if payload is not None:
            return json.dumps(payload).encode("utf-8")

    def create_request(
        self,
        host: str,
        endpoint: str,
        scheme: str = None,
        query: str = None,
        headers: dict = None,
        payload: dict = None,
        params: dict = None,
    ) -> urllib.request.Request:
        """
        Construct a request with optional payload

        """
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

    def _send_request(self, request: urllib.request.Request) -> str:
        """
        Attempt to open a request, with the instantiated timeout

        Paramters
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
        self, func: Callable, url: str, **kwargs
    ) -> Union[str, None]:
        tries = self.tries
        logger = self.logger
        delay = self.delay
        backoff = self.backoff

        while tries > 1:
            try:
                result = func(url, **kwargs)
                if (
                    self.validation_func is not None
                    and self.validation_func(result) is True
                ):
                    raise ValidationException
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

    def pull_request_data(
        self, request: urllib.request.Request, **kwargs
    ) -> str:
        data = self._retry_request(self._send_request, request, **kwargs)
        return data

    def write_and_upload(
        self, data: list, filename: str, bucket: str, **kwargs
    ) -> None:
        file_extension = Path(filename).suffix
        try:
            write_func = self.file_format_functions[file_extension]
            write_func(data=data, filename=filename)
            upload_file_to_bucket(filename, bucket, **kwargs)
        except KeyError:
            raise NotImplementedError(
                f"Type {type} is not implemented yet. "
                f"Only {', '.join(self.file_format_functions)} are supported."
            )
        finally:
            os.remove(filename)
