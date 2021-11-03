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

    def __repr__(self):
        return self._repr("username", "email", "member_plus")

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

    @property
    def id(self) -> str:
        return self._id

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email

    @property
    def banned(self) -> bool:
        return self._banned

    @property
    def confirmed(self) -> bool:
        return self._confirmed

    @property
    def icon(self) -> str:
        return self._icon

    @property
    def member_plus(self) -> bool:
        return self._member_plus

    @property
    def documents_made(self) -> int:
        return self._documents_made

    @property
    def active_unlimited_documents(self) -> int:
        return self._active_unlimited_documents

    @property
    def discord_id(self) -> str:
        return self._discord_id

    @property
    def admin(self) -> bool:
        return self._admin

    @property
    def api_token(self) -> str:
        return self._api_token

    @property
    def github_access(self) -> str:
        return self._github_access

    @property
    def opt(self) -> str:
        return self._opt
