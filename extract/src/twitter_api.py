from typing import Union
import os
import json
from dataclasses import dataclass, field

from util.base_api import APIBase
from util.file_formats import JSONLFormatter, Formatter
from util.enums_utils import join_enums, dictify_enums
from util.gcp_utils import GCPUtil
import src.twitter_enums as TwitterFields
from src.twitter_enums import *


class TwitterAPIDefaults(Enum):
    META = "meta"
    DATA = "data"
    NEXT_TOKEN = "next_token"


class TwitterURLs(Enum):
    HOST = "api.twitter.com/2"


class ValidationException(Exception):
    """Something went wrong"""


@dataclass(kw_only=True)
class TwitterAPI(APIBase):
    query: str
    date: str
    cloud_util: Union[GCPUtil]
    max_results: int = field(default=100)
    file_formatter: Formatter = field(default=JSONLFormatter(), init=False)

    bearer_token: str = os.getenv("BEARER_TOKEN")
    api_key: str = os.getenv("API_KEY")
    api_key_secret: str = os.getenv("API_KEY_SECRET")
    access_token: str = os.getenv("ACCESS_TOKEN")
    access_token_secret: str = os.getenv("ACCESS_TOKEN_SECRET")
    client_id: str = os.getenv("CLIENT_ID")
    client_secret: str = os.getenv("CLIENT_SECRET")

    results: list = field(default_factory=list, init=False)

    @property
    def filename(self) -> str:
        name = f"{self.query}_{self.date}{self.file_formatter.file_format}"
        self.file_formatter.check_file(name)
        return name

    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
            "grant_type": "client_credentials",
            # "User-Agent": "tweet-graphs",
        }

    @property
    def endpoints(self) -> dict:
        return dictify_enums(TwitterEndpoints)

    @property
    def query_dict(self) -> dict:
        return {
            "query": self.query,
            "expansions": join_enums(TweetExpansions),
            "media.fields": join_enums(TweetMediaFields),
            "place.fields": join_enums(TweetPlaceFields),
            "poll.fields": join_enums(TweetPollFields),
            "tweet.fields": join_enums(TweetTweetFields),
            "user.fields": join_enums(TweetUserFields),
            "max_results": self.max_results,
            "start_time": self.date_formatter.add_start_of_day_time(self.date),
            "end_time": self.date_formatter.add_end_of_day_time(self.date),
        }

    def validation_function(self, response: str):
        """Check that responses are good"""
        if not "meta" in json.loads(response).keys():
            raise ValidationException("`meta` key not present")

    def perform_search(
        self, endpoint: str = "search_recent", next_token=None
    ) -> dict:
        if next_token is not None:
            self.query_dict["next_token"] = next_token
        search_request = self.create_request(
            host=TwitterURLs.HOST.value,
            endpoint=self.endpoints.get(endpoint),
            query=self.query_dict,
            headers=self.headers,
            safe=":",
        )
        data = self.pull_request_data(search_request)
        return json.loads(data)

    def get_responses(self, n_pages=5) -> None:
        page_count = 1

        # always check the first page at least, and keep even if 0 results
        first_result = self.perform_search()
        self.results.append(first_result)
        next_token = first_result.get(TwitterAPIDefaults.META.value).get(
            TwitterAPIDefaults.NEXT_TOKEN.value
        )

        # only get extra pages if there is another page
        # and if max pages not exceeded
        while next_token is not None and page_count < n_pages:
            page_count += 1

            page_results = self.perform_search(next_token=next_token)
            self.results.append(page_results)
            next_token = page_results.get(TwitterAPIDefaults.META.value).get(
                TwitterAPIDefaults.NEXT_TOKEN.value
            )
