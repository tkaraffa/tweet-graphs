import os
import json
from util.base_api import APIBase
from twitter_api.twitter_enums import (
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
        bearer_token=None,
        api_key=None,
        api_key_secret=None,
        access_token=None,
        access_token_secret=None,
    ) -> None:
        super().__init__()

        self.max_results = TwitterAPIDefaults.MAX_RESULTS.value
        self.validation_function = self.twitter_api_validation
        self.bearer_token = bearer_token or os.getenv("BEARER_TOKEN")
        self.api_key = api_key or os.getenv("API_KEY")
        self.api_key_secret = api_key_secret or os.getenv("API_KEY_SECRET")
        self.access_token = access_token or os.getenv("ACCESS_TOKEN")
        self.access_token_secret = access_token_secret or os.getenv(
            "ACCESS_TOKEN_SECRET"
        )
        self.host = TwitterURLs.HOST.value

        self.endpoints = self._create_endpoints()
        self.validation_func = self.twitter_api_validation()

        self.meta = TwitterAPIDefaults.META.value
        self.data = TwitterAPIDefaults.DATA.value
        self.next_token = TwitterAPIDefaults.NEXT_TOKEN.value

    @staticmethod
    def _create_headers(bearer_token):
        return {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json",
            "Grant_Type": "client_credentials",
        }

    def _create_payload(self):
        return {}

    @staticmethod
    def _create_endpoints():
        return {
            endpoint.name.lower(): endpoint.value.lower()
            for endpoint in TwitterEndpoints
        }

    def twitter_api_validation(self):
        """Check that reposnses are good"""
        pass

    @staticmethod
    def _create_query(
        query, max_results=100, next_token=None, include_retweets=False
    ):
        if include_retweets is False:
            query += " -is:retweet"
        expansions = ",".join([i.value for i in TweetExpansions])
        media_fields = ",".join([i.value for i in TweetMediaFields])
        place_fields = ",".join([i.value for i in TweetPlaceFields])
        poll_fields = ",".join([i.value for i in TweetPollFields])
        tweet_fields = ",".join([i.value for i in TweetTweetFields])
        user_fields = ",".join([i.value for i in TweetUserFields])
        query_dict = {
            "query": query,
            "expansions": expansions,
            "media.fields": media_fields,
            "place.fields": place_fields,
            "poll.fields": poll_fields,
            "tweet.fields": tweet_fields,
            "user.fields": user_fields,
            "max_results": max_results,
        }
        if next_token is not None:
            query_dict["next_token"] = next_token
        return query_dict

    def perform_search(self, query, next_token=None):
        search_request = self.create_request(
            host=self.host,
            endpoint=self.endpoints.get("search"),
            scheme=self.scheme,
            query=self._create_query(
                query=query,
                max_results=self.max_results,
                next_token=next_token,
            ),
            headers=self._create_headers(self.bearer_token),
        )
        data = self._send_request(search_request)
        data = self.pull_request_data(search_request)
        return json.loads(data)

    def paginate_tweets(self, query, n_pages=5):
        tweets = list()
        next_token = None
        for _ in range(n_pages):
            page_results = self.perform_search(query, next_token=next_token)
            tweets.extend(page_results.get(self.data))
            next_token = page_results.get(self.meta).get(self.next_token)
        return tweets
