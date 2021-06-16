__title__ = "Imperialb.in simple API wrapper"
__author__ = "Hexiro"

import os
from typing import List, Optional

from . import client
from .document import Document
from .checks import ensure_api_token

__all__ = (
    "Imperial",
    "create_document",
    "get_document",
    "edit_document",
    "delete_document",
    "verify",
    "purge_documents"
)


class Imperial:
    __slots__ = (
        "__api_token",
    )

    def __init__(self, api_token: str = None):
        """
        :param api_token: ImperialBin API token
        15 requests max every 15 minutes; unlimited with an api token.
        """
        # set token overrides path set token
        self.__api_token = api_token or os.environ.get("IMPERIAL_TOKEN")
        if self.api_token is not None:
            ensure_api_token(self.api_token)

    def __repr__(self):
        return f"<Imperial api_token={self.api_token}>"

    @property
    def api_token(self) -> Optional[str]:
        return self.__api_token

    @api_token.setter
    def api_token(self, new_token):
        if new_token is not None:
            ensure_api_token(new_token)
        self.__api_token = new_token

    def create_document(self,
                        content: str, *,
                        short_urls: bool = False,
                        longer_urls: bool = False,
                        language: str = None,
                        public: bool = False,
                        instant_delete: bool = False,
                        image_embed: bool = False,
                        expiration: int = 5,
                        encrypted: bool = False,
                        password: str = None,
                        editors: List[str] = None) -> Document:
        """
        Uploads content to https://imperialb.in
        POST https://imperialb.in/api/document
        :param content: the text content to store on imperialbin
        :param short_urls: creates 4 character URLs instead of 8
        :param longer_urls: creates 26 character URLs instead of 8
        :param language: the programming language of the content (or plain text)
        :param public: makes the document publicly viewable on the imperial public page
        :param instant_delete: instantly deletes the document after being viewed once.
        :param image_embed: have a sneak peak with an image through Open Graph embeds
        :param expiration: sets the number of days before the paste deletes (overwritten by instant_delete)
        :param encrypted: encrypts the document with a password and aes256 encryption
        :param password: the password if a document is encrypted
        :param editors: a list of users who are allowed to edit a document
        """

        resp = client.create_document(
            content=content,
            short_urls=short_urls,
            longer_urls=longer_urls,
            language=language,
            public=public,
            instant_delete=instant_delete,
            image_embed=image_embed,
            expiration=expiration,
            encrypted=encrypted,
            password=password,
            editors=editors,
            api_token=self.api_token
        )

        return Document(
            content=content,
            api_token=self.api_token,
            **resp["document"]
        )

    def get_document(self, document_id: str, *, password: str = None) -> Document:
        """
        Gets document from https://imperialb.in
        GET https://imperialb.in/api/document/:documentID
        :param document_id: the id associated with the imperialbin document
        :param password: the password if a document is encrypted
        """
        resp = client.get_document(
            document_id=document_id,
            password=password,
            api_token=self.api_token
        )

        return Document(
            content=resp["content"],
            api_token=self.api_token,
            **resp["document"]
        )

    def edit_document(self, content: str, document_id: str) -> Document:
        """
        Edits document content on https://imperialb.in
        PATCH https://imperialb.in/api/document
        :param content: the text content to store on imperialbin
        :param document_id: the id associated with the imperialbin document
        """
        resp = client.edit_document(
            content=content,
            document_id=document_id,
            api_token=self.api_token
        )

        return Document(
            content=content,
            api_token=self.api_token,
            **resp["document"]
        )

    def delete_document(self, document_id: str) -> None:
        """
        Deletes document from https://imperialb.in
        DELETE https://imperialb.in/api/document/:documentID
        :param document_id: ImperialBin Document ID.
        """
        client.delete_document(document_id, api_token=self.api_token)

    def verify(self) -> None:
        """
        Validate API token from https://imperialb.in
        GET https://imperialb.in/api/checkApiToken/:apiToken
        """
        client.check_api_token(self.api_token)

    def purge_documents(self) -> int:
        """
        Deletes all documents created by an API token
        DELETE https://imperialb.in/api/purgeDocuments
        :return: number of accounts deleted
        """
        return client.purge_documents(api_token=self.api_token)["number_deleted"]


# shorthand functions


def create_document(content: str, *,
                    api_token: str = None,
                    short_urls: bool = False,
                    longer_urls: bool = False,
                    language: str = None,
                    public: bool = False,
                    instant_delete: bool = False,
                    image_embed: bool = False,
                    expiration: int = 5,
                    encrypted: bool = False,
                    password: str = None,
                    editors: List[str] = None) -> Document:
    """
    Uploads content to https://imperialb.in
    POST https://imperialb.in/api/document
    :param content: the text content to store on imperialbin
    :param api_token: the API token linked with your imperial account
    :param short_urls: creates 4 character URLs instead of 8
    :param longer_urls: creates 26 character URLs instead of 8
    :param language: the programming language of the content (or plain text)
    :param public: makes the document publicly viewable on the imperial public page
    :param instant_delete: instantly deletes the document after being viewed once.
    :param image_embed: have a sneak peak with an image through Open Graph embeds
    :param expiration: sets the number of days before the paste deletes (overwritten by instant_delete)
    :param encrypted: encrypts the document with a password and aes256 encryption
    :param password: the password if a document is encrypted
    :param editors: a list of users who are allowed to edit a document
    """
    return Imperial(api_token).create_document(
        content=content,
        short_urls=short_urls,
        longer_urls=longer_urls,
        language=language,
        public=public,
        instant_delete=instant_delete,
        image_embed=image_embed,
        expiration=expiration,
        encrypted=encrypted,
        password=password,
        editors=editors
    )


def get_document(document_id: str, *, password: str = None, api_token: str = None) -> Document:
    """
    Gets document from https://imperialb.in
    GET https://imperialb.in/api/document/:documentID
    :param document_id: the id associated with the imperialbin document
    :param password: the password if a document is encrypted
    :param api_token: the API token linked with your imperial account
    """
    return Imperial(api_token).get_document(document_id, password=password)


def edit_document(content: str, document_id: str, *, api_token: str = None) -> Document:
    """
    Edits document content on https://imperialb.in
    PATCH https://imperialb.in/api/document
    :param content: the text content to store on imperialbin
    :param document_id: the id associated with the imperialbin document
    :param api_token: the API token linked with your imperial account
    """
    return Imperial(api_token).edit_document(content=content, document_id=document_id)


def delete_document(document_id: str, *, api_token: str = None) -> None:
    """
    Deletes document from https://imperialb.in
    DELETE https://imperialb.in/api/document/:documentID
    :param document_id: the id associated with the imperialbin document
    :param api_token: the API token linked with your imperial account
    """
    Imperial(api_token).delete_document(document_id=document_id)


def verify(api_token: str = None) -> None:
    """
    Validate API token from https://imperialb.in
    GET https://imperialb.in/api/checkApiToken/:apiToken
    :param api_token: the API token linked with your imperial account
    """
    # p.s. `api_token` isn't required because it can be set by an environment variable :)
    Imperial(api_token).verify()


def purge_documents(api_token: str = None) -> int:
    """
    Deletes all documents created by an API token
    DELETE https://imperialb.in/api/purgeDocuments
    :param api_token: the API token linked with your imperial account
    :return: number of accounts deleted
    """
    return Imperial(api_token).purge_documents()
