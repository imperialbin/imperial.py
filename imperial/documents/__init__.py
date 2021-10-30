from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional, List

from imperial.clients import BaseClient
from imperial.common import HOSTNAME, date_difference


class BaseDocument(ABC):
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

    def __init__(self, client: BaseClient, content: str, **kwargs: Any):
        self._client: BaseClient = client
        self._content: str = content
        self._id: Optional[str] = None
        self._views: int = 0
        self._deleted: bool = False
        self._creation: Optional[datetime] = None
        self._expiration: Optional[datetime] = None
        self._language: Optional[str] = None
        self._image_embed: bool = False
        self._instant_delete: bool = False
        self._encrypted: bool = False
        self._password: Optional[str] = None
        self._public: bool = False
        self._editors: List[str] = []
        self._update(**kwargs)

    def __repr__(self):
        representation = f"<Document id={self.id}"
        if self.id:
            if self.expiration:
                representation += f" expiration={self.expiration:%x}"
            if self.language:
                representation += f" language={self.language}"
            if self.password:
                representation += f" password={self.password}"
            if self.deleted:
                # self.deleted will always be true here
                representation += " deleted=True"
        return representation + ">"

    def _update(self, **kwargs):
        self._id: str = kwargs.get("id", self._id)
        self._views: int = kwargs.get("views", self._views)

        timestamps = kwargs.get("timestamps", {})
        if "creation" in timestamps:
            self._creation: datetime = datetime.fromtimestamp(timestamps.get("creation"))
        if "expiration" in timestamps:
            self._expiration: datetime = datetime.fromtimestamp(timestamps.get("expiration"))

        settings = kwargs.get("settings", {})
        if "language" in settings:
            self._language: Optional[str] = settings["language"]
        if "image_embed" in settings:
            self._image_embed: bool = settings["image_embed"]
        if "instant_delete" in settings:
            self._instant_delete: bool = settings["instant_delete"]
        if "encrypted" in settings:
            self._encrypted: bool = settings["encrypted"]
        if "password" in settings:
            self._password: Optional[str] = settings["password"]
        if "public" in settings:
            self._public: bool = settings["public"]
        if "editors" in settings:
            self._editors: List[str] = settings["editors"]

    # signature should match patch_document (without id)
    @abstractmethod
    def edit(self, content: str, *,
             language: str = None,
             expiration: int = 5,
             image_embed: bool = False,
             instant_delete: bool = False,
             public: bool = False,
             editors: List[str] = None) -> None:
        """
        Edits document code on https://imperialb.in
        """

    @abstractmethod
    def duplicate(self, content: str, *,
                  language: Optional[str] = None,
                  expiration: int = 5,
                  short_urls: bool = False,
                  long_urls: bool = False,
                  image_embed: bool = False,
                  instant_delete: bool = False,
                  encrypted: bool = False,
                  password: Optional[str] = None,
                  public: bool = False,
                  create_gist: bool = False,
                  editors: List[str] = None) -> "BaseDocument":
        """
        Duplicates document
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
        return self._client.token and not self.deleted

    @property
    def raw(self) -> str:
        return f"{HOSTNAME}/r/{self.id}"

    @property
    def formatted(self) -> str:
        return f"{HOSTNAME}/p/{self.id}"

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
    def password(self) -> Optional[str]:
        return self._password

    @property
    def public(self) -> bool:
        return self._public

    @property
    def editors(self) -> List[str]:
        return self._editors
