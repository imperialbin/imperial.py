from abc import ABC

import httpx

from imperial.lib.clients import BaseClient
from imperial.lib.common import API_V1_DOCUMENT


class Client(BaseClient, ABC):

    def __init__(self):
        BaseClient.__init__(self)
        self._client: httpx.Client = httpx.Client()

    def _request(self, *, method, url, data=None):
        resp = self._client.request(
            method=method,
            url=url,
            data=data,
            headers={"User-Agent": "imperial-py; (+https://github.com/imperialbin/imperial-py)"}
        )
        return self._response(resp)

    def create_document(self, settings):
        return self._request(method="POST", url=API_V1_DOCUMENT, data=settings)

    def get_document(self, id: str):
        return self._request(method="GET", url=f"{API_V1_DOCUMENT}/{id}")

    def patch_document(self, settings):
        self._request(method="PATCH", url=API_V1_DOCUMENT, data=settings)

    def delete_document(self, id: str):
        self._request(method="DELETE", url=f"{API_V1_DOCUMENT}/{id}")

if __name__ == "__main__":
    imp = Client()
    print(imp.create_document({"content": "yeah"}))
