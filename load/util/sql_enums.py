from enum import Enum
from src.bigquery import SQLBigQuery
from src.sqllite import SQLSqlLite


class ConnectionString(Enum):
    BIGQUERY = "bigquery"
    SQLITE = "sqlite"


class Connector(Enum):
    BIGQUERY = SQLBigQuery
    SQLLITE = SQLSqlLite


class FileType(Enum):
    PY = ".py"
    SQL = ".sql"
