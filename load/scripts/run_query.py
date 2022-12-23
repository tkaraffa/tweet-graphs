"""
Load data from a source to a table,
using a user-provided SQL file.
"""

import argparse
import json
import sqlalchemy as sa
from util.gcp_utils import get_credentials
from load.sql_base import SQLBase


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--params", type=json.loads)
    return parser.parse_args()


def main():
    args = parse_args()
    sql = SQLBase()

    query_file = args.query
    params = args.params

    query = sql.get_query(query_file, **params)
    sql.engine.execute(query)


if __name__ == "__main__":
    main()
