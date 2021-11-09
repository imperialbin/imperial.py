from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from imperial.lib.base.base import Base

if TYPE_CHECKING:
    from imperial.lib.base.classes import BaseDocument


class BaseDocumentManager(Base, metaclass=ABCMeta):

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
               editors: list[str] = None) -> BaseDocument:
        """
        Uploads content to https://imperialb.in
        POST https://api.imperialb.in/v1/document
        """

    @abstractmethod
    def get(self, id: str) -> BaseDocument:
        """
        Gets document from https://imperialb.in
        GET https://api.imperialb.in/v1/document/:id
        """

    @abstractmethod
    def patch(self, id: str, content: str, *,
              language: str = None,
              expiration: int = 5,
              image_embed: bool = False,
              instant_delete: bool = False,
              public: bool = False,
              editors: list[str] = None) -> BaseDocument:
        """
        Edits document on https://imperialb.in
        PATCH https://api.imperialb.in/v1/document/:id
        """

    @abstractmethod
    def delete(self, id: str) -> None:
        """
        Deletes document from https://imperialb.in
        DELETE https://api.imperialb.in/v1/document/:id
        """
