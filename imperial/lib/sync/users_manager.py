from __future__ import annotations


from abc import ABCMeta

from imperial.lib.base.users_manager import BaseUsersManager
from imperial.lib.sync.user import User


class UsersManager(BaseUsersManager, metaclass=ABCMeta):

    def get(self, username: str) -> User:
        data = self.client.rest.request(method="GET", url=f"/user/{username}")
        return User(self.client, **data)
