from __future__ import annotations

from abc import abstractmethod, ABCMeta
from typing import TYPE_CHECKING, Literal

from imperial.lib.base.base import Base

if TYPE_CHECKING:
    from imperial.lib.base.me import BaseMe
    from imperial.lib.sync.document import Document


class BaseMeManager(Base, metaclass=ABCMeta):

    @abstractmethod
    def get(self) -> BaseMe:
        pass

    @abstractmethod
    def recent(self) -> list[Document] | None:
        pass

    @abstractmethod
    def set_icon(self, method: Literal["github", "gravatar"], url: str):
        pass
