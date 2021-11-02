from __future__ import annotations

from abc import ABC

from imperial.exceptions import DocumentNotFound, InvalidAuthorization
from imperial.lib.base.document import BaseDocument


class Document(BaseDocument, ABC):

    def edit(self, content: str = None, *,
             language: str = None,
             expiration: int = 5,
             image_embed: bool = False,
             instant_delete: bool = False,
             public: bool = False,
             editors: list[str] = None) -> None:

        if self.deleted:
            raise DocumentNotFound(self.id)
        if not self.editable or not self.client.token:
            raise InvalidAuthorization()

        payload = {
            "id": self.id,
            "content": content or self.content,
            "language": language or self.language,
            "expiration": expiration or self.expiration_days,
            "image_embed": image_embed or self.image_embed,
            "public": public or self.public,
            "editors": editors or self.editors
        }

        settings = self.client.rest.request(method="PATCH", url="/document", payload=payload)
        self._update(**settings)

    def duplicate(self, content: str, *,
                  language: str | None = None,
                  expiration: int = 5,
                  short_urls: bool = False,
                  long_urls: bool = False,
                  image_embed: bool = False,
                  instant_delete: bool = False,
                  encrypted: bool = False,
                  password: str | None = None,
                  public: bool = False,
                  create_gist: bool = False,
                  editors: list[str] = None) -> BaseDocument:

        payload = {
            "content": content or self.content,
            "language": language or self.language,
            "expiration": expiration or self.expiration_days,
            "short_urls": short_urls or self.short_urls,
            "long_urls": long_urls or self.long_urls,
            "image_embed": image_embed or self.image_embed,
            "instant_delete": instant_delete or self.instant_delete,
            "encrypted": encrypted or self.encrypted,
            "password": password or self.password,
            "public": public or self.public,
            "create_gist": create_gist,
            "editors": editors or self.editors
        }

        data = self.client.rest.request(method="POST", url="/document", payload=payload)
        return Document(self.client, **data)

    def delete(self) -> None:
        self.client.rest.request(method="DELETE", url=f"/document/{self.id}")
