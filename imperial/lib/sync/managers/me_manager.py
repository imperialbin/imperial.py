from __future__ import annotations

from abc import ABCMeta
from typing import Literal

from imperial.lib.base.managers import BaseMeManager
from imperial.lib.sync.classes import Document, Me


class MeManager(BaseMeManager, metaclass=ABCMeta):

    def get(self) -> Me:
        data = self.client.rest.request(method="GET", path="/user/@me")
        return Me(self.client, **data)

    def recent(self) -> list[Document] | None:
        data = self.client.rest.request(method="GET", path="/user/@me/recentDocuments")
        if not data:
            return
        return [Document(self.client, **doc) for doc in data]

    def set_icon(self, method: Literal["github", "gravatar"], url: str) -> None:
        self.client.rest.request(method="PATCH", path="/user/@me/icon", payload=locals())
