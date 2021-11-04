from __future__ import annotations

from abc import ABCMeta

from imperial.lib.base.classes import BaseUser


class User(BaseUser, metaclass=ABCMeta):
    pass
