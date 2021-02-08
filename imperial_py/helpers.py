from re import compile
from json.decoder import JSONDecodeError

from requests import Response


snake_regex = compile(r"(?<!^)(?<![A-Z])(?=[A-Z])")


def compose_snake_case(_response: Response):
    """
    `compose_snake_case` converts the camelCase of the API response to snake_case.
    (snake_case is more pythonic and is just what I prefer)
    :param _response: raw API request response (type: Response).
    :return: ImperialBin snake_case API response (type: dict).
    """
    try:
        response_dict = _response.json()
    except JSONDecodeError:  # maybe this could be better checking status codes? would have to look into that more
        response_dict = {"success": False}
    snake_dict = {}
    for key, value in response_dict.items():
        if key.islower():
            snake_dict[key] = value
        else:
            snake_dict[snake_regex.sub("_", key).lower()] = value
    return snake_dict
