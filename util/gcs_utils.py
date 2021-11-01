from google.cloud.storage import Client as StorageClient
from google.cloud.bigquery import Client as BigQueryClient


def upload_file_to_bucket(filename, bucket, **kwargs):
    client = StorageClient()
    bucket = client.get_bucket(bucket)
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename, **kwargs)
