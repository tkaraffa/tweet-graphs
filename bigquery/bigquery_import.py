from sqlalchemy import create_engine

bq = create_engine(
    "bigquery://", credentials_path="serviceaccount.json"
)
with open("bigquery_load/sql/load_raw_tweets.sql") as f:
    query = f.read()
bq.execute(query)