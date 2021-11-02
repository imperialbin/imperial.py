from abc import ABC
from typing import List, Optional

import httpx

from imperial.common import MISSING
from imperial.lib.base.client import BaseClient
from imperial.lib.sync.document_manager import DocumentManager


class Client(BaseClient, ABC):
    __slots__ = "_client", "_document"

    def __init__(self, token: Optional[str] = MISSING):  # type: ignore[assignment]
        super().__init__(token)
        self._client: httpx.Client = httpx.Client()
        self._document = DocumentManager(self)

    @property
    def document(self):
        return self._document

    def _request(self, *, method, url, payload=None):
        payload = self._payload(payload) if payload else {}
        resp = self._client.request(
            method=method,
            url=url,
            json=payload,
            headers=self.headers
        )
        return self._response(resp)

    def _create_document(self, content: str, *,
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
                         editors: List[str] = None) -> dict:
        return self._request(method="POST", url=self.API_V1_DOCUMENT, payload=locals())

    def _get_document(self, id: str) -> dict:
        return self._request(method="GET", url=f"{self.API_V1_DOCUMENT}/{id}")

    def _patch_document(self, id: str, content: str, *,
                        language: Optional[str] = None,
                        expiration: int = 5,
                        image_embed: bool = False,
                        instant_delete: bool = False,
                        public: bool = False,
                        editors: List[str] = None) -> dict:
        return self._request(method="PATCH", url=self.API_V1_DOCUMENT, payload=locals())

    def _delete_document(self, id: str) -> dict:
        return self._request(method="DELETE", url=f"{self.API_V1_DOCUMENT}/{id}")
