import argparse
import json

from twitter_api.twitter_api import TwitterAPI


def get_args():
    parser = argparse.ArgumentParser("Search for Tweets based on a term.")
    parser.add_argument("query", type=str)

    return parser.parse_args()


def search():
    args = get_args()
    query = args.query

    t = TwitterAPI()

    tweets = list()

    results = t.perform_search(query)
    tweets.extend(results.get("data"))
    for _ in range(5):
        next_token = results.get("meta").get("next_token")
        results = t.perform_search(query, next_token=next_token)
        tweets.extend(results.get("data"))
    with open("results.json", "w+") as f:
        json.dump(tweets, f, sort_keys=True, indent=2)


if __name__ == "__main__":
    search()
