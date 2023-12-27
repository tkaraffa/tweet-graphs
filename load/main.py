"""
Load data from a source to a table,
using a user-provided .sql or .py file.
"""

import argparse
import json
from util.sql_enums import Connector
from util.sql_base import SQLBase


def get_connector(connector_name: str) -> SQLBase:
    return Connector[connector_name].value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "query",
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
    query_file = args.query
    params = args.params
    return_results = args.return_results
    credentials = args.credentials
    sql = connector(credentials=credentials)

    res = sql.execute_query_from_file(
        query_file, return_results=return_results, **params
    )
    if return_results:
        print(res)


if __name__ == "__main__":
    main()
