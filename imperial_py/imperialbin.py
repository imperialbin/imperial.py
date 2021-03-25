__title__ = "Imperialb.in simple API wrapper"
__author__ = "Hexiro"

from re import match
from re import compile
from os import environ

import requests

from imperial_py.utils import compose_snake_case, format_datetime_expiry, parse_document_id


api_token_regex = compile(r"^IMPERIAL-[a-zA-Z\d]{8}(-[a-zA-Z\d]{4}){3}-[a-zA-Z\d]{12}$")


class Imperial:

    def __init__(self, api_token=None):
        """
        :param api_token: ImperialBin API token
        :type api_token: str
        15 requests max every 15 minutes; unlimited with an api token.
        """
        self.session = requests.Session()
        self.document_url = "https://imperialb.in/api/document/"
        self.api_url = "https://imperialb.in/api/"
        self.api_token = api_token
        path_token = environ.get("IMPERIAL-TOKEN")
        # set token overrides path set token
        if not self.api_token and path_token:
            self.api_token = path_token
        if self.api_token:
            self.session.headers.update({
                "authorization": self.api_token
            })

    def create_document(self,
                        code,
                        longer_urls=False,
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
        if not isinstance(code, str):
            # save imperialbin bandwidth by catching the error for them
            return {"success": False, "message": "You need to post code! No code was submitted!"}
        return format_datetime_expiry(compose_snake_case(self.session.post(self.document_url, json={
            "code": code,
            "longerUrls": longer_urls,
            "instantDelete": instant_delete,
            "imageEmbed": image_embed,
            "expiration": expiration,
            "encrypted": encrypted,
            "password": password
        })))

    def get_document(self, document_id):
        """
        Gets code from https://imperialb.in
        GET https://imperialb.in/api/document/:documentID
        :param document_id: ImperialBin Document ID.
        :type document_id: str
        :return: ImperialBin API response (type: dict).
        """
        if not isinstance(document_id, str):
            # save imperialbin bandwidth by catching the error for them
            return {"success": False, "message": "We couldn't find that document!"}
        return compose_snake_case(self.session.get(self.document_url + parse_document_id(document_id)))

    def edit_document(self, code, document_id):
        """
        Edits document code on https://imperialb.in
        PATCH https://imperialb.in/api/document
        :param code: Code from any programming language, capped at 512KB per request (type: str).
        :type code: str
        :param document_id: ImperialBin Document ID.
        :type document_id: str
        :return: ImperialBin API response (type: dict).
        """
        return format_datetime_expiry(compose_snake_case(self.session.patch(self.document_url, json={
            "newCode": code,
            "document": parse_document_id(document_id)
        })))

    def verify(self):
        """
        Validate API token from https://imperialb.in
        GET https://imperialb.in/api/checkApiToken/:apiToken
        :return: ImperialBin API response (type: dict).
        """
        if not isinstance(self.api_token, str):
            return {"success": False, "message": "No token to verify!"}
        if not match(api_token_regex, self.api_token):
            # save imperialbin bandwidth by catching the error for them
            return {"success": False, "message": "API token is invalid!"}
        return compose_snake_case(self.session.get(self.api_url + "checkApiToken/" + self.api_token))


# shorthand functions


def create_document(code,
                    api_token=None,
                    longer_urls=False,
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
    return Imperial(api_token).create_document(code, longer_urls, instant_delete, image_embed, expiration, encrypted, password)


def get_document(document_id, api_token=None):
    """
    Gets code from https://imperialb.in
    GET https://imperialb.in/api/getCode/:documentID
    :param document_id: ImperialBin Document ID.
    :type document_id: str
    :param api_token: ImperialBin API token.
    :type api_token: str
    :return: ImperialBin API response (type: dict).
    """
    return Imperial(api_token).get_document(document_id)


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
    return Imperial(api_token).edit_document(code, document_id)


def verify(api_token=None):
    """
    Validate API token from https://imperialb.in
    GET https://imperialb.in/api/checkApiToken/:apiToken
    :param api_token: ImperialBin API token.
    :type api_token: str
    :return: ImperialBin API response (type: dict).
    """
    # p.s. this isn't required because api_token can be set by environment variable :)
    return Imperial(api_token).verify()

