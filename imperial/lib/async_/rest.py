from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

import httpx

from imperial.lib.base.rest import BaseRest

if TYPE_CHECKING:
    from imperial.lib.base.client import BaseClient


class AsyncRest(BaseRest, ABC):

    def __init__(self, client: BaseClient, http_client: httpx.AsyncClient | None = None):
        super().__init__(client)
        self._http_client: httpx.AsyncClient | None = http_client

    @property
    def http_client(self) -> httpx.AsyncClient | None:
        return self._http_client

    async def request(self, *, method: str, path: str, payload: dict | None = None) -> dict:
        url = self.API_V1 + path
        payload = self._payload(payload) if payload else {}
        resp: httpx.Response

        if self.http_client:
            resp = await self.http_client.request(
                method=method,
                url=url,
                json=payload,
                headers=self.headers
            )
        else:
            async with httpx.AsyncClient() as client:
                resp = await client.request(
                    method=method,
                    url=url,
                    json=payload,
                    headers=self.headers
                )
        return self._response(resp)
