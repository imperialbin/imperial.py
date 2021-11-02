import os
from abc import ABC, abstractmethod
from typing import Optional

import httpx

from imperial.common import MISSING, ensure_json, camel_dict_to_snake, snake_dict_to_camel
from imperial.exceptions import InvalidAuthorization, DocumentNotFound, ImperialError
from imperial.lib.base.document_manager import BaseDocumentManager


class BaseClient(ABC):

    def __init__(self, token: Optional[str] = MISSING):  # type: ignore[assignment]
        # if None is explicitly passed, then no token will be used.
        self._token: Optional[str] = token if token is not MISSING else os.environ.get("IMPERIAL_TOKEN", default=None)

    def __repr__(self):
        return f"<{self.__class__.__name__} token={self._token!r}>"

    @property
    @abstractmethod
    def document(self) -> BaseDocumentManager:
        pass

    @property
    def token(self) -> Optional[str]:
        return self._token

    @token.setter
    def token(self, new_token: str):
        self._token = new_token

    def _assert_token(self):
        if not self.token:
            raise InvalidAuthorization()
