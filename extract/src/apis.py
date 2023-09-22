from typing import Type
from enum import Enum

from src.twitter_api import TwitterAPI
from util.base_api import APIBase


class APIs(Enum):
    TWITTER = TwitterAPI


def get_api_class(name: str) -> Type[APIBase]:
    match name.upper():
        case APIs.TWITTER.name:
            return APIs.TWITTER.value
        case _:
            raise ValueError(f"Invalid API: {name}")
