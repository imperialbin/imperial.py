import re
from datetime import datetime
from json import JSONDecodeError
from typing import Optional

# this is required so pycharm recognized the type
# (there's no good way to do this unfortunately)
from requests import Response

from ..exceptions import ImperialError

snake_regex = re.compile(r"(?<!^)(?<![A-Z])(?=[A-Z])")

__all__ = (
    "ensure_json",
    "to_snake_case",
    "to_camel_case",
    "parse_dates",
    "get_date_difference"
)


def ensure_json(response: Response) -> dict:
    """ ensures response from API will be a valid python dictionary """
    try:
        return response.json()
    except JSONDecodeError:
        raise ImperialError()


def to_snake_case(json: dict) -> dict:
    """ replaces camelCased keys with snake_cased keys """
    json = {(key if key.islower() else snake_regex.sub("_", key).lower()): value for key, value in json.items()}
    # note: in python 3.8+ this can be done with list comprehension with the := operator
    for key, value in json.items():
        if isinstance(value, dict):
            json[key] = to_snake_case(value)
    return json


def to_camel_case(json: dict) -> dict:
    """ replaces snake_cased keys with camelCased keys """
    # please don't make fun of my minified-looking comps
    json = {
        ("".join((word.capitalize() if i != 0 else word.lower()) for i, word in enumerate(key.split("_")))): value
        for key, value in json.items()
    }
    for key, value in json.items():
        if isinstance(value, dict):
            json[key] = to_camel_case(value)
    return json


def parse_dates(json: dict) -> dict:
    """ replaces unix timestamps with python datetime objects """
    # this just creates a more specific pointer
    document = json.get("document")
    if document and "creation_date" in document and "expiration_date" in document:
        document["creation_date"] = datetime.fromtimestamp(document["creation_date"] / 1000)
        document["expiration_date"] = datetime.fromtimestamp(document["expiration_date"] / 1000)
    return json


def get_date_difference(now: datetime, later: datetime) -> Optional[int]:
    """ :returns: the number of days between two datetime objects (or None if there are 0 days between) """
    days = (later - now).days
    return days if days > 0 else None
