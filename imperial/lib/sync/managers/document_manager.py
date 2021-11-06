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
        data = self.client.rest.request(method="POST", path="/document", payload=locals())
        return Document(client=self._client, **data)

    def get(self, id: str, password: str = None) -> Document:
        path = f"/document/{id}"
        if password:
            path += f"?password={password}"
        data = self.client.rest.request(method="GET", path=path)
        return Document(client=self._client, **data)

    def patch(self, id: str, content: str, *,
              language: str = None,
              expiration: int = 5,
              image_embed: bool = False,
              instant_delete: bool = False,
              public: bool = False,
              editors: list[str] = None) -> Document:
        data = self.client.rest.request(method="PATCH", path="/document/", payload=locals())
        return Document(client=self._client, **data)

    def delete(self, id: str) -> None:
        self.client.rest.request(method="DELETE", path=f"/document/{id}")
