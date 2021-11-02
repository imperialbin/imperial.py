from __future__ import annotations

import os
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from imperial.common import MISSING
from imperial.exceptions import InvalidAuthorization

if TYPE_CHECKING:
    from imperial.lib.base.rest import BaseRest
    from imperial.lib.base.document_manager import BaseDocumentManager


class BaseClient(metaclass=ABCMeta):

    def __init__(self, token: str | None = MISSING):  # type: ignore[assignment]
        # if None is explicitly passed, then no token will be used.
        self._token: str | None = token if token is not MISSING else os.environ.get("IMPERIAL_TOKEN", default=None)

    def __repr__(self):
        return f"<{self.__class__.__name__} token={self._token!r}>"

    @property
    @abstractmethod
    def rest(self) -> BaseRest:
        pass

    @property
    @abstractmethod
    def document(self) -> BaseDocumentManager:
        pass

    @property
    def token(self) -> str | None:
        return self._token

    @token.setter
    def token(self, new_token: str):
        self._token = new_token

    def _assert_token(self):
        if not self.token:
            raise InvalidAuthorization()
