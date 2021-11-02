from __future__ import annotations

from abc import ABC

from imperial.common import MISSING
from imperial.lib.base.client import BaseClient
from imperial.lib.sync.document_manager import DocumentManager
from imperial.lib.sync.rest import Rest


class Client(BaseClient, ABC):

    def __init__(self, token: str | None = MISSING):  # type: ignore[assignment]
        super().__init__(token)
        self._rest = Rest(self)
        self._document = DocumentManager(self)

    @property
    def document(self):
        return self._document
