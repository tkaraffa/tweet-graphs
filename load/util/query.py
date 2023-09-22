from abc import ABC, abstractmethod, abstractproperty
from typing import Optional, Callable, Union
from importlib.util import spec_from_file_location, module_from_spec
import sys
from dataclasses import dataclass, field

import sqlalchemy as sa

from util.sql_enums import FileType


@dataclass(frozen=True)
class Query(ABC):
    """
    Abstract class for executing queries from files using SQLAlchemy
    """

    @abstractproperty
    def filetype(self):
        """Abstract property for class's file type"""

    @staticmethod
    @abstractmethod
    def execute_query(engine: sa.engine, query: str, **kwargs):
        """Abstract method for executing a query"""

    @staticmethod
    @abstractmethod
    def find_query(file_path: str):
        """Abstract method for finding a query from a file"""

    @staticmethod
    @abstractmethod
    def get_query_string(query: Union[Callable, sa.sql.elements.TextClause]):
        """Abstract method for getting the string rep of a query"""


@dataclass(frozen=True)
class SQLQuery(Query):
    """
    Class that supports executing queries from .sql files
    """

    filetype: FileType = FileType.SQL

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

    @staticmethod
    def get_query_string(query: sa.sql.elements.TextClause) -> str:
        return str(query)


@dataclass(frozen=True)
class PyQuery(Query):
    filetype: FileType = FileType.PY

    @staticmethod
    def execute_query(engine: sa.engine, query: sa.select, **kwargs):
        with engine.connect() as conn:
            result = conn.execute(query(**kwargs))
        return result

    @staticmethod
    def find_query(
        file_path: str, function_name: Optional[str] = "query"
    ) -> sa.select:
        spec = spec_from_file_location(function_name, file_path)
        module = module_from_spec(spec)
        sys.modules[function_name] = module
        spec.loader.exec_module(module)
        return getattr(module, function_name)

    @staticmethod
    def get_query_string(query: Callable) -> str:
        return str(query())
