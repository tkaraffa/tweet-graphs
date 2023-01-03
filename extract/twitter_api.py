import os
import json
from datetime import datetime

from util.base_api import APIBase
from util.api_exceptions import ValidationException
from extract.twitter_enums import (
    TweetMediaFields,
    TweetPlaceFields,
    TweetPollFields,
    TweetTweetFields,
    TweetUserFields,
    TwitterAPIDefaults,
    TwitterEndpoints,
    TwitterURLs,
    TweetExpansions,
)


class TwitterAPI(APIBase):
    def __init__(
        self,
        query: str,
        date: str,
        bearer_token: str = None,
        api_key: str = None,
        api_key_secret: str = None,
        access_token: str = None,
        access_token_secret: str = None,
        max_results: int = None,
    ) -> None:
        super().__init__()
        self.query = query
        self.date = date

        self.max_results = (
            max_results
            if max_results is not None
            else TwitterAPIDefaults.MAX_RESULTS.value
        )
        self.validation_func = self.twitter_api_validation
        self.bearer_token = os.getenv("BEARER_TOKEN")
        self.api_key = os.getenv("API_KEY")
        self.api_key_secret = os.getenv("API_KEY_SECRET")
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

        self.host = TwitterURLs.HOST.value
        self.meta = TwitterAPIDefaults.META.value
        self.data = TwitterAPIDefaults.DATA.value
        self.next_token = TwitterAPIDefaults.NEXT_TOKEN.value

        self.results = list()
        self.filename = f"{self.query}_{self.date}{self.jsonl_file_format}"

    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
            "Grant_Type": "client_credentials",
        }

    @property
    def endpoints(self) -> dict:
        return {
            endpoint.name.lower(): endpoint.value.lower()
            for endpoint in TwitterEndpoints
        }

    @property
    def query_dict(self) -> dict:
        expansions = ",".join([i.value for i in TweetExpansions])
        media_fields = ",".join([i.value for i in TweetMediaFields])
        place_fields = ",".join([i.value for i in TweetPlaceFields])
        poll_fields = ",".join([i.value for i in TweetPollFields])
        tweet_fields = ",".join([i.value for i in TweetTweetFields])
        user_fields = ",".join([i.value for i in TweetUserFields])
        query_dict = {
            "query": self.query,
            "expansions": expansions,
            "media.fields": media_fields,
            "place.fields": place_fields,
            "poll.fields": poll_fields,
            "tweet.fields": tweet_fields,
            "user.fields": user_fields,
            "max_results": self.max_results,
            "start_time": self.add_start_of_day_time(self.date),
            "end_time": self.add_end_of_day_time(self.date),
        }
        return query_dict

    def twitter_api_validation(self, response: str):
        """Check that responses are good"""
        self.data in json.loads(response).keys()

    def perform_search(
        self, endpoint: str = "search_recent", next_token=None
    ) -> dict:
        if next_token is not None:
            self.query_dict["next_token"] = next_token
        search_request = self.create_request(
            host=self.host,
            endpoint=self.endpoints.get(endpoint),
            scheme=self.scheme,
            query=self.query_dict,
            # params=self.parameters,
            headers=self.headers,
            safe=":",
        )
        data = self.pull_request_data(search_request)
        return json.loads(data)

    def paginate_tweets(self, n_pages=5) -> None:
        page_count = 1

        # always check the first page at least, and keep even if 0 results
        first_result = self.perform_search()
        self.results.append(first_result)
        next_token = first_result.get(self.meta).get(self.next_token)

        # only get extra pages if there is another page
        # and if max pages not exceeded
        while next_token is not None and page_count < n_pages:
            page_count += 1

            page_results = self.perform_search(next_token=next_token)
            self.results.append(page_results)
            next_token = page_results.get(self.meta).get(self.next_token)
