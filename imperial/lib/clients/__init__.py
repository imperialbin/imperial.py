from abc import ABC, abstractmethod
from typing import Union, Optional

import httpx

from imperial.lib.common import MISSING, ensure_json, camel_dict_to_snake
from imperial.lib.document import Settings
from imperial.lib.exceptions import InvalidAuthorization, DocumentNotFound, ImperialError


class BaseClient(ABC):
    __slots__ = ("_token", "_client")

    def __init__(self, token: str = MISSING):  # type: ignore[assignment]
        self._token = token
        self._client: Optional[Union[httpx.Client, httpx.AsyncClient]]

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

    @abstractmethod
    def _request(self, *, method: str, url: str, data: Optional[dict] = None) -> httpx.Response:
        """
        Handles the sending of requests
        """

    @staticmethod
    def _response(resp: httpx.Response) -> dict:
        """
        Handles parsing response of request
        """
        json = ensure_json(resp)
        json = camel_dict_to_snake(json)

        success = json.get("success", False)
        message = json.get("message", None)

        if resp.status_code == 401:
            raise InvalidAuthorization()
        if resp.status_code == 404:
            raise DocumentNotFound()
        if not success:
            raise ImperialError(message)
        return json
