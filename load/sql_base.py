import os
from pathlib import Path
from pydoc import locate
import sqlalchemy as sa
from pydantic import BaseModel
from util.gcp_utils import get_credentials


class SQLBase(BaseModel):
    query_suffix: str = ".py"
    query_path = "load.queries.{file_path}.query"

    @property
    def query_directory(self):
        return os.path.join(os.path.dirname(__file__), "queries")

    @property
    def _credentials(self):
        return get_credentials()

    @property
    def engine(self):
        return sa.engine.create_engine(
            "bigquery://",
            **self._credentials,
        )

    def validate_query_file(self, file_path):
        # make sure file exists
        if file_path.suffix not in (self.query_suffix, ""):
            raise NotImplementedError(
                f"You used a {file_path.suffix} file. "
                + f"Use either a stem or a {self.query_suffix} file!"
            )
        full_file_path = os.path.join(
            self.query_directory, file_path.with_suffix(self.query_suffix)
        )
        if not os.path.exists(full_file_path):
            raise FileNotFoundError(
                f"{full_file_path} does not exist!"
                + f"Check {self.query_directory} for your file."
            )

    def get_query(self, query_file: str, **kwargs) -> sa.select:
        """
        Find a .py file and return the select object
        representation of its contents.

        Params
        ------
        filename: str
            The filename containing the query function to return

        Returns
        -------
        query: str
            The sqlalchemy.select representation of the query
        """
        file_path = Path(query_file)
        self.validate_query_file(file_path)
        query = locate(self.query_path.format(file_path=file_path))
        return query(**kwargs)
