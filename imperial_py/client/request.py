import requests

from ..exceptions import InvalidAuthorization, DocumentNotFound, ImperialError
from ..utils import ensure_json, to_snake_case, parse_dates
from ..client.body import Body


def request(*, method: str, url: str, api_token: str = None, **kwargs) -> dict:
    # url is a hostname obj with a repr of the url
    # not sure where, but somewhere it gets converted to string,
    # but this could possibly cause issues on other versions

    # api_token gets mixed in with **kwargs inside Body constructor
    body = Body(method=method, api_token=api_token, **kwargs)

    resp = requests.request(
        method=method,
        url=url,
        headers=body.headers,
        params=body.params,
        json=body.json
    )

    json = ensure_json(resp)
    json = to_snake_case(json)
    success = json.get("success", False)
    message = json.get("message", None)

    if resp.status_code == 401:
        raise InvalidAuthorization(message, api_token=api_token)
    if resp.status_code == 404:
        raise DocumentNotFound(kwargs.get("document_id", None))
    if not success:
        raise ImperialError(message)

    json = parse_dates(json)
    return json
