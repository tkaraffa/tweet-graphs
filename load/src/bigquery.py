from typing import Any
import os
from dataclasses import dataclass, field

from util.sql_base import SQLBase
from util.sql_enums import ConnectionStrings


@dataclass
class SQLBigquery(SQLBase):
    credentials: dict[str, str] = field(
        default_factory=lambda: dict(
            credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
    )

    conn_string: str = field(
        default=ConnectionStrings.BIGQUERY.value, init=False
    )