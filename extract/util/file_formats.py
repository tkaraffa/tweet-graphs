import json
import csv
from pathlib import Path
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from extract.util.api_enums import FileFormats


class Formatter(ABC):
    file_format: str

    @staticmethod
    @abstractmethod
    def write_file(data: list, filename: str) -> None:
        """Abstract method for writing a file"""

    def check_file(self, filename: str) -> str:
        """
        Check that a file has the correct extension

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
            if the file does not have the appropriate extension
        """
        file_suffix = Path(filename).suffix
        if file_suffix != self.file_format:
            raise TypeError(f"Please use {self.file_format} file extension.")
        return filename


@dataclass
class JSONLFormatter(Formatter):
    """
    Formatter for checking and writing JSONL files
    """

    file_format: str = field(default=FileFormats.JSONL.value, init=False)

    @staticmethod
    def write_file(data: list, filename: str) -> None:
        """
        Write data to a .jsonl file

        Parameters
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


@dataclass
class CSVFormatter(Formatter):
    """
    Formatter for checking and writing CSV files
    """

    file_format: str = field(default=FileFormats.CSV.value, init=False)

    @staticmethod
    def write_file(data: list, filename: str) -> None:
        """
        Write data to a .csv file

        Parameters
        ---------
        data: list
            List of CSV data to write
        filename: str
            Filename to write
        """
        with open(filename, "w+") as f:
            writer = csv.writer(f)
            writer.writerows(data)
