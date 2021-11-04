from __future__ import annotations

from abc import ABCMeta

from imperial.lib.base.managers import BaseUsersManager
from imperial.lib.async_.classes import AsyncUser


class AsyncUsersManager(BaseUsersManager, metaclass=ABCMeta):

    async def get(self, username: str) -> AsyncUser:
        data = await self.client.rest.request(method="GET", path=f"/user/{username}")
        return AsyncUser(self.client, **data)
