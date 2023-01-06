"""
Load data from a source to a table,
using a user-provided SQL file.
"""

import argparse
import os
from pathlib import Path
import json

from load.bigquery import SQLBigquery


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--params", type=json.loads)
    parser.add_argument("--return_results", "-r", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()

    query_file = args.query
    params = args.params
    return_results = args.return_results

    top_directory = list(Path(__file__).parents)[-2].name
    query_directory = os.path.join(top_directory, "queries")
    sql = SQLBigquery(query_directory=query_directory)

    res = sql.execute_query_from_file(
        query_file, return_results=return_results, **params
    )
    if return_results:
        print(res)


if __name__ == "__main__":
    main()
