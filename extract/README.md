# twitter_api

Module to download Tweets and upload to a Google Cloud Bucket.

Depends on `serviceaccount.json` in the root directory to provide Google Service Account crendentials. This file is created by Terraform, specifically `terraform apply` run from the `infrastructure` directory.

## Usage

The recommended usage is through `docker-compose run twitter <query> [OPTIONS]`.

```
usage: search.py [-h] query --bucket BUCKET [OPTIONS]
                 

Search for Tweets based on a term.

positional arguments:
  query              The search term.

optional arguments:
  -h, --help         show this help message and exit
  --n_pages N_PAGES  The number of pages of Tweets to pull.
  --outfile OUTFILE  The name of the file in which to save results.
  --bucket BUCKET    The GCS Bucket in which to upload resutls.
```
