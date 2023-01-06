from google.cloud.storage import Client


def upload_file_to_bucket(filename, bucket, **kwargs):
    client = Client()
    bucket = client.get_bucket(bucket)
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename, **kwargs)
