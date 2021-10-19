import os
import json
from util.base_api import APIBase
from twitter_api.twitter_enums import TwitterEndpoints, TwitterURLs

from dotenv import load_dotenv

load_dotenv()


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

        self.validation_function = self.twitter_api_validation
        self.bearer_token = bearer_token or os.getenv("BEARER_TOKEN")
        self.api_key = api_key or os.getenv("API_KEY")
        self.api_key_secret = api_key_secret or os.getenv("API_KEY_SECRET")
        self.access_token = access_token or os.getenv("ACCESS_TOKEN")
        self.access_token_secret = access_token_secret or os.getenv(
            "ACCESS_TOKEN_SECRET"
        )

        self.host = TwitterURLs.HOST.value

        self.headers = self._create_headers()
        self.endpoints = self._create_endpoints()
        self.validation_func = self.twitter_api_validation()

    def _create_headers(self):
        return {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
            "Grant_Type": "client_credentials",
        }

    def _create_payload(self):
        return {}

    def _create_endpoints(self):
        return {
            endpoint.name.lower(): endpoint.value.lower()
            for endpoint in TwitterEndpoints
        }

    def twitter_api_validation(self):
        """Check that reposnses are good"""
        pass

    def perform_search(self, query):
        search_request = self.create_request(
            host=self.host,
            endpoint=self.endpoints.get("search"),
            scheme=self.scheme,
            query={
                "query": query,
                "expansions": "author_id",
                "tweet.fields": "entities",
            },
            headers=self.headers,
        )
        data = self._send_request(search_request)
        data = self.pull_request_data(search_request)
        return json.loads(data)
