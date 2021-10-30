from json import JSONDecodeError

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
    return {camel_to_snake(k): v for k, v in data.items()}


def ensure_json(response: httpx.Response) -> dict:
    """
    ensures response from API will be a valid python dictionary
    """
    try:
        return response.json()
    except JSONDecodeError:
        raise ImperialError("failed to parse JSON")
