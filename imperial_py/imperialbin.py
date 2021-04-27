__title__ = "Imperialb.in simple API wrapper"
__author__ = "Hexiro"

import os

from .utils import client
from .document import Document


class Imperial:

    def __init__(self, api_token: str = None):
        """
        :param api_token: ImperialBin API token
        15 requests max every 15 minutes; unlimited with an api token.
        """
        # set token overrides path set token
        self.api_token = api_token or os.environ.get("IMPERIAL_TOKEN")

    def create_document(self,
                        code: str,
                        longer_urls: bool = False,
                        language: str = None,
                        instant_delete: bool = False,
                        image_embed: bool = False,
                        expiration: int = 5,
                        encrypted: bool = False,
                        password: str = None):
        """
        Uploads code to https://imperialb.in
        POST https://imperialb.in/api/document
        :param code: Code from any programming language, capped at 512KB per request.
        :param longer_urls: increases the length of the random document id by 3x.
        :param language: the programming language of the code (or plain)
        :param instant_delete: makes the paste delete on its first visit.
        :param image_embed: changes embed content from text to an image (overwritten by instant_delete)
        :param expiration: sets the number of days before the paste deletes (overwritten by instant_delete)
        :param encrypted: whether the document gets encrypted or not
        :param password: the document password (only if document is encrypted)
        """

        resp = client.create(
            code=code,
            longer_urls=longer_urls,
            language=language,
            instant_delete=instant_delete,
            image_embed=image_embed,
            expiration=expiration,
            encrypted=encrypted,
            password=password,
            api_token=self.api_token
        )

        return Document(
            document_dict=resp,
            code=code,
            api_token=self.api_token
        )

    def get_document(self, document_id: str, password: str = None):
        """
        Gets code from https://imperialb.in
        GET https://imperialb.in/api/document/:documentID
        :param document_id: ImperialBin Document ID.
        :param password: ImperialBin Document password
        """
        return Document(
            document_dict=client.get(document_id=document_id, password=password, api_token=self.api_token),
            api_token=self.api_token
        )

    def edit_document(self, code: str, document_id: str):
        """
        Edits document code on https://imperialb.in
        PATCH https://imperialb.in/api/document
        :param code: Code from any programming language, capped at 512KB per request (type: str).
        :param document_id: ImperialBin Document ID.
        """
        return Document(
            document_dict=client.edit(code=code, document_id=document_id, api_token=self.api_token),
            code=code,
            api_token=self.api_token
        )

    def delete_document(self, document_id: str, password: str = None):
        """
        Deletes document from https://imperialb.in
        DELETE https://imperialb.in/api/document/:documentID
        :param document_id: ImperialBin Document ID.
        :param password: ImperialBin Document password
        """
        return client.delete(document_id, password=password, api_token=self.api_token)

    def verify(self):
        """
        Validate API token from https://imperialb.in
        GET https://imperialb.in/api/checkApiToken/:apiToken
        :return: ImperialBin API response (type: dict).
        """
        return client.verify(self.api_token)


# shorthand functions


def create_document(code: str,
                    api_token: str = None,
                    longer_urls: bool = False,
                    language: str = None,
                    instant_delete: bool = False,
                    image_embed: bool = False,
                    expiration: int = 5,
                    encrypted: bool = False,
                    password: str = None):
    """
    Uploads code to https://imperialb.in
    POST https://imperialb.in/api/postCode
    :param code: Code from any programming language, capped at 512KB per request.
    :param api_token: ImperialBin API token
    :param longer_urls: increases the length of the random document id by 3x.
    :param language: the programming language of the code (or plain)
    :param instant_delete: makes the paste delete on its first visit.
    :param image_embed: changes embed content from text to an image (overwritten by instant_delete)
    :param expiration: sets the number of days before the paste deletes (overwritten by instant_delete)
    :param encrypted: whether the document gets encrypted or not
    :param password: the document password (only if document is encrypted)
    :return: ImperialBin API response (type: dict).
    """
    return Imperial(api_token).create_document(
        code=code,
        longer_urls=longer_urls,
        language=language,
        instant_delete=instant_delete,
        image_embed=image_embed,
        expiration=expiration,
        encrypted=encrypted,
        password=password
    )


def get_document(document_id: str, password: str = None, api_token: str = None):
    """
    Gets code from https://imperialb.in
    GET https://imperialb.in/api/getCode/:documentID
    :param document_id: ImperialBin Document ID.
    :param api_token: ImperialBin API token.
    :param password: ImperialBin Document password.
    :return: ImperialBin API response (type: dict).
    """
    return Imperial(api_token).get_document(document_id, password=password)


def edit_document(code: str, document_id: str, api_token: str = None):
    """
    Edits document code on https://imperialb.in
    PATCH https://imperialb.in/api/document
    :param code: Code from any programming language, capped at 512KB per request.
    :param document_id: ImperialBin Document ID.
    :param api_token: ImperialBin API token.
    :return: ImperialBin API response (type: dict).
    """
    return Imperial(api_token).edit_document(code=code, document_id=document_id)


def delete_document(document_id: str, password: str = None, api_token: str = None):
    """
    Deletes document from https://imperialb.in
    DELETE https://imperialb.in/api/document/:documentID
    :param document_id: ImperialBin Document ID.
    :param password: ImperialBin Document password
    :param api_token: ImperialBin API token.
    :return: ImperialBin API response (type: dict).
    """
    return Imperial(api_token).delete_document(document_id=document_id, password=password)


def verify(api_token: str = None):
    """
    Validate API token from https://imperialb.in
    GET https://imperialb.in/api/checkApiToken/:apiToken
    :param api_token: ImperialBin API token.
    :return: ImperialBin API response (type: dict).
    """
    # p.s. `api_token` isn't required because it can be set by an environment variable :)
    return Imperial(api_token).verify()
