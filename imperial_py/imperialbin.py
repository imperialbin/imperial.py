__title__ = "Imperialb.in simple API wrapper"
__author__ = "Hexiro"

import os
from typing import List

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
    def api_token(self):
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
                        editors: List[str] = None):
        """
        Uploads code to https://imperialb.in
        POST https://imperialb.in/api/document
        :param content: Code from any programming language, capped at 512KB per request.
        :param short_urls: increases the length of the random document id from 8 to 4
        :param longer_urls: increases the length of the random document id from 8 to 26
        :param language: the programming language of the code (or plain)
        :param public: makes the document publicly viewable on an imperial public page
        :param instant_delete: makes the paste delete on its first visit.
        :param image_embed: changes embed content from text to an image (overwritten by instant_delete)
        :param expiration: sets the number of days before the paste deletes (overwritten by instant_delete)
        :param encrypted: whether the document gets encrypted or not
        :param password: the document password (only if document is encrypted)
        :param editors: list of users who're allowed to edit a document
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

    def get_document(self, document_id: str, *, password: str = None):
        """
        Gets code from https://imperialb.in
        GET https://imperialb.in/api/document/:documentID
        :param document_id: ImperialBin Document ID.
        :param password: ImperialBin Document password
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

    def edit_document(self, content: str, document_id: str):
        """
        Edits document code on https://imperialb.in
        PATCH https://imperialb.in/api/document
        :param content: Code from any programming language, capped at 512KB per request (type: str).
        :param document_id: ImperialBin Document ID.
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

    def delete_document(self, document_id: str):
        """
        Deletes document from https://imperialb.in
        DELETE https://imperialb.in/api/document/:documentID
        :param document_id: ImperialBin Document ID.
        """
        client.delete_document(document_id, api_token=self.api_token)

    def verify(self):
        """
        Validate API token from https://imperialb.in
        GET https://imperialb.in/api/checkApiToken/:apiToken
        :rtype: None
        """
        client.check_api_token(self.api_token)

    def purge_documents(self):
        """
        Deletes all documents associated with an account (by API token)
        DELETE https://imperialb.in/api/purgeDocuments
        :return: number of accounts deleted
        :rtype: int
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
                    editors: List[str] = None):
    """
    Uploads code to https://imperialb.in
    POST https://imperialb.in/api/postCode
    :param content: Code from any programming language, capped at 512KB per request.
    :param api_token: ImperialBin API token
    :param short_urls: increases the length of the random document id from 8 to 4
    :param longer_urls: increases the length of the random document id from 8 to 26
    :param language: the programming language of the code (or plain)
    :param public: makes the document publicly viewable on an imperial public page
    :param instant_delete: makes the paste delete on its first visit.
    :param image_embed: changes embed content from text to an image (overwritten by instant_delete)
    :param expiration: sets the number of days before the paste deletes (overwritten by instant_delete)
    :param encrypted: whether the document gets encrypted or not
    :param password: the document password (only if document is encrypted)
    :param editors: list of users who're allowed to edit a document
    :return: ImperialBin API response (type: dict).
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


def get_document(document_id: str, *, password: str = None, api_token: str = None):
    """
    Gets code from https://imperialb.in
    GET https://imperialb.in/api/getCode/:documentID
    :param document_id: ImperialBin Document ID.
    :param api_token: ImperialBin API token.
    :param password: ImperialBin Document password.
    :return: ImperialBin API response (type: dict).
    """
    return Imperial(api_token).get_document(document_id, password=password)


def edit_document(content: str, document_id: str, *, api_token: str = None):
    """
    Edits document code on https://imperialb.in
    PATCH https://imperialb.in/api/document
    :param content: Code from any programming language, capped at 512KB per request.
    :param document_id: ImperialBin Document ID.
    :param api_token: ImperialBin API token.
    :return: ImperialBin API response (type: dict).
    """
    return Imperial(api_token).edit_document(content=content, document_id=document_id)


def delete_document(document_id: str, *, api_token: str = None):
    """
    Deletes document from https://imperialb.in
    DELETE https://imperialb.in/api/document/:documentID
    :param document_id: ImperialBin Document ID.
    :param api_token: ImperialBin API token.
    :rtype: None
    """
    Imperial(api_token).delete_document(document_id=document_id)


def verify(api_token: str = None):
    """
    Validate API token from https://imperialb.in
    GET https://imperialb.in/api/checkApiToken/:apiToken
    :param api_token: ImperialBin API token.
    :rtype: None
    """
    # p.s. `api_token` isn't required because it can be set by an environment variable :)
    Imperial(api_token).verify()


def purge_documents(api_token: str = None):
    """
    Deletes all documents associated with an account (by API token)
    DELETE https://imperialb.in/api/purgeDocuments
    :param api_token: ImperialBin API token.
    :return: number of accounts deleted
    :rtype: int
    """
    return Imperial(api_token).purge_documents()
