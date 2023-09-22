from typing import Any
import argparse

from util.base_api import DateFormatter
from src.apis import get_api_class
from util.gcp_utils import GCPUtil


def get_args():
    date_formatter = DateFormatter()

    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Search for something in an API based on a term.",
    )
    parser.add_argument(
        "api",
        type=str,
        help="The API to use.",
    )
    parser.add_argument(
        "query",
        type=str,
        help="The search term.",
    )
    parser.add_argument(
        "--date",
        type=date_formatter.check_iso_8601,
        help="ISO 8601 formatted date.",
        default=date_formatter.get_yesterday(),
        required=False,
    )
    parser.add_argument(
        "--n_pages",
        type=int,
        help="The number of pages of Tweets to pull.",
        required=False,
        default=5,
    )
    parser.add_argument(
        "--bucket",
        type=str,
        help="The GCS Bucket in which to upload resutls.",
        required=True,
    )
    return parser.parse_args()


def main():
    args = get_args()
    api_class = get_api_class(args.api)
    api = api_class(query=args.query, date=args.date, cloud_util=GCPUtil())
    api.get_responses()
    # api.paginate_tweets(n_pages=args.n_pages)
    api.write_and_upload(api.results, api.filename, args.bucket)


if __name__ == "__main__":
    main()
