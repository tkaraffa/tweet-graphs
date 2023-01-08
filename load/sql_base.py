from typing import Optional, Callable, List, Tuple, Dict, Union
import logging
import sys
import os
from pathlib import Path
from abc import ABC
from dataclasses import dataclass, field

import sqlalchemy as sa

from load.query import SQLQuery, PyQuery, Query


@dataclass
class SQLBase(ABC):
    conn_string: str
    credentials: dict
    query_directory: Optional[str] = field(default_factory=str)

    @property
    def queriers(self) -> Dict[str, Query]:
        return {query.filetype: query() for query in {SQLQuery, PyQuery}}

    @property
    def logger(self) -> logging.Logger:
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
    def engine(self) -> sa.engine.base.Engine:
        """
        Property for executing SQL queries, either
        string representations or SQLAlchemy select objects.
        """
        return sa.engine.create_engine(self.conn_string, **self.credentials)

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

        Raises
        ------
        FileNotFoundError:
            if file does not exist in the instantiated query directory

        NotImplementedError
            if file is of an unsupported type
        """
        full_file_path = os.path.join(self.query_directory, query_file)
        file_suffix = Path(query_file).suffix
        # make sure file exists and has valid extension
        if not os.path.exists(full_file_path):
            raise FileNotFoundError(
                f"{full_file_path} does not exist!"
                + f"Check {self.query_directory} for your file."
            )
        if file_suffix not in self.queriers:
            raise NotImplementedError(
                f"You used a {file_suffix} file. "
                + "Use one of the following filetypes:\n"
                + f"{', '.join(self.queriers)}"
            )

    def execute_query_from_file(
        self,
        query_file: str,
        return_results: Optional[bool] = False,
        **kwargs,
    ) -> Optional[List[Tuple]]:
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
        file_suffix = Path(query_file).suffix

        querier = self.queriers.get(file_suffix)
        query = querier.find_query(full_file_path)

        self.log_query(query, **kwargs)

        results = querier.execute_query(self.engine, query, **kwargs)
        if return_results is True:
            return results.fetchall()

    def reflect_table(self, table_name, schema_name):
        return sa.Table(
            table_name,
            sa.MetaData(),
            schema=schema_name,
            autoload=True,
            autoload_with=self.engine,
        )

    def log_query(
        self,
        query: Union[sa.sql.elements.TextClause, Callable],
        **kwargs,
    ) -> None:
        self.logger.info(f"{'Executing Query':-^40}")
        if isinstance(query, sa.sql.elements.TextClause):
            self.logger.info(str(query))
        elif isinstance(query, Callable):
            self.logger.info(str(query()))

        # self.logger.info(str(query))
        self.logger.info(f"{'With Parameters':-^40}")
        for key, value in kwargs.items():
            self.logger.info(f"{key}: {value}")
        self.logger.info(f"{'':-^40}")
