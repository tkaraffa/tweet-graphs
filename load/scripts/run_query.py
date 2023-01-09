"""
Load data from a source to a table,
using a user-provided .sql or .py file.
"""

import argparse
import json

from src.bigquery import SQLBigquery


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
    return parser.parse_args()


def main():
    args = parse_args()

    query_file = args.query
    params = args.params
    return_results = args.return_results

    sql = SQLBigquery()

    res = sql.execute_query_from_file(
        query_file, return_results=return_results, **params
    )
    if return_results:
        print(res)


if __name__ == "__main__":
    main()
