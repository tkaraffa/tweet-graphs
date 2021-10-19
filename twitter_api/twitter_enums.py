from enum import Enum


class TwitterURLs(Enum):
    HOST = "api.twitter.com/2"


class TwitterEndpoints(Enum):
    SEARCH = "tweets/search/recent"
