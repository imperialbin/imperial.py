import re
from datetime import datetime

# this is required so pycharm recognized the type
# (there's no good way to do this unfortunately)
from requests import Response

from .checks import is_valid
from ..exceptions import ImperialError

snake_regex = re.compile(r"(?<!^)(?<![A-Z])(?=[A-Z])")


def ensure_json(response: Response):
    if response.text.lower().startswith("<!doctype html"):
        raise ImperialError("Uncaught Exception. Report Here: https://github.com/imperialbin/imperial-py")

    json = response.json()
    if json.get("success", False):
        return json
    elif json.get("message"):
        raise ImperialError(json["message"], status=response.status_code)
    else:
        raise ImperialError("Uncaught Exception. Report Here: https://github.com/imperialbin/imperial-py")


def to_snake_case(json: dict):
    json = {(key if key.islower() else snake_regex.sub("_", key).lower()): value for key, value in json.items()}
    # note: in python 3.8+ this can be done with list comprehension with the := operator
    for key, value in json.items():
        if isinstance(value, dict):
            json[key] = to_snake_case(value)
    return json


def to_camel_case(json: dict):
    # please don't make fun of my minified-looking comps
    json = {("".join((word.capitalize() if num != 0 else word.lower()) for num, word in enumerate(key.split("_")))): value
            for key, value in json.items()}
    for key, value in json.items():
        if isinstance(value, dict):
            json[key] = to_camel_case(value)
    return json


def parse_dates(json: dict):
    # this just creates a more specific pointer
    document = json.get("document")
    # this super weird syntax just checks if both those keys exist in the document
    if document and {"creation_date", "expiration_date"} <= set(document):
        document["creation_date"] = datetime.fromtimestamp(document["creation_date"] / 1000)
        document["expiration_date"] = datetime.fromtimestamp(document["expiration_date"] / 1000)
    return json


def parse_response(response: Response):
    # probably not good that i just nest three funcs here :shrug:
    return parse_dates(to_snake_case(ensure_json(response)))


def parse_request(method: str, api_token: str, **kwargs):
    return {
        # I don't think you're supposed to pass bare mutable types into requests
        # ex. passing json={} could cause issues
        # if it wasn't this way, I could remove the ternary expressions, which would be optimal.
        "headers": {"authorization": api_token} if api_token else None,
        "params": {"password": kwargs.pop("password")} if ("password" in kwargs and method == "GET") else None,
        "json": to_camel_case({key: value for key, value in kwargs.items() if is_valid(key, value)}) if kwargs else None
    }