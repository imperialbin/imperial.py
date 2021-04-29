import requests

from ..utils.parser import parse_request, parse_response


def request(*, method: str, url: str, api_token: str = None, **kwargs):
    # url is a hostname obj with a repr of the url
    # not sure where, but somewhere it gets converted to string,
    # but this could possibly cause issues on other versions
    resp = requests.request(
        method=method,
        url=url,
        **parse_request(method, api_token, **kwargs)
    )
    return parse_response(resp)
