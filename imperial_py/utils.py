import re
from datetime import datetime
from json.decoder import JSONDecodeError

# for pycharm to count the docstring type as valid this needs to be imported still
# even though it's not explicitly used :shrug:
from requests import Response


snake_regex = re.compile(r"(?<!^)(?<![A-Z])(?=[A-Z])")


def compose_snake_case(response):
    """
    `compose_snake_case` converts the camelCase of the API response to snake_case.
    (snake_case is more pythonic and is just what I prefer)
    :param response: raw API request response (type: Response).
    :type response: Response
    :return: ImperialBin snake_case API response (type: dict).
    """
    try:
        response_dict = response.json()
    except JSONDecodeError:
        # invalid json
        # maybe this could be better checking status codes? would have to look into that more
        response_dict = {
            "success": False,
            "message": "Uncaught Exception. Report Here: https://github.com/imperialbin/imperial-py"
        }
    snake_dict = {}
    for key, value in response_dict.items():
        if key.islower():
            snake_dict[key] = value
        else:
            snake_dict[snake_regex.sub("_", key).lower()] = value
    return snake_dict


def format_datetime_expiry(response_dict):
    """
    changes isoformat formated key `expires_in` to datetime object.
    :param response_dict: dictionary to modify
    :type response_dict: dict
    :return: datetime object modified dictionary
    """
    # changed from `if "expires_in" in response_dict:`
    # expires_in was `None` due to a bug so now it's future proof :)
    if response_dict.get("expires_in"):
        response_dict["expires_in"] = datetime.strptime(response_dict["expires_in"], "%Y-%m-%dT%H:%M:%S.%fZ")
    return response_dict


def parse_document_id(document_id):
    """
    returns raw document_id or document id from end of full URL.
    :param document_id: ImperialBin Document ID
    :type document_id: str
    :return: parsed document_id (type: str).
    """
    if "/" in document_id:
        # url parsed
        # might change this to match a regex like imperial-node.
        # as of now, we assume they are passing a valid url
        return document_id.split("/")[-1]
    return document_id
