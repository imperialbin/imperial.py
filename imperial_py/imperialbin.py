__title__ = "Imperialb.in simple API wrapper"
__author__ = "Hexiro"

import os

from .utils import client
from .utils.json_parser import remove_self
from .document import Document


class Imperial:

    def __init__(self, api_token=None):
        """
        :param api_token: ImperialBin API token
        :type api_token: str
        15 requests max every 15 minutes; unlimited with an api token.
        """
        # set token overrides path set token
        self.api_token = api_token
        path_token = os.environ.get("IMPERIAL-TOKEN")
        if self.api_token is None and path_token:
            self.api_token = path_token

    def create_document(self,
                        code,
                        longer_urls=False,
                        language=None,
                        instant_delete=False,
                        image_embed=False,
                        expiration=5,
                        encrypted=False,
                        password=None):
        """
        Uploads code to https://imperialb.in
        POST https://imperialb.in/api/document
        :param code: Code from any programming language, capped at 512KB per request.
        :type code: str
        :param longer_urls: increases the length of the random document id by 3x.
        :type longer_urls: bool
        :param language: the programming language of the code (or plain)
        :type language: str
        :param instant_delete: makes the paste delete on its first visit.
        :type instant_delete: bool
        :param image_embed: changes embed content from text to an image (overwritten by instant_delete)
        :type image_embed: bool
        :param expiration: sets the number of days before the paste deletes (overwritten by instant_delete)
        :type expiration: int
        :param encrypted: whether the document gets encrypted or not
        :type encrypted: bool
        :param password: the document password (only if document is encrypted)
        :type password: str
        """

        return Document(
            document_dict=client.create(**remove_self(locals()), api_token=self.api_token),
            code=code,
            api_token=self.api_token
        )

    def get_document(self, document_id, password=None):
        """
        Gets code from https://imperialb.in
        GET https://imperialb.in/api/document/:documentID
        :param document_id: ImperialBin Document ID.
        :type document_id: str
        :param password: ImperialBin Document password
        :type password: str
        """
        return Document(
            document_dict=client.get(**remove_self(locals()), api_token=self.api_token),
            api_token=self.api_token
        )

    def edit_document(self, code, document_id):
        """
        Edits document code on https://imperialb.in
        PATCH https://imperialb.in/api/document
        :param code: Code from any programming language, capped at 512KB per request (type: str).
        :type code: str
        :param document_id: ImperialBin Document ID.
        :type document_id: str
        """
        return Document(
            document_dict=client.edit(**remove_self(locals()), api_token=self.api_token),
            code=code,
            api_token=self.api_token
        )

    def delete_document(self, document_id, password=None):
        """
        Deletes document from https://imperialb.in
        DELETE https://imperialb.in/api/document/:documentID
        :param document_id: ImperialBin Document ID.
        :type document_id: str
        :param password: ImperialBin Document password
        :type password: str
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


def create_document(code,
                    api_token=None,
                    longer_urls=False,
                    language=None,
                    instant_delete=False,
                    image_embed=False,
                    expiration=5,
                    encrypted=False,
                    password=None):
    """
    Uploads code to https://imperialb.in
    POST https://imperialb.in/api/postCode
    :param code: Code from any programming language, capped at 512KB per request.
    :type code: str
    :param api_token: ImperialBin API token
    :type api_token: str
    :param longer_urls: increases the length of the random document id by 3x.
    :type longer_urls: bool
    :param language: the programming language of the code (or plain)
    :type language: str
    :param instant_delete: makes the paste delete on its first visit.
    :type instant_delete: bool
    :param image_embed: changes embed content from text to an image (overwritten by instant_delete)
    :type image_embed: bool
    :param expiration: sets the number of days before the paste deletes (overwritten by instant_delete)
    :type expiration: int
    :param encrypted: whether the document gets encrypted or not
    :type encrypted: bool
    :param password: the document password (only if document is encrypted)
    :type password: str
    :return: ImperialBin API response (type: dict).
    """
    params = locals().copy()
    return Imperial(params.pop("api_token")).create_document(**params)


def get_document(document_id, api_token=None, password=None):
    """
    Gets code from https://imperialb.in
    GET https://imperialb.in/api/getCode/:documentID
    :param document_id: ImperialBin Document ID.
    :type document_id: str
    :param api_token: ImperialBin API token.
    :type api_token: str
    :param password: ImperialBin Document password.
    :type password: str
    :return: ImperialBin API response (type: dict).
    """
    params = locals().copy()
    return Imperial(params.pop("api_token")).get_document(**params)


def edit_document(code, document_id, api_token=None):
    """
    Edits document code on https://imperialb.in
    PATCH https://imperialb.in/api/document
    :param code: Code from any programming language, capped at 512KB per request.
    :type code: str
    :param document_id: ImperialBin Document ID.
    :type document_id: str
    :param api_token: ImperialBin API token.
    :type api_token: str
    :return: ImperialBin API response (type: dict).
    """
    params = locals().copy()
    return Imperial(params.pop("api_token")).edit_document(**params)


def delete_document(document_id, password=None, api_token=None):
    """
    Deletes document from https://imperialb.in
    DELETE https://imperialb.in/api/document/:documentID
    :param document_id: ImperialBin Document ID.
    :type document_id: str
    :param password: ImperialBin Document password
    :type password: str
    :param api_token: ImperialBin API token.
    :type api_token: str
    :return: ImperialBin API response (type: dict).
    """
    params = locals().copy()
    return Imperial(params.pop("api_token")).delete_document(**params)


def verify(api_token=None):
    """
    Validate API token from https://imperialb.in
    GET https://imperialb.in/api/checkApiToken/:apiToken
    :param api_token: ImperialBin API token.
    :type api_token: str
    :return: ImperialBin API response (type: dict).
    """
    # p.s. `api_token` isn't required because it can be set by an environment variable :)
    return Imperial(api_token).verify()

