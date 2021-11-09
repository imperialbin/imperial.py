from __future__ import annotations

from abc import abstractmethod, ABCMeta
from datetime import datetime
from typing import TYPE_CHECKING

from imperial.common import date_difference
from imperial.lib.base.base import Base

if TYPE_CHECKING:
    from imperial.lib.base.client import BaseClient


class BaseDocument(Base, metaclass=ABCMeta):
    __slots__ = (
        "_client",
        "_content",
        "_id",
        "_views",
        "_deleted",
        "_creation",
        "_expiration",
        "_language",
        "_image_embed",
        "_instant_delete",
        "_encrypted",
        "_public",
        "_editors",
    )

    def __init__(self, client: BaseClient, content: str, **kwargs):
        super().__init__(client)
        self._content: str = content
        self._id: str | None = None
        self._views: int = 0
        self._deleted: bool = False
        self._creation: datetime | None = None
        self._expiration: datetime | None = None
        self._language: str | None = None
        self._image_embed: bool = False
        self._instant_delete: bool = False
        self._encrypted: bool = False
        self._password: str | None = None
        self._public: bool = False
        self._editors: list[str] = []
        self._update(**kwargs)

    def __repr__(self):
        return self._repr("id", "expiration", "language", "password", "deleted", validate_keys=True)

    def _update(self, **kwargs):
        if not self._id:
            self._id: str = kwargs.get("id", None)
        self._content: str = kwargs.get("content", self._content)
        self._views: int = kwargs.get("views", self._views)

        timestamps = kwargs.get("timestamps", {})
        if "creation" in timestamps:
            self._creation: datetime = datetime.fromtimestamp(timestamps.get("creation"))
        if "expiration" in timestamps:
            self._expiration: datetime = datetime.fromtimestamp(timestamps.get("expiration"))

        settings = kwargs.get("settings", {})
        if "language" in settings:
            self._language = settings["language"]
        if "image_embed" in settings:
            self._image_embed = settings["image_embed"]
        if "instant_delete" in settings:
            self._instant_delete = settings["instant_delete"]
        if "encrypted" in settings:
            self._encrypted = settings["encrypted"]
        if "password" in settings:
            self._password = settings["password"]
        if "public" in settings:
            self._public = settings["public"]
        if "editors" in settings:
            self._editors = settings["editors"]

    @abstractmethod
    def edit(self, content: str, *,
             language: str = None,
             expiration: int = 5,
             image_embed: bool = False,
             instant_delete: bool = False,
             public: bool = False,
             editors: list[str] = None) -> None:
        """
        Edits document settings
        """

    @abstractmethod
    def duplicate(self, content: str, *,
                  language: str | None = None,
                  expiration: int = 5,
                  short_urls: bool = False,
                  long_urls: bool = False,
                  image_embed: bool = False,
                  instant_delete: bool = False,
                  encrypted: bool = False,
                  password: str | None = None,
                  public: bool = False,
                  create_gist: bool = False,
                  editors: list[str] = None) -> "BaseDocument":
        """
        Duplicates document with new settings, or settings from current document
        """

    @abstractmethod
    def delete(self) -> None:
        """
        Deletes document
        """

    # dynamic getters

    @property
    def short_urls(self):
        return len(self._id) == 4

    @property
    def long_urls(self):
        return len(self._id) == 32

    @property
    def editable(self) -> bool:
        return self.client.token and not self.deleted

    @property
    def raw(self) -> str:
        return f"{self.client.rest.HOSTNAME}/r/{self.id}"

    @property
    def formatted(self) -> str:
        return f"{self.client.rest.HOSTNAME}/p/{self.id}"

    @property
    def expiration_days(self) -> int:
        return date_difference(self.creation, self.expiration)

    @property
    def days_left(self) -> int:
        return date_difference(datetime.now(), self.expiration)

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
    def language(self) -> str | None:
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
    def password(self) -> str | None:
        return self._password

    @property
    def public(self) -> bool:
        return self._public

    @property
    def editors(self) -> list[str]:
        return self._editors
