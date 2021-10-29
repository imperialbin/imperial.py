from abc import ABC, abstractmethod
from typing import Union, Optional

import httpx

from imperial.lib.common import MISSING
from imperial.lib.document import Settings


class BaseClient(ABC):
    __slots__ = ("_token", "_client")

    def __init__(self, token: str = MISSING):
        self._token = token
        self._client: Optional[Union[httpx.Client, httpx.AsyncClient]]

    @abstractmethod
    def _request(self, *, method: str, url: str, data: dict):
        pass

    @abstractmethod
    def create_document(self, settings: Union[dict, Settings]):
        """
        Uploads content to https://imperialb.in
        POST https://staging-balls-api.impb.in/document
        """

    @abstractmethod
    def get_document(self, id: str):
        """
        Gets document from https://imperialb.in
        GET https://staging-balls-api.impb.in/document/:id
        """

    @abstractmethod
    def patch_document(self, settings: Union[dict, Settings]):
        pass

    @abstractmethod
    def delete_document(self, id: str):
        pass
