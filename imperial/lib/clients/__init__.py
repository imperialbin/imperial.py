import os
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, List

import httpx

from imperial.lib.common import MISSING, ensure_json, camel_dict_to_snake, snake_dict_to_camel
from imperial.lib.exceptions import InvalidAuthorization, DocumentNotFound, ImperialError

if TYPE_CHECKING:
    from imperial.lib.documents import BaseDocument


class BaseClient(ABC):
    __slots__ = "_token",

    def __init__(self, token: Optional[str] = MISSING):  # type: ignore[assignment]
        # if None is explicitly passed, then no token will be used.
        self._token: Optional[str] = token if token is not MISSING else os.environ.get("IMPERIAL_TOKEN", default=None)

    def __repr__(self):
        return f"<{self.__class__.__name__} token={self._token!r}>"

    @property
    def token(self) -> Optional[str]:
        return self._token

    @token.setter
    def token(self, new_token: str):
        self._token = new_token

    @abstractmethod
    def create_document(self, content: str, *,
                        language: str = None,
                        expiration: int = 5,
                        short_urls: bool = False,
                        long_urls: bool = False,
                        image_embed: bool = False,
                        instant_delete: bool = False,
                        encrypted: bool = False,
                        password: str = None,
                        public: bool = False,
                        create_gist: bool = False,
                        editors: List[str] = None) -> "BaseDocument":
        """
        Uploads content to https://imperialb.in
        POST https://staging-balls-api.impb.in/document
        """

    @abstractmethod
    def get_document(self, id: str) -> "BaseDocument":
        """
        Gets document from https://imperialb.in
        GET https://staging-balls-api.impb.in/document/:id
        """

    @abstractmethod
    def patch_document(self, id: str, content: str, *,
                       language: str = None,
                       expiration: int = 5,
                       image_embed: bool = False,
                       instant_delete: bool = False,
                       public: bool = False,
                       editors: List[str] = None) -> "BaseDocument":
        """
        Edits document on https://imperialb.in
        PATCH https://staging-balls-api.impb.in/document/:id
        """

    @abstractmethod
    def delete_document(self, id: str) -> None:
        """
        Deletes document from https://imperialb.in
        DELETE https://staging-balls-api.impb.in/document
        """

    @abstractmethod
    def _create_document(self, content: str, *,
                         language: str = None,
                         expiration: int = 5,
                         short_urls: bool = False,
                         long_urls: bool = False,
                         image_embed: bool = False,
                         instant_delete: bool = False,
                         encrypted: bool = False,
                         password: str = None,
                         public: bool = False,
                         create_gist: bool = False,
                         editors: List[str] = None) -> dict:
        """
        Uploads content to https://imperialb.in
        POST https://staging-balls-api.impb.in/document
        """

    @abstractmethod
    def _get_document(self, id: str) -> dict:
        """
        Gets document from https://imperialb.in
        GET https://staging-balls-api.impb.in/document/:id
        """

    @abstractmethod
    def _patch_document(self, id: str, content: str, *,
                        language: str = None,
                        expiration: int = 5,
                        image_embed: bool = False,
                        instant_delete: bool = False,
                        public: bool = False,
                        editors: List[str] = None) -> dict:
        """
        Edits document on https://imperialb.in
        PATCH https://staging-balls-api.impb.in/document/:id
        """

    @abstractmethod
    def _delete_document(self, id: str) -> dict:
        """
        Deletes document from https://imperialb.in
        DELETE https://staging-balls-api.impb.in/document
        """

    @property
    def headers(self) -> dict:
        headers = {"User-Agent": "imperial-py; (+https://github.com/imperialbin/imperial-py)"}
        if self._token:
            headers["Authorization"] = self._token
        return headers

    @abstractmethod
    def _request(self, *, method: str, url: str, data: Optional[dict] = None) -> dict:
        """
        Handles the sending of requests
        """

    @staticmethod
    def _payload(data: dict) -> dict:
        """
        Prepares data before it's sent in _request
        """
        data.pop("self", None)
        new_data: dict = {"settings": {}}
        for k, v in data.items():
            if v is None:
                continue
            if k not in ("id", "content", "settings"):
                new_data["settings"][k] = v
            else:
                new_data[k] = v
        return snake_dict_to_camel(new_data)

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
