import argparse

from extract.twitter_api import TwitterAPI
from extract.util.base_api import DateFormatter


def get_args():
    date_formatter = DateFormatter()

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


def search():
    args = get_args()
    query = args.query
    date = args.date
    n_pages = args.n_pages
    bucket = args.bucket

    twitter = TwitterAPI(query=query, date=date)

    twitter.paginate_tweets(n_pages=n_pages)
    twitter.write_and_upload(twitter.results, twitter.filename, bucket)


if __name__ == "__main__":
    search()
