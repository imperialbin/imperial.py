from __future__ import annotations

from abc import ABCMeta
from typing import Literal

from imperial.lib.base.managers import BaseMeManager
from imperial.lib.async_.classes import AsyncDocument, AsyncMe


class AsyncMeManager(BaseMeManager, metaclass=ABCMeta):

    async def get(self) -> AsyncMe:
        data = await self.client.rest.request(method="GET", path="/user/@me")
        return AsyncMe(self.client, **data)

    async def recent(self) -> list[AsyncDocument] | None:
        data = await self.client.rest.request(method="GET", path="/user/@me/recentDocuments")
        if not data:
            return
        return [AsyncDocument(self.client, **doc) for doc in data]

    async def set_icon(self, method: Literal["github", "gravatar"], url: str) -> None:
        await self.client.rest.request(method="PATCH", path="/user/@me/icon", payload=locals())
