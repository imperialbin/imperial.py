from __future__ import annotations

from imperial.lib.base.document_manager import BaseDocumentManager
from imperial.lib.sync.document import Document


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
               editors: list[str] = None) -> "BaseDocument":
        """
        Uploads content to https://imperialb.in
        POST https://staging-balls-api.impb.in/document
        """
        resp = self._client._create_document(content=content, language=language, expiration=expiration,
                                             short_urls=short_urls, long_urls=long_urls, image_embed=image_embed,
                                             instant_delete=instant_delete, encrypted=encrypted, password=password,
                                             public=public, create_gist=create_gist, editors=editors)
        return Document(client=self._client, **resp["data"])

    def get(self, id: str) -> "BaseDocument":
        """
        Gets document from https://imperialb.in
        GET https://staging-balls-api.impb.in/document/:id
        """
        return Document(client=self._client, **self._client._get_document(id))

    def patch(self, id: str, content: str, *,
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
        resp = self._client._patch_document(id, content, language=language, expiration=expiration,
                                            image_embed=image_embed, instant_delete=instant_delete, public=public,
                                            editors=editors)
        return Document(client=self._client, **resp["data"])

    def delete(self, id: str) -> None:
        """
        Deletes document from https://imperialb.in
        DELETE https://staging-balls-api.impb.in/document
        """
        self._client._delete_document(id)
