from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from imperial.common import snake_dict_to_camel, ensure_json, camel_dict_to_snake
from imperial.exceptions import InvalidAuthorization, ImperialError, DocumentNotFound
from imperial.lib.base.manager import Manager

if TYPE_CHECKING:
    import httpx
    from imperial.lib.base.client import BaseClient


class BaseRest(Manager, ABC):
    """
    Handles direct API interactions
    """
    USER_AGENT = "imperial-py; (+https://github.com/imperialbin/imperial-py)"
    HOSTNAME = "https://staging.impb.in"
    API = "https://staging-api.impb.in"
    API_V1 = f"{API}/v1"
    API_V1_DOCUMENT = f"{API_V1}/document"

    def __init__(self, client: BaseClient):
        super().__init__(client)
        self._http_client: httpx.Client | httpx.AsyncClient | None = None

    @property
    @abstractmethod
    def http_client(self) -> httpx.Client | httpx.AsyncClient | None:
        return self._http_client

    @abstractmethod
    def _request(self, *, method: str, url: str, data: dict | None = None) -> dict:
        """
        Handles the sending of requests
        """

    @property
    def headers(self) -> dict[str, str]:
        headers = {"User-Agent": self.USER_AGENT}
        if self.client.token:
            headers["Authorization"] = self.client.token
        return headers

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
        if not success or "data" not in json:
            raise ImperialError(message)
        return json["data"]
