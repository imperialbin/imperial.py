from __future__ import annotations


from abc import ABCMeta
from typing import TYPE_CHECKING

from imperial.lib.base.base import Base

if TYPE_CHECKING:
    from imperial.lib.base.client import BaseClient


class BaseMe(Base, metaclass=ABCMeta):

    def __init__(self, client: BaseClient, **kwargs):
        super().__init__(client)
        self._id: str
        self._user_id: int = 0
        self._username: str
        self._email: str
        self._banned: bool = False
        self._confirmed: bool = False
        self._icon: str
        self._member_plus: bool = False
        self._documents_made: int = 0
        self._active_unlimited_documents: int = 0
        self._discord_id: str
        self._admin: bool = False
        self._api_token: str = self.client.token
        self._github_access: str
        self._opt: str
        self._update(**kwargs)

    def _update(self, **kwargs):
        if "id" in kwargs:
            self._id = kwargs["id"]
        if "user_id" in kwargs:
            self._user_id = kwargs["user_id"]
        if "username" in kwargs:
            self._username = kwargs["username"]
        if "email" in kwargs:
            self._email = kwargs["email"]
        if "banned" in kwargs:
            self._banned = kwargs["banned"]
        if "confirmed" in kwargs:
            self._confirmed = kwargs["confirmed"]
        if "icon" in kwargs:
            self._icon = kwargs["icon"]
        if "member_plus" in kwargs:
            self._member_plus = kwargs["member_plus"]
        if "documents_made" in kwargs:
            self._documents_made = kwargs["documents_made"]
        if "active_unlimited_documents" in kwargs:
            self._active_unlimited_documents = kwargs["active_unlimited_documents"]
        if "discord_id" in kwargs:
            self._discord_id = kwargs["discord_id"]
        if "admin" in kwargs:
            self._admin = kwargs["admin"]
        if "api_token" in kwargs:
            self._api_token = kwargs["api_token"]
        if "github_access" in kwargs:
            self._github_access = kwargs["github_access"]
        if "opt" in kwargs:
            self._opt = kwargs["opt"]
