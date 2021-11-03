from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from imperial.lib.base.base import Base

if TYPE_CHECKING:
    from imperial.lib.base.user import BaseUser


class BaseUsersManager(Base, metaclass=ABCMeta):

    @abstractmethod
    def get(self, username: str) -> BaseUser:
        pass
