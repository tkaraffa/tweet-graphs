"""
Load data from a source to a table,
using a user-provided SQL file.
"""

import argparse
import sqlalchemy as sa
from load.get_query import get_query
from util.gcs_utils import get_credentials

query = get_query("insert_into_tweets")
print(query)
# conn = db.engine.execute(query)
credentials = get_credentials()
engine = sa.engine.create_engine("bigbquery://")
res = engine.execute(query)
print(str(res))
