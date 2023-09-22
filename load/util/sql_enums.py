from enum import Enum


class ConnectionString(Enum):
    BIGQUERY = "bigquery"
    SQLITE = "sqlite"


class FileType(Enum):
    PY = ".py"
    SQL = ".sql"
