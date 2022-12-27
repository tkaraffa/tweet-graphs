from enum import Enum


class ConnectionStrings(Enum):
    BIGQUERY = "bigquery://"


class FileTypes(Enum):
    PY = ".py"
    SQL = ".sql"
