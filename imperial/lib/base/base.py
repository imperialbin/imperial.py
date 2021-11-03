from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any
    from imperial.lib.base.client import BaseClient


class Base:

    def __init__(self, client: BaseClient):
        self._client: BaseClient = client

    def __repr__(self):
        return self._repr()

    def _repr(self, *keys: str, validate_keys: bool = False):
        if not keys:
            return f"<{self.__class__.__name__}>"
        matches: dict[str, Any] = {}
        for key in keys:
            value = getattr(self, key)
            if validate_keys and not value:
                continue
            matches[key] = repr(value)
        content = ", ".join(f"{k}={v}" for k, v in matches.items())
        return f"<{self.__class__.__name__} {content}>"

    @property
    def client(self) -> BaseClient:
        return self._client
