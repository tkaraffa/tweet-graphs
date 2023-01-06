from util.api_enums import FileFormats


class BaseFormat:
    """
    Base for file format mixins to ensure required attribute exists
    """

    def __init__(self):
        self.file_format_functions = (
            self.file_format_functions
            if hasattr(self, "file_format_functions")
            else dict()
        )


class JSONLFormat(BaseFormat):
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


class CSVFormat(BaseFormat):
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
