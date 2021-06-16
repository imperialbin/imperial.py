import requests

from ..utils import ensure_json, to_snake_case, parse_dates
from ..client.body import Body


def request(*, method: str, url: str, api_token: str = None, **kwargs) -> dict:
    # url is a hostname obj with a repr of the url
    # not sure where, but somewhere it gets converted to string,
    # but this could possibly cause issues on other versions

    # api_token gets mixed in with **kwargs inside Body constructor
    parsed_body = Body(method=method, api_token=api_token, **kwargs)

    resp = requests.request(
        method=method,
        url=url,
        headers=parsed_body.headers,
        params=parsed_body.params,
        json=parsed_body.json
    )

    json = ensure_json(resp)
    json = to_snake_case(json)
    if not json["success"]:
        return json
    json = parse_dates(json)
    return json
