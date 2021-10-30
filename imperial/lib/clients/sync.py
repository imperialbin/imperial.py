from abc import ABC
from typing import List, Optional

import httpx

from imperial.lib.clients import BaseClient
from imperial.lib.common import API_V1_DOCUMENT


class Client(BaseClient, ABC):

    def __init__(self):
        BaseClient.__init__(self)
        self._client: httpx.Client = httpx.Client()

    def _request(self, *, method, url, payload=None):
        payload = self._payload(payload) if payload else {}
        resp = self._client.request(
            method=method,
            url=url,
            json=payload,
            headers={"User-Agent": "imperial-py; (+https://github.com/imperialbin/imperial-py)"}
        )
        return self._response(resp)

    def create_document(self, content: str, *,
                        language: Optional[str] = None,
                        expiration: int = 5,
                        short_urls: bool = False,
                        long_urls: bool = False,
                        image_embed: bool = False,
                        instant_delete: bool = False,
                        encrypted: bool = False,
                        password: Optional[str] = None,
                        public: bool = False,
                        create_gist: bool = False,
                        editors: List[str] = None):
        return self._request(method="POST", url=API_V1_DOCUMENT, payload=locals())

    def get_document(self, id: str):
        return self._request(method="GET", url=f"{API_V1_DOCUMENT}/{id}")

    def patch_document(self, id: str, content: str, *,
                       language: Optional[str] = None,
                       expiration: int = 5,
                       short_urls: bool = False,
                       long_urls: bool = False,
                       image_embed: bool = False,
                       instant_delete: bool = False,
                       public: bool = False,
                       editors: List[str] = None):
        self._request(method="PATCH", url=API_V1_DOCUMENT, payload=locals())

    def delete_document(self, id: str):
        self._request(method="DELETE", url=f"{API_V1_DOCUMENT}/{id}")


if __name__ == "__main__":
    imp = Client()
    print(imp.create_document("yeah", short_urls=True))
