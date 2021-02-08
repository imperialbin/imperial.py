__title__ = "Imperialb.in simple API wrapper"
__author__ = "Hexiro"

from re import match
from re import compile
from os import environ
from datetime import datetime

import requests

from imperial_py.helpers import compose_snake_case

api_token_regex = compile(r"^IMPERIAL-[a-zA-Z\d]{8}(-[a-zA-Z\d]{4}){3}-[a-zA-Z\d]{12}$")


class Imperial:

    def __init__(self, api_token=None):
        """
        :param api_token: ImperialBin API token (type: str).
        15 requests max every 15 minutes; unlimited with an api token.
        """
        self.document_url = "https://imperialb.in/api/document/"
        self.api_url = "https://imperialb.in/api/"
        self.api_token = api_token
        path_token = environ.get("IMPERIAL-TOKEN")
        if not self.api_token and path_token:
            self.api_token = path_token
        self.session = requests.Session()
        if self.api_token:
            self.session.headers.update({
                "authorization": self.api_token
            })

    def post_code(self, code: str, longer_urls=False, instant_delete=False, image_embed=False, expiration=5):
        """
        Uploads code to https://imperialb.in
        POST https://imperialb.in/api/postCode
        :param code: Code from any programming language, capped at 512KB per request (type: str).
        :param longer_urls: increases the length of the random document id by 3x (type: boolean).
        :param instant_delete: makes the paste delete on its first visit (type: boolean).
        :param image_embed: changes embed content from text to an image (type: boolean; overwritten by instant_delete)
        :param expiration: sets the number of days before the paste deletes (type: str/int; overwritten by instant_delete)
        :return: ImperialBin API response (type: dict).
        """
        if not isinstance(code, str):
            # save imperialbin bandwidth by catching the error for them
            return {"success": False, "message": "You need to post code! No code was submitted!"}
        response_dict = compose_snake_case(self.session.post(self.document_url, json={
            "code": code,
            "longerUrls": longer_urls,
            "instantDelete": instant_delete,
            "imageEmbed": image_embed,
            "expiration": expiration
        }))
        if "expires_in" in response_dict:
            response_dict["expires_in"] = datetime.strptime(response_dict["expires_in"], "%Y-%m-%dT%H:%M:%S.%fZ")
        return response_dict

    def get_code(self, document_id: str):
        """
        Gets code from https://imperialb.in
        GET https://imperialb.in/api/getCode/:documentID
        :param document_id: ImperialBin Document ID (type: str).
        :return: ImperialBin API response (type: dict).
        """
        if not isinstance(document_id, str):
            # save imperialbin bandwidth by catching the error for them
            return {"success": False, "message": "We couldn't find that document!"}
        if "/" in document_id:  # url passed
            document_id = document_id.split("/")[-1]
        return compose_snake_case(self.session.get(self.document_url + document_id))

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


def post_code(code: str, api_token=None, longer_urls=False, instant_delete=False, image_embed=False, expiration=5):
    """
    Uploads code to https://imperialb.in
    POST https://imperialb.in/api/postCode
    :param code: Code from any programming language, capped at 512KB per request (type: str).
    :param api_token: ImperialBin API token (type: str).
    :param longer_urls: increases the length of the random document id by 3x (type: boolean).
    :param instant_delete: makes the paste delete on its first visit (type: boolean).
    :param image_embed: changes embed content from text to an image (type: boolean; overwritten by instant_delete)
    :param expiration: sets the number of days before the paste deletes (type: str/int; overwritten by instant_delete)
    :return: ImperialBin API response (type: dict).
    """
    return Imperial(api_token).post_code(code, longer_urls, instant_delete, image_embed, expiration)


def get_code(document_id: str, api_token=None):
    """
    Gets code from https://imperialb.in
    GET https://imperialb.in/api/getCode/:documentID
    :param document_id: ImperialBin Document ID (type: str).
    :param api_token: ImperialBin API token (type: str).
    :return: ImperialBin API response (type: dict).
    """
    return Imperial(api_token).get_code(document_id)


def verify(api_token):
    """
    Validate API token from https://imperialb.in
    GET https://imperialb.in/api/checkApiToken/:apiToken
    :param api_token: ImperialBin API token (type: str).
    :return: ImperialBin API response (type: dict).
    """
    return Imperial(api_token).verify()
