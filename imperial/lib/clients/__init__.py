from abc import ABC, abstractmethod
from typing import Union, Optional, List

import httpx

from imperial.lib.common import MISSING, ensure_json, camel_dict_to_snake, snake_dict_to_camel
from imperial.lib.exceptions import InvalidAuthorization, DocumentNotFound, ImperialError


class BaseClient(ABC):
    __slots__ = ("_token", "_client")

    def __init__(self, token: str = MISSING):  # type: ignore[assignment]
        self._token = token
        self._client: Optional[Union[httpx.Client, httpx.AsyncClient]]

    def __repr__(self):
        return f"<{self.__class__.__name__} token={self._token!r}>"

    @abstractmethod
    def create_document(self, content: str, *,
                        language: Optional[str] = None,
                        expiration: int = 5,
                        short_urls: bool = False,
                        long_urls: bool = False,
                        image_embed: bool = False,
                        instant_delete: bool = False,
                        encrypted: bool = False,
                        password: Optional[str] = None,
                        public: bool = False,
                        create_gist: bool = False,
                        editors: List[str] = None):
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
    def patch_document(self, id: str, content: str, *,
                       language: Optional[str] = None,
                       expiration: int = 5,
                       short_urls: bool = False,
                       long_urls: bool = False,
                       image_embed: bool = False,
                       instant_delete: bool = False,
                       public: bool = False,
                       editors: List[str] = None):
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
    def _payload(data: dict):
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
        print(resp.text)

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
