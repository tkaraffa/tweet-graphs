import os
from dataclasses import dataclass, field

from load.sql_base import SQLBase
from load.sql_enums import ConnectionStrings


@dataclass
class SQLBigquery(SQLBase):
    conn_string: str = field(default=ConnectionStrings.BIGQUERY.value, init=False)

    @property
    def _credentials(self):
        return dict(credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
