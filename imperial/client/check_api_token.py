from .request import request
from ..checks import ensure_api_token
from ..utils import https


def check_api_token(api_token: str) -> dict:
    """
    Validate API token from https://imperialb.in
    GET https://imperialb.in/api/checkApiToken/:apiToken
    :param api_token: the API token linked with your imperial account
    """
    ensure_api_token(api_token)

    return request(
        method="GET",
        url=https.imperialbin / "api" / "checkApiToken" / api_token
    )
