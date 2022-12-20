import os

from google.cloud.storage import Client


def upload_file_to_bucket(filename, bucket, **kwargs):
    client = Client()
    bucket = client.get_bucket(bucket)
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename, **kwargs)


def get_credentials():
    credentials = dict(
        credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    return credentials
    # project = os.getenv("GOOGLE_CLOUD_PROJECT")
    # dataset = os.getenv("BIGQUERY_DATASET")
    # return f"bigquery://{project}/{dataset}"
