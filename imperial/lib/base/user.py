from __future__ import annotations

from abc import ABCMeta
from typing import TYPE_CHECKING

from imperial.lib.base.base import Base

if TYPE_CHECKING:
    from imperial.lib.base.client import BaseClient


class BaseUser(Base, metaclass=ABCMeta):

    def __init__(self, client: BaseClient, username: str, icon: str, member_plus: bool, banned: bool):
        super().__init__(client)
        self._username: str
        self._icon: str
        self._member_plus: bool = False
        self._banned: bool = False
        self._update(username, icon, member_plus, banned)

    def __repr__(self):
        return self._repr("username", "member_plus")

    def _update(self, username: str, icon: str, member_plus: bool, banned: bool):
        self._username = username
        self._icon = icon
        self._member_plus = member_plus
        self._banned = banned

    @property
    def username(self) -> str:
        return self._username

    @property
    def icon(self):
        return self._icon

    @property
    def icon_url(self):
        return f"{self.client.rest.HOSTNAME}{self.icon}"

    @property
    def member_plus(self):
        return self._member_plus

    @property
    def banned(self):
        return self._banned
