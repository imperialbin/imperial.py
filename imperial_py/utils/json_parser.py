import re
from datetime import datetime

from .param_checks import is_required, is_valid_data
from ..exceptions import ImperialError

snake_regex = re.compile(r"(?<!^)(?<![A-Z])(?=[A-Z])")


def parse_body(method, kwargs):
    json = {}
    params = {}
    # parse kwargs into json / params
    for key, value in kwargs.items():
        if is_required(key):
            # if there is not default value we assume it's mandatory,
            # and always pass it into the json body.
            # mandatory keys are pre-checked to be valid
            json[key] = value
        elif is_valid_data(key, value):
            pass
        elif key != "password":
            json[key] = value
        # from now on, `key` will always be `password`
        elif method != "GET":
            json[key] = value
        # as of right now, I believe this is the only case where we pass params
        else:
            params[key] = value
    return {"json": json, "params": params}


def ensure_json(response):
    if response.text.lower().startswith("<!doctype html"):
        raise ImperialError("Uncaught Exception. Report Here: https://github.com/imperialbin/imperial-py")

    json = response.json()
    if json.get("success", False):
        return json
    elif json.get("message"):
        raise ImperialError(json["message"], status=response.status_code)
    else:
        raise ImperialError("Uncaught Exception. Report Here: https://github.com/imperialbin/imperial-py")


def to_snake_case(json):
    json = {(key if key.islower() else snake_regex.sub("_", key).lower()): value for key, value in json.items()}
    # i would dict comp. this recursion, but I don't want to torture future maintainers (me lol)
    for key, value in json.items():
        if isinstance(value, dict):
            json[key] = to_snake_case(value)
    return json


def json_modifications(json):
    # convert to snake case
    json = to_snake_case(json)
    # this just creates a more specific pointer
    document = json.get("document")
    # convert to datetime obj
    # this super weird syntax just checks if both those keys exist in the document
    if document and {"creation_date", "expiration_date"} <= set(document):
        document["creation_date"] = datetime.fromtimestamp(document["creation_date"] / 1000)
        document["expiration_date"] = datetime.fromtimestamp(document["expiration_date"] / 1000)
    return json


def remove_self(data):
    """
    removes keys from dict w/o errors if key isn't found (dict comp.)
    :type data: dict
    """
    return {key: value for key, value in data.items() if key != "self"}
