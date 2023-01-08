from abc import ABC, abstractmethod
from typing import Optional
import importlib.util
import sys
from dataclasses import dataclass, field

import sqlalchemy as sa

from load.sql_enums import FileTypes


@dataclass(frozen=True)
class Query(ABC):
    @staticmethod
    @abstractmethod
    def execute_query(engine: sa.engine, query: str, **kwargs):
        """Abstract method for executing a query"""

    @staticmethod
    @abstractmethod
    def find_query(file_path: str):
        """Abstract method for finding a query from a file"""


@dataclass(frozen=True)
class SQLQuery(Query):
    filetype: str = field(default=FileTypes.SQL.value, init=False)

    @staticmethod
    def execute_query(engine: sa.engine, query: str, **kwargs):
        with engine.connect() as conn:
            result = conn.execute(query, **kwargs)
        return result

    @staticmethod
    def find_query(file_path: str):
        with open(file_path, "r") as f:
            query = sa.text(f.read())
        return query


@dataclass(frozen=True)
class PyQuery(Query):
    filetype: str = field(default=FileTypes.PY.value, init=False)

    @staticmethod
    def execute_query(engine: sa.engine, query: sa.select, **kwargs):
        with engine.connect() as conn:
            result = conn.execute(query(**kwargs))
        return result

    @staticmethod
    def find_query(
        file_path: str, function_name: Optional[str] = "query"
    ) -> sa.select:
        spec = importlib.util.spec_from_file_location(function_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[function_name] = module
        spec.loader.exec_module(module)
        return module.query
