from typing import Any, Optional
import os
from dataclasses import dataclass, field

from util.sql_base import SQLBase
from util.sql_enums import ConnectionString


@dataclass
class SQLSqlite(SQLBase):
    credentials: Optional[dict[str, str]] = None
    credentials_default: dict[str, str] = field(
        init=False,
        repr=False,
        default_factory=lambda: {"database": os.getenv("SQLITE_DB")},
    )

    conn_string: ConnectionString = field(init=False, default=ConnectionString.SQLITE)
