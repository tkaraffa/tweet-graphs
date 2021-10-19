import argparse

from twitter_api.twitter_api import TwitterAPI


def get_args():
    parser = argparse.ArgumentParser("Search for Tweets based on a term.")
    parser.add_argument("query", type=str)

    return parser.parse_args()


def search():
    args = get_args()
    query = args.query

    t = TwitterAPI()

    results = t.perform_search(query)
    import json

    print(results.get("data"))


if __name__ == "__main__":
    search()
