import re
from datetime import datetime

snake_regex = re.compile(r"(?<!^)(?<![A-Z])(?=[A-Z])")
defaults = {"longerUrls": False,
            "instantDelete": False,
            "imageEmbed": False,
            "expiration": 5,
            "encrypted": False,
            "password": None}


def parse_kwargs(method, kwargs):
    json = {}
    params = {}
    # parse kwargs into json / params
    for key, value in kwargs.items():
        if key not in defaults:
            # if there is not default value we assume it's mandatory,
            # and always pass it into the json body.
            json[key] = value
        elif value != defaults[key]:
            if key != "password":
                json[key] = value
            elif method != "GET":
                json["password"] = value
            else:  # elif method == "GET"
                # as of right now, I believe this is the only case where we pass params
                json["params"]["password"] = value
    return {"json": json, "params": params}


def ensure_json(response):
    if response.status_code <= 404:
        return response.json()
    return {"success": False,
            "message": "Uncaught Exception. Report Here: https://github.com/imperialbin/imperial-py"}


def json_modifications(json):
    json = {(key if key.islower() else snake_regex.sub("_", key).lower()): value for key, value in
            json.items()}
    if "expiration" in json:
        json["expiration"] = datetime.strptime(json["expiration"], "%Y-%m-%dT%H:%M:%S.%fZ")
    return json


def remove_self(data):
    """
    removes keys from dict w/o errors if key isn't found (dict comp.)
    :type data: dict
    # :type to_remove: list[str]
    """
    return {key: value for key, value in data.items() if key != "self"}
