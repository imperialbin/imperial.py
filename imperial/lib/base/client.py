import os
from abc import ABC, abstractmethod
from typing import Optional, List

import httpx

from imperial.common import MISSING, ensure_json, camel_dict_to_snake, snake_dict_to_camel
from imperial.exceptions import InvalidAuthorization, DocumentNotFound, ImperialError
from imperial.lib.base.document_manager import BaseDocumentManager


class BaseClient(ABC):
    __slots__ = "_token", "_headers"
    USER_AGENT = "imperial-py; (+https://github.com/imperialbin/imperial-py)"
    HOSTNAME = "https://staging-balls.impb.in"
    API = "https://staging-balls-api.impb.in"
    API_V1 = f"{API}/v1"
    API_V1_DOCUMENT = f"{API_V1}/document"

    def __init__(self, token: Optional[str] = MISSING):  # type: ignore[assignment]
        # if None is explicitly passed, then no token will be used.
        self._token: Optional[str] = token if token is not MISSING else os.environ.get("IMPERIAL_TOKEN", default=None)
        self._headers = {"User-Agent": self.USER_AGENT}
        if self._token is not None:
            self._headers["Authorization"] = self._token

    def __repr__(self):
        return f"<{self.__class__.__name__} token={self._token!r}>"

    @property
    def token(self) -> Optional[str]:
        return self._token

    @token.setter
    def token(self, new_token: str):
        self._token = new_token

    @property
    @abstractmethod
    def document(self) -> BaseDocumentManager:
        pass

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
