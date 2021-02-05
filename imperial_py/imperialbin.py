__title__ = "Imperialb.in simple API wrapper"
__author__ = "Hexiro"

from re import compile
from os import environ
from datetime import datetime
from json.decoder import JSONDecodeError

import requests
from requests import Response


pattern = compile(r"(?<!^)(?<![A-Z])(?=[A-Z])")


# helper functions
def compose_json(_post: Response):
    """
    `compose_json` makes sure the rest of the function has dictionary regardless of failure or not.
    :param _post: python3 requests POST method (type: Response).
    :return: ImperialBin API response (type: dict).
    """
    try:
        return _post.json()
    except JSONDecodeError:  # maybe this could be better checking status codes? would have to look into that more
        return {"success": False}


def compose_snake_case(_dict: dict):
    """
    `compose_snake_case` converts the camelCase of the API response json keys to snake_case.
    (snake_case is more pythonic and is just what I prefer)
    :param _dict: ImperialBin API response (type: dict).
    :return: ImperialBin snake_case API response (type: dict).
    """
    snake_dict = {}
    for key, value in _dict.items():
        if key.islower():
            snake_dict[key] = value
        else:
            snake_dict[pattern.sub("_", key).lower()] = value
    return snake_dict


class Imperial:

    def __init__(self, api_token=None):
        """
        :param api_token: ImperialBin API token (type: str).
        15 requests max every 15 minutes; unlimited with an api token.
        """
        self.api_url = "https://imperialb.in/api"
        self.api_token = api_token
        path_token = environ.get("IMPERIAL-TOKEN")
        if not self.api_token and path_token:
            self.api_token = path_token

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
        if self.api_token:
            headers = {
                "authorization": self.api_token
            }
            payload = {
                "code": code,
                "longerUrls": longer_urls,
                "instantDelete": instant_delete,
                "imageEmbed": image_embed,
                "expiration": expiration
            }
        else:
            headers = {}
            payload = {
                "code": code
            }
        json = compose_snake_case(compose_json(requests.post("%s/postCode" % self.api_url, json=payload, headers=headers)))
        if "expires_in" in json:
            json["expires_in"] = datetime.strptime(json["expires_in"], "%Y-%m-%dT%H:%M:%S.%fZ")
        return json

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
        if self.api_token:
            headers = {
                "authorization": self.api_token
            }
        else:
            headers = {}
        if "/" in document_id:  # url passed
            document_id = document_id.split("/")[-1]
        return compose_snake_case(compose_json(requests.get("%s/getCode/%s" % (self.api_url, document_id), headers=headers)))

    def verify(self):
        """
        Validate API token from https://imperialb.in
        GET https://imperialb.in/api/checkApiToken/:apiToken
        :return: ImperialBin API response (type: dict).
        """
        if not isinstance(self.api_token, str):
            return {"success": False, "message": "No token to verify!"}
        if not self.api_token.startswith("IMPERIAL-") or len(self.api_token) != 45:
            # save imperialbin bandwidth by catching the error for them
            return {"success": False, "message": "API token is invalid!"}
        return compose_snake_case(compose_json(requests.get("%s/checkApiToken/%s" % (self.api_url, self.api_token), headers={
            "authorization": self.api_token
        })))


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
