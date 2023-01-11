from typing import Any
import os
from dataclasses import dataclass, field
from enum import Enum

from util.sql_base import SQLBase
from util.sql_enums import ConnectionStrings


@dataclass
class SQLBigquery(SQLBase):
    credentials: dict[str, str] = field(
        default_factory=lambda: dict(
            credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
    )

    conn_string: ConnectionStrings = field(
        default=ConnectionStrings.BIGQUERY, init=False
    )
