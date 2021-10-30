from json import JSONDecodeError
from typing import Callable

import httpx

from imperial.lib.exceptions import ImperialError

HOSTNAME = "https://staging-balls.impb.in"
API_HOSTNAME = "https://staging-balls-api.impb.in"

API_V1 = f"{API_HOSTNAME}/v1"
API_V1_DOCUMENT = f"{API_V1}/document"

MISSING = object()


# reference: https://github.com/Hexiro/autorequests/blob/main/autorequests/utilities/case.py

def camel_to_snake(text: str) -> str:
    return "".join("_" + t.lower() if t.isupper() else t for t in text).lstrip("_")


def camel_dict_to_snake(data: dict) -> dict:
    return _format_dict(camel_to_snake, data)


def snake_to_camel(text: str) -> str:
    return "".join(t.lower() if i == 0 else t.capitalize() for i, t in enumerate(text.split("_")))


def snake_dict_to_camel(data: dict) -> dict:
    return _format_dict(snake_to_camel, data)


def _format_dict(func: Callable, data: dict):
    updated = {}
    for k, v in data.items():
        if isinstance(v, dict):
            v = _format_dict(func, v)
        updated[func(k)] = v
    return updated


def ensure_json(response: httpx.Response) -> dict:
    """
    ensures response from API will be a valid python dictionary
    """
    try:
        return response.json()
    except JSONDecodeError:
        raise ImperialError("failed to parse JSON")
