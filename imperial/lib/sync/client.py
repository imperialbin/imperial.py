from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from imperial.common import MISSING
from imperial.lib.base.client import BaseClient
from imperial.lib.sync.document_manager import DocumentManager
from imperial.lib.sync.rest import Rest

if TYPE_CHECKING:
    from imperial.lib.base.rest import BaseRest


class Client(BaseClient, ABC):

    def __init__(self, token: str | None = MISSING):  # type: ignore[assignment]
        super().__init__(token)
        self._rest = Rest(self)
        self._document = DocumentManager(self)

    @property
    def rest(self) -> BaseRest:
        return self._rest

    @property
    def document(self):
        return self._document


if __name__ == "__main__":
    client = Client()
    doc = client.document.create(content="yeah")
    print(doc)
    print(doc.formatted)