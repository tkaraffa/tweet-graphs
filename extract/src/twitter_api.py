import os
import json
from dataclasses import dataclass, field

from extract.util.base_api import APIBase
from extract.util.file_formats import JSONLFormatter, Formatter
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


@dataclass(kw_only=True)
class TwitterAPI(APIBase):
    query: str
    date: str
    max_results: int = TwitterAPIDefaults.MAX_RESULTS.value
    file_formatter: Formatter = field(default=JSONLFormatter(), init=False)

    bearer_token: str = os.getenv("BEARER_TOKEN")
    api_key: str = os.getenv("API_KEY")
    api_key_secret: str = os.getenv("API_KEY_SECRET")
    access_token: str = os.getenv("ACCESS_TOKEN")
    access_token_secret: str = os.getenv("ACCESS_TOKEN_SECRET")

    results: list = field(default_factory=list, init=False)

    @property
    def filename(self) -> str:
        name = f"{self.query}_{self.date}{self.file_formatter.file_format}"
        return self.file_formatter.check_file(name)

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
            "start_time": self.date_formatter.add_start_of_day_time(self.date),
            "end_time": self.date_formatter.add_end_of_day_time(self.date),
        }
        return query_dict

    def validation_function(self, response: str):
        """Check that responses are good"""
        return TwitterAPIDefaults.META.value in json.loads(response).keys()

    @property
    def validation_exception(self):
        return Exception("nooo")

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

    def paginate_tweets(self, n_pages=5) -> None:
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
