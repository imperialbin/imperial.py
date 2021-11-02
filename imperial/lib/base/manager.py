from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from imperial.lib.base.client import BaseClient


class Manager:

    def __init__(self, client: BaseClient):
        self._client: BaseClient = client

    @property
    def client(self) -> BaseClient:
        return self._client
