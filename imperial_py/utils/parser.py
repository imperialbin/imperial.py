import re
from datetime import datetime
# this is required so pycharm recognized the type
# (there's no good way to do this unfortunately)
from json import JSONDecodeError
from typing import Optional

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
    # success: False can get through, but not invalid json
    try:
        return response.json()
    except JSONDecodeError as exc:
        raise ImperialError(str(exc))


def to_snake_case(json: dict) -> dict:
    json = {(key if key.islower() else snake_regex.sub("_", key).lower()): value for key, value in json.items()}
    # note: in python 3.8+ this can be done with list comprehension with the := operator
    for key, value in json.items():
        if isinstance(value, dict):
            json[key] = to_snake_case(value)
    return json


def to_camel_case(json: dict) -> dict:
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
    # this just creates a more specific pointer
    document = json.get("document")
    # this super weird syntax just checks if both those keys exist in the document
    if document and "creation_date" in document and "expiration_date" in document:
        document["creation_date"] = datetime.fromtimestamp(document["creation_date"] / 1000)
        document["expiration_date"] = datetime.fromtimestamp(document["expiration_date"] / 1000)
    return json


def get_date_difference(now, later) -> Optional[int]:
    # assumes now and later are datetime objects
    days = (later - now).days
    return days if days > 0 else None
