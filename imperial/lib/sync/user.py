from __future__ import annotations

from abc import ABCMeta

from imperial.lib.base.user import BaseUser

class User(BaseUser, metaclass=ABCMeta):
    pass