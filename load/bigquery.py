import os

from load.sql_base import SQLBase
from load.query import SQLQuery, PyQuery
from load.sql_enums import ConnectionStrings


class SQLBigquery(SQLBase, SQLQuery):
    def __init__(self, query_directory):
        super(SQLBigquery, self).__init__(
            query_directory=query_directory,
            conn_string=ConnectionStrings.BIGQUERY.value,
        )

    @property
    def _credentials(self):
        return dict(
            credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
