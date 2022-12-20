import argparse
from datetime import datetime

from twitter_api.twitter_api import TwitterAPI


def format_now():
    return datetime.strftime(datetime.now(), "%Y%m%d")


def check_json(file: str):
    if not file.endswith(".json"):
        print("Please use .json file extensions.")
        raise TypeError
    return file


def get_args():
    parser = argparse.ArgumentParser(
        prog="search.py",
        description="Search for Tweets based on a term.",
    )
    parser.add_argument(
        "query",
        type=str,
        help="The search term.",
    )
    parser.add_argument(
        "--n_pages",
        type=int,
        help="The number of pages of Tweets to pull.",
        required=False,
        default=5,
    )
    parser.add_argument(
        "--outfile",
        type=check_json,
        help="The name of the file in which to save results.",
        required=False,
    )
    parser.add_argument(
        "--bucket",
        type=str,
        help="The GCS Bucket in which to upload resutls.",
        required=True,
    )
    return parser.parse_args()


def search():
    args = get_args()
    query = args.query
    n_pages = args.n_pages
    outfile = args.outfile
    bucket = args.bucket

    t = TwitterAPI()
    now = format_now()
    results = t.paginate_tweets(query, n_pages=n_pages)
    filename = outfile or f"{query}_{now}.json"
    t.write_and_upload(results, filename, bucket)


if __name__ == "__main__":
    search()
