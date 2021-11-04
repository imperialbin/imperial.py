from __future__ import annotations

from abc import ABCMeta

from imperial.lib.base.classes import BaseUser


class AsyncUser(BaseUser, metaclass=ABCMeta):
    pass
