from __future__ import annotations

import asyncio
from abc import ABC

import httpx

from imperial.common import MISSING
from imperial.lib.async_.managers import AsyncDocumentManager, AsyncMeManager, AsyncUsersManager
from imperial.lib.async_.rest import AsyncRest
from imperial.lib.base.client import BaseClient


class AsyncClient(BaseClient, ABC):

    def __init__(self, token: str | None = MISSING):  # type: ignore[assignment]
        super().__init__(token)
        self._rest = AsyncRest(self)
        self._document = AsyncDocumentManager(self)
        self._users = AsyncUsersManager(self)
        self._me = AsyncMeManager(self)

    async def __aenter__(self):
        self._rest = AsyncRest(self, http_client=httpx.AsyncClient())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._rest.http_client.aclose()

    @property
    def rest(self) -> AsyncRest:
        return self._rest

    @property
    def document(self) -> AsyncDocumentManager:
        return self._document

    @property
    def users(self) -> AsyncUsersManager:
        return self._users

    @property
    def me(self) -> AsyncMeManager:
        return self._me


async def _main():
    client = AsyncClient()
    print(client)
    print(client.rest)
    print(client.document)
    print(await client.document.create("yeah"))
    print(client.me)
    print(await client.me.get())
    print(client.users)
    print(await client.users.get("pxseu"))

if __name__ == "__main__":
    asyncio.run(_main())
