from __future__ import annotations

from abc import ABCMeta

from imperial.lib.base.managers import BaseUsersManager
from imperial.lib.sync.classes import User


class UsersManager(BaseUsersManager, metaclass=ABCMeta):

    def get(self, username: str) -> User:
        data = self.client.rest.request(method="GET", path=f"/user/{username}")
        return User(self.client, **data)
