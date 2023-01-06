import importlib.util
import sys

import sqlalchemy as sa

from load.sql_enums import FileTypes


class BaseQuery:
    """
    Base class for query mixins to ensure required attributes
    """

    def __init__(self):
        self.query_execute_functions = (
            self.query_execute_functions
            if hasattr(self, "query_execute_functions")
            else dict()
        )
        self.query_find_functions = (
            self.query_find_functions
            if hasattr(self, "query_find_functions")
            else dict()
        )


class SQLQuery(BaseQuery):
    """
    Mixin with methods for executing queries from .sql files
    """

    def __init__(self):
        super(SQLQuery, self).__init__()

        self.sql_filetype = FileTypes.SQL.value
        self.query_execute_functions[
            self.sql_filetype
        ] = self._execute_sql_query
        self.query_find_functions[self.sql_filetype] = self._find_sql_query

    @staticmethod
    def _execute_sql_query(engine, query: str, **kwargs):
        with engine.connect() as conn:
            result = conn.execute(query, **kwargs)
        return result

    @staticmethod
    def _find_sql_query(file_path: str):
        with open(file_path, "r") as f:
            query = sa.text(f.read())
        return query


class PyQuery(BaseQuery):
    """
    Mixin with methods for executing queries from .py files
    """

    def __init__(self):
        super(PyQuery, self).__init__()
        self.py_filetype = FileTypes.PY.value
        self.query_execute_functions[self.py_filetype] = self._execute_py_query
        self.query_find_functions[self.py_filetype] = self._find_py_query

    @staticmethod
    def _execute_py_query(engine, query: sa.select, **kwargs):
        with engine.connect() as conn:
            result = conn.execute(query(**kwargs))
        return result

    @staticmethod
    def _find_py_query(
        file_path: str, function_name: str = "query"
    ) -> sa.select:
        spec = importlib.util.spec_from_file_location(function_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[function_name] = module
        spec.loader.exec_module(module)
        return module.query
