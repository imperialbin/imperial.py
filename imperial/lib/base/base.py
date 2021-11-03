from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from imperial.lib.base.client import BaseClient


class Base:

    def __init__(self, client: BaseClient):
        self._client: BaseClient = client

    def __repr__(self):
        return self._repr()

    def _repr(self, *keys: str, validate_keys: bool = False):
        if not keys:
            return f"<{self.__class__.__name__}>"
        elif not validate_keys:
            matches = [f"{k}={getattr(self, k)}" for k in keys]
        else:
            matches = [f"{k}={getattr(self, k)}" for k in keys if keys]
        content = ", ".join(matches)
        return f"<{self.__class__.__name__} {content}>"

    @property
    def client(self) -> BaseClient:
        return self._client
