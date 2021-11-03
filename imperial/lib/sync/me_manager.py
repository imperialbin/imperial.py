from __future__ import annotations

from abc import ABCMeta
from typing import Literal

from imperial.lib.base.me_manager import BaseMeManager
from imperial.lib.sync.document import Document
from imperial.lib.sync.me import Me


class MeManager(BaseMeManager, metaclass=ABCMeta):

    def get(self) -> Me:
        data = self.client.rest.request(method="GET", url="/user/@me")
        return Me(self.client, **data)

    def recent(self) -> list[Document] | None:
        data = self.client.rest.request(method="GET", url="/user/@me/recentDocuments")
        if not data:
            return
        return [Document(self.client, **doc) for doc in data]

    def set_icon(self, method: Literal["github", "gravatar"], url: str) -> None:
        self.client.rest.request(method="PATCH", url="/user/@me/icon", payload=locals())

