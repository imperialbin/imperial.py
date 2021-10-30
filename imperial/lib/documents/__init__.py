from abc import ABC
from datetime import datetime
from typing import Any, Optional, List

from imperial.lib.clients import BaseClient


class BaseDocument(ABC):
    __slots__ = (
        "_client",
        "_content",
        "_id",
        "_views",
        "_deleted",
        "_language",
        "_image_embed",
        "_instant_delete",
        "_encrypted",
        "_public",
        "_editors",
    )

    def __init__(self, client: BaseClient, content: str, **kwargs: Any):
        self._client: BaseClient = client

        self._content: str = content
        self._id: str = kwargs.get("id")
        self._views: int = kwargs.get("views")
        self._deleted: bool = False

        timestamps = kwargs.get("timestamps", {})
        self._creation: datetime = datetime.fromtimestamp(timestamps.get("creation"))
        self._expiration: datetime = datetime.fromtimestamp(timestamps.get("expiration"))

        settings = kwargs.get("settings", {})
        self._language: Optional[str] = settings.get("language", None)
        self._image_embed: bool = settings.get("image_embed", False)
        self._instant_delete: bool = settings.get("instant_delete", False)
        self._encrypted: bool = settings.get("encrypted", False)
        self._public: bool = settings.get("public", False)
        self._editors: List[str] = settings.get("editors", [])

    # dynamic getters

    @property
    def short_urls(self):
        return len(self._id) == 4

    @property
    def long_urls(self):
        return len(self._id) == 32

    @property
    def editable(self) -> bool:
        return self._client.token and not self.deleted

    # getters

    @property
    def content(self) -> str:
        return self._content

    @property
    def id(self) -> str:
        return self._id

    @property
    def views(self) -> int:
        return self._views

    @property
    def deleted(self) -> bool:
        return self._deleted

    @property
    def creation(self) -> datetime:
        return self._creation

    @property
    def expiration(self) -> datetime:
        return self._expiration

    @property
    def language(self) -> Optional[str]:
        return self._language

    @property
    def image_embed(self) -> bool:
        return self._image_embed

    @property
    def instant_delete(self) -> bool:
        return self._instant_delete

    @property
    def encrypted(self) -> bool:
        return self._encrypted

    @property
    def public(self) -> bool:
        return self._public

    @property
    def editors(self) -> List[str]:
        return self._editors
