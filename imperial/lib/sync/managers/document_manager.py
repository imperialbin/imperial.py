from __future__ import annotations

from imperial.lib.base.managers import BaseDocumentManager
from imperial.lib.sync.classes import Document


class DocumentManager(BaseDocumentManager):

    def create(self, content: str, *,
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
               editors: list[str] = None) -> Document:
        """
        Uploads content to https://imperialb.in
        POST https://staging-balls-api.impb.in/document
        """
        data = self.client.rest.request(method="POST", path="/document", payload=locals())
        return Document(client=self._client, **data)

    def get(self, id: str) -> Document:
        """
        Gets document from https://imperialb.in
        GET https://staging-balls-api.impb.in/document/:id
        """
        data = self.client.rest.request(method="GET", path=f"/document/{id}")
        return Document(client=self._client, **data)

    def patch(self, id: str, content: str, *,
              language: str = None,
              expiration: int = 5,
              image_embed: bool = False,
              instant_delete: bool = False,
              public: bool = False,
              editors: list[str] = None) -> Document:
        """
        Edits document on https://imperialb.in
        PATCH https://staging-balls-api.impb.in/document/:id
        """
        data = self.client.rest.request(method="PATCH", path="/document/", payload=locals())
        return Document(client=self._client, **data)

    def delete(self, id: str) -> None:
        """
        Deletes document from https://imperialb.in
        DELETE https://staging-balls-api.impb.in/document
        """
        self.client.rest.request(method="DELETE", path=f"/document/{id}")
