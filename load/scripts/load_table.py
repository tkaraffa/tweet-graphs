"""
Load data from a source to a table,
using a user-provided SQL file.
"""

import argparse

from load.get_query import get_query

print(get_query("insert_into_tweets"))
