from __future__ import annotations

from imperial.lib.async_.classes import AsyncDocument
from imperial.lib.base.managers import BaseDocumentManager


class AsyncDocumentManager(BaseDocumentManager):

    async def create(self, content: str, *,
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
                     editors: list[str] = None) -> AsyncDocument:
        """
        Uploads content to https://imperialb.in
        POST https://staging-balls-api.impb.in/document
        """
        data = await self.client.rest.request(method="POST", path="/document", payload=locals())
        return AsyncDocument(client=self._client, **data)

    async def get(self, id: str, password: str = None) -> AsyncDocument:
        """
        Gets document from https://imperialb.in
        GET https://staging-balls-api.impb.in/document/:id
        """
        path = f"/document/{id}"
        if password:
            path += f"?password={password}"
        data = await self.client.rest.request(method="GET", path=path)
        return AsyncDocument(client=self._client, **data)

    async def patch(self, id: str, content: str, *,
                    language: str = None,
                    expiration: int = 5,
                    image_embed: bool = False,
                    instant_delete: bool = False,
                    public: bool = False,
                    editors: list[str] = None) -> AsyncDocument:
        """
        Edits document on https://imperialb.in
        PATCH https://staging-balls-api.impb.in/document/:id
        """
        data = await self.client.rest.request(method="PATCH", path="/document/", payload=locals())
        return AsyncDocument(client=self._client, **data)

    async def delete(self, id: str) -> None:
        """
        Deletes document from https://imperialb.in
        DELETE https://staging-balls-api.impb.in/document
        """
        await self.client.rest.request(method="DELETE", path=f"/document/{id}")
