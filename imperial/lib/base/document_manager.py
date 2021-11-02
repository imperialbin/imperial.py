from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from imperial.lib.base.client import BaseClient
    from imperial.lib.base.document import BaseDocument


class BaseDocumentManager(ABC):
    __slots__ = "_client",

    def __init__(self, client: "BaseClient"):
        self._client = client

    @abstractmethod
    def create(self, content: str, *,
               language: str = None,
               expiration: int = 5,
               short_urls: bool = False,
               long_urls: bool = False,
               image_embed: bool = False,
               instant_delete: bool = False,
               encrypted: bool = False,
               password: str = None,
               public: bool = False,
               create_gist: bool = False,
               editors: list[str] = None) -> "BaseDocument":
        """
        Uploads content to https://imperialb.in
        POST https://staging-balls-api.impb.in/document
        """

    @abstractmethod
    def get(self, id: str) -> "BaseDocument":
        """
        Gets document from https://imperialb.in
        GET https://staging-balls-api.impb.in/document/:id
        """

    @abstractmethod
    def patch(self, id: str, content: str, *,
              language: str = None,
              expiration: int = 5,
              image_embed: bool = False,
              instant_delete: bool = False,
              public: bool = False,
              editors: list[str] = None) -> "BaseDocument":
        """
        Edits document on https://imperialb.in
        PATCH https://staging-balls-api.impb.in/document/:id
        """

    @abstractmethod
    def delete(self, id: str) -> None:
        """
        Deletes document from https://imperialb.in
        DELETE https://staging-balls-api.impb.in/document
        """
