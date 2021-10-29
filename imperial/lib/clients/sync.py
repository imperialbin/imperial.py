import httpx

from . import BaseClient


class Client(BaseClient):

    def __init__(self):
        super().__init__()
        self._client = httpx.Client()

    def _request(self, *, method: str, url: str, data: dict):

        resp = self._client.request(
            method=method,
            url=url,
            data=data,
            headers={
                "User-Agent": "imperial-py; (+https://github.com/imperialbin/imperial-py)"
            },

        )

        json = ensure_json(resp)
        json = to_snake_case(json)
        success = json.get("success", False)
        message = json.get("message", None)

        if resp.status_code == 401:
            raise InvalidAuthorization()
        if resp.status_code == 404:
            raise DocumentNotFound()
        if not success:
            raise ImperialError(message)
