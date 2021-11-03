from __future__ import annotations

from abc import ABC

from imperial.common import MISSING
from imperial.lib.base.client import BaseClient
from imperial.lib.sync.document_manager import DocumentManager
from imperial.lib.sync.me_manager import MeManager
from imperial.lib.sync.rest import Rest
from imperial.lib.sync.users_manager import UsersManager


class Client(BaseClient, ABC):

    def __init__(self, token: str | None = MISSING):  # type: ignore[assignment]
        super().__init__(token)
        self._rest = Rest(self)
        self._document = DocumentManager(self)
        self._users = UsersManager(self)
        self._me = MeManager(self)

    @property
    def rest(self) -> Rest:
        return self._rest

    @property
    def document(self) -> DocumentManager:
        return self._document

    @property
    def users(self) -> UsersManager:
        return self._users

    @property
    def me(self) -> MeManager:
        return self._me


if __name__ == "__main__":
    client = Client()
    user = client.me.get()
    print(user)
