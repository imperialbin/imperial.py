from abc import ABC
from types import Union

import httpx

from . import BaseClient
from ..document import Settings


class Client(BaseClient, ABC):

    def __init__(self):
        BaseClient.__init__(self)
        self._client = httpx.Client()

    def _request(self, *, method: str, url: str, data: dict):
        resp = self._client.request(
            method=method,
            url=url,
            data=data,
            headers={"User-Agent": "imperial-py; (+https://github.com/imperialbin/imperial-py)"}
        )
        return self._response(resp)

    def create_document(self, settings: Union[dict, Settings]):
        pass