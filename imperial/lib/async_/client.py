from abc import ABC
from typing import List, Optional

import httpx

from imperial.lib.base.client import BaseClient


class AsyncClient(BaseClient, ABC):

    async def _request(self, *, method, url, payload=None):
        async with httpx.AsyncClient() as client:
            payload = self._payload(payload) if payload else {}
            resp = await client.request(
                method=method,
                url=url,
                json=payload,
                headers=self._headers
            )
            return self._response(resp)

    async def _create_document(self, content: str, *,  # type: ignore[override]
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
        return await self._request(method="POST", url=self.API_V1_DOCUMENT, payload=locals())

    async def _get_document(self, id: str):  # type: ignore[override]
        return await self._request(method="GET", url=f"{self.API_V1_DOCUMENT}/{id}")

    async def _patch_document(self, id: str, content: str, *,  # type: ignore[override]
                              language: str = None,
                              expiration: int = 5,
                              image_embed: bool = False,
                              instant_delete: bool = False,
                              public: bool = False,
                              editors: List[str] = None):
        await self._request(method="PATCH", url=self.API_V1_DOCUMENT, payload=locals())

    async def _delete_document(self, id: str):  # type: ignore[override]
        await self._request(method="DELETE", url=f"{self.API_V1_DOCUMENT}/{id}")
