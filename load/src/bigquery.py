from typing import Any, Optional
import os
from dataclasses import dataclass, field
from enum import Enum

from util.sql_base import SQLBase
from util.sql_enums import ConnectionString


@dataclass
class SQLBigquery(SQLBase):
    credentials: Optional[dict[str, str]] = None
    credentials_default: dict[str, str] = field(
        init=False,
        repr=False,
        default_factory=lambda: dict(
            credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        ),
    )

    conn_string: ConnectionString = field(init=False, default=ConnectionString.BIGQUERY)
