from typing import Optional, Union, Callable, Dict
import logging
import sys
import os
from pathlib import Path
from abc import abstractmethod
from pydoc import locate
import sqlalchemy as sa
from sqlalchemy.engine.cursor import LegacyCursorResult
from pydantic import BaseModel
from abc import ABC
import importlib.util
import sys
from load.sql_enums import FileTypes

"""
execute string query
execute sqlalchemy query

get query from .sql file
get query from .py file - `query` function

"""


class SQLQuery:
    """
    Mixin with methods for executing queries from .sql files
    """

    def __init__(self):
        super(SQLQuery, self).__init__()
        self.filetype = FileTypes.SQL.value
        self.query_execute_functions[self.filetype] = self._execute_sql_query
        self.query_find_functions[self.filetype] = self._find_sql_query

    def _execute_sql_query(self, query: str, **kwargs):
        with self.engine.connect() as conn:
            result = conn.execute(query, **kwargs)
        return result

    @staticmethod
    def _find_sql_query(file_path: str):
        with open(file_path, "r") as f:
            query = sa.text(f.read())
        return query


class PyQuery:
    """
    Mixin with methods for executing queries from .py files
    """

    def __init__(self):
        super(PyQuery, self).__init__()
        self.filetype = FileTypes.PY.value
        self.query_execute_functions[self.filetype] = self._execute_py_query
        self.query_find_functions[self.filetype] = self._find_py_query

    def _execute_py_query(self, query: sa.select, **kwargs):
        with self.engine.connect() as conn:
            result = conn.execute(query(**kwargs))
        return result

    @staticmethod
    def _find_py_query(file_path: str) -> sa.select:
        spec = importlib.util.spec_from_file_location("query", file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["query"] = module
        spec.loader.exec_module(module)
        return module.query


class SQLBase(ABC):
    def __init__(self, query_directory=None, conn_string=None):
        self.query_directory: Optional[str] = query_directory
        self.conn_string: Optional[str] = conn_string

        self.query_execute_functions = dict()
        self.query_find_functions = dict()

        super(SQLBase, self).__init__()

    @property
    def logger(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.handlers = [handler]
        return logger

    @property
    @abstractmethod
    def _credentials(self) -> None:
        """
        Abstact property to be implemented in child classes.
        Client-specific credentials/configurations for connecting
        to database.
        """
        pass

    @property
    def engine(self) -> sa.engine.base.Engine:
        """
        Property for executing SQL queries, either
        string representations or SQLAlchemy select objects.
        """
        return sa.engine.create_engine(self.conn_string, **self._credentials)

    def validate_query_file(self, query_file: str) -> None:
        """
        Validate a query file based on its filetype.

        If using a .py file, expects a `query` function,
        which will be invoked via `pydoc.locate` to return a sqlalchemy
        select object, and executed with sqlalchemy

        If using a .sql file, expects a plain text query,
        which will be read via IO, and executed with sqlalchemy

        Parameters
        ----------
        query_file: str
            Name of the file containing the query to validate.
        """
        file_path = Path(query_file)
        # make sure file exists and has valid extension
        if file_path.suffix not in self.query_find_functions:
            raise NotImplementedError(
                f"You used a {file_path.suffix} file. "
                + "Use one of the following filetypes:\n"
                + f"{', '.join(list(self.query_find_functions))}"
            )

        if not os.path.exists(query_file):
            raise FileNotFoundError(
                f"{query_file} does not exist!"
                + f"Check {self.query_directory} for your file."
            )

    def log_query(self, query, kwargs):
        self.logger.info(f"{'Executing Query':-^40}")
        self.logger.info(str(query))
        self.logger.info(f"{'With Parameters':-^40}")
        for key, value in kwargs.items():
            self.logger.info(f"{key}: {value}")
        self.logger.info(f"{'':-^40}")

    def execute_query_from_file(
        self, query_file: str, return_results: Optional[bool] = False, **kwargs
    ) -> Optional[LegacyCursorResult]:
        """
        Execute a query from its file, optionally returning the resulting
        cursor object.

        Params
        ------
        query_file: str
        return_results: Optional[bool]

        Returns
        -------

        """
        full_file_path = os.path.join(self.query_directory, query_file)
        find_query_function = self.get_find_query_function(full_file_path)
        execute_query_function = self.get_execute_query_function(
            full_file_path
        )

        query = find_query_function(full_file_path)
        self.log_query(query, kwargs)

        results = execute_query_function(query, **kwargs)
        if return_results is True:
            return results.fetchall()

    def _get_query_function(
        self, full_file_path: str, functions: dict
    ) -> Callable:
        """
        Prototype function for getting filetype-sepcific
        """
        self.validate_query_file(full_file_path)
        file_suffix = Path(full_file_path).suffix
        query_function = functions[file_suffix]
        return query_function

    def get_find_query_function(self, full_file_path: str) -> Callable:
        """
        Return a function to execute a query based on its filetype
        Also validate the query file
        """
        return self._get_query_function(
            full_file_path,
            self.query_find_functions,
        )

    def get_execute_query_function(self, full_file_path: str):
        return self._get_query_function(
            full_file_path,
            self.query_execute_functions,
        )

    def reflect_table(self, table_name, schema_name):
        return sa.Table(
            table_name,
            sa.MetaData(),
            schema=schema_name,
            autoload=True,
            autoload_with=self.engine,
        )
