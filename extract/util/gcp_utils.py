from dataclasses import dataclass, field

from google.cloud.storage import Client


@dataclass(init=False, frozen=True)
class GCPUtil:
    gcs_client: Client = Client()

    def upload_file_to_bucket(self, filename, bucket, **kwargs):
        bucket = self.gcs_client.get_bucket(bucket)
        blob = bucket.blob(filename)
        blob.upload_from_filename(filename, **kwargs)
        print(f"Uploaded {filename} to {bucket}")
