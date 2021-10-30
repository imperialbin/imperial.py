from abc import ABC
from typing import List, Optional

import httpx

from imperial.lib.clients import BaseClient
from imperial.lib.common import API_V1_DOCUMENT
from imperial.lib.common import MISSING
from imperial.lib.documents.io import Document


class Client(BaseClient, ABC):
    __slots__ = "_client",

    def __init__(self, token: Optional[str] = MISSING):  # type: ignore[assignment]
        super(Client, self).__init__(token)
        self._client: httpx.Client = httpx.Client()

    def create_document(self, content: str, *,
                        language: str = None,
                        expiration: int = 5,
                        short_urls: bool = False,
                        long_urls: bool = False,
                        image_embed: bool = False,
                        instant_delete: bool = False,
                        encrypted: bool = False,
                        password: str = None,
                        public: bool = False,
                        create_gist: bool = False,
                        editors: List[str] = None) -> "Document":
        resp = self._create_document(content=content, language=language, expiration=expiration, short_urls=short_urls,
                                     long_urls=long_urls, image_embed=image_embed, instant_delete=instant_delete,
                                     encrypted=encrypted, password=password, public=public, create_gist=create_gist,
                                     editors=editors)
        return Document(client=self, **resp["data"])

    def get_document(self, id: str) -> "Document":
        return Document(client=self, **self._get_document(id))

    def patch_document(self, id: str, content: str, *,
                       language: str = None,
                       expiration: int = 5,
                       image_embed: bool = False,
                       instant_delete: bool = False,
                       public: bool = False,
                       editors: List[str] = None) -> "Document":
        resp = self._patch_document(id, content, language=language, expiration=expiration, image_embed=image_embed,
                                    instant_delete=instant_delete, public=public, editors=editors)
        return Document(client=self, **resp)

    def delete_document(self, id: str) -> None:
        self._delete_document(id)

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
        return self._request(method="POST", url=API_V1_DOCUMENT, payload=locals())

    def _get_document(self, id: str) -> dict:
        return self._request(method="GET", url=f"{API_V1_DOCUMENT}/{id}")

    def _patch_document(self, id: str, content: str, *,
                        language: Optional[str] = None,
                        expiration: int = 5,
                        image_embed: bool = False,
                        instant_delete: bool = False,
                        public: bool = False,
                        editors: List[str] = None) -> dict:
        return self._request(method="PATCH", url=API_V1_DOCUMENT, payload=locals())

    def _delete_document(self, id: str) -> dict:
        return self._request(method="DELETE", url=f"{API_V1_DOCUMENT}/{id}")


if __name__ == "__main__":
    imp = Client()
    doc = imp.create_document("yeah", short_urls=True)
    print(f"{doc.language=}")
    doc.edit(language="python")
    print(doc)
    print(f"{doc.language=}")
