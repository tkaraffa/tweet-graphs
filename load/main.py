"""
Load data from a source to a table,
using a user-provided .sql or .py file.
"""

import argparse
import json
from enum import Enum
from util.sql_base import SQLBase
from util.filter_args import filter_args
from src.bigquery import SQLBigquery
from src.sqlite import SQLSqlite


class Connector(Enum):
    BIGQUERY = SQLBigquery
    SQLLITE = SQLSqlite


def get_connector(connector_name: str) -> SQLBase:
    print(connector_name)
    return Connector[connector_name.upper()].value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "query_file",
        type=str,
        help="The query file to run.",
    )
    parser.add_argument(
        "--params",
        type=json.loads,
        default=dict(),
        help="Any JSON-formatted parameters to pass to the query file",
    )
    parser.add_argument(
        "--return_results",
        "-r",
        action="store_true",
        help="Flag for whether or not to return the results of the query.",
    )
    parser.add_argument(
        "--connector",
        "-c",
        type=get_connector,
        help="The database connector to use.",
        required=True,
    )
    parser.add_argument(
        "--credentials",
        type=json.loads,
        help="Credentials to use for the database connection.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    connector = args.connector
    connector_args = filter_args(args, include_keys=["credentials"])
    execute_args = filter_args(
        args,
        include_keys=[
            "query_file",
            "return_results",
            "params",
        ],
    )

    return_results = args.return_results

    sql = connector(**connector_args)
    res = sql.execute_query_from_file(**execute_args)
    if return_results:
        print(res)


if __name__ == "__main__":
    main()
