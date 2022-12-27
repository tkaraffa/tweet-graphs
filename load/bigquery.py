import os

from load.sql_base import SQLBase
from load.sql_enums import ConnectionStrings


class SQLBigquery(SQLBase):
    query_directory: str = None

    def __init__(self, query_directory):
        super().__init__(
            query_directory=query_directory,
            conn_string=ConnectionStrings.BIGQUERY.value,
        )

    @property
    def _credentials(self):
        return dict(
            credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
