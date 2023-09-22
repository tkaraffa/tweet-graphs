from typing import Any
import os
from dataclasses import dataclass, field

from util.sql_base import SQLBase
from util.sql_enums import ConnectionString


@dataclass
class SQLSqlite(SQLBase):
    credentials: dict[str, str] = field(
        default_factory=lambda: {"database": os.getenv("SQLITE_DB")}
    )

    conn_string: ConnectionString = ConnectionString.SQLITE
