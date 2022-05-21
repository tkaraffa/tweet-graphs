from google.cloud import bigquery

client = bigquery.Client()
# table_id = "tweet-graphs-330003.tweets.raw_tweets"
# job_config = bigquery.LoadJobConfig(
#     source_format=bigquery.SourceFormat.CSV,
# )

# uri = "gs://tweets-raw/trump_20211024:232859.jsonl"

# load_job = client.load_table_from_uri(
#     uri, table_id, location="us-central1", job_config=job_config
# )
# load_job.result()

# destination_table = client.get_table(table_id)
# print(destination_table.num_rows)

dataset_id = "tweets"
project = "tweet-graphs-330003"
dataset_ref = bigquery.DatasetReference(project=project, dataset_id=dataset_id)
temp_table_id = "temp_raw_tweets"
table_id = "raw_tweets"

schema = [
    bigquery.SchemaField("source", "STRING"),
    bigquery.SchemaField("filename", "STRING"),
    bigquery.SchemaField("json_text", "STRING"),
]
temp_table = bigquery.Table(dataset_ref.table(temp_table_id), schema=schema)
table = bigquery.Table(dataset_ref.table(table_id), schema=schema)
external_config = bigquery.ExternalConfig("CSV")
external_config.source_uris = ["gs://tweets-raw/trump_20211024:232859.jsonl"]
temp_table.external_data_configuration = external_config
client.delete_table(temp_table, not_found_ok=True)
client.create_table(temp_table)

query = """
insert into `{project}.{dataset_id}.{table_id}`
(
    select
        'test' as source,
        'test' as filename,
        'hi' as json_text
    from
        `{project}.{dataset_id}.{temp_table_id}`
)
""".format(
    dataset_id=dataset_id,
    table_id=table_id,
    temp_table_id=temp_table_id,
    project=project,
)

query_job = client.query(query)
job = list(query_job)
client.delete(project, dataset_id, temp_table_id)
