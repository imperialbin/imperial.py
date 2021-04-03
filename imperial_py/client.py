import re

import requests

from .utils import parse_kwargs, ensure_json, json_modifications

api_token_regex = re.compile(r"^IMPERIAL-[a-zA-Z\d]{8}(-[a-zA-Z\d]{4}){3}-[a-zA-Z\d]{12}$")
document_url = "https://imperialb.in/api/document/"
api_token_url = "https://imperialb.in/api/checkApiToken/"


def request(*, method, url, api_token=None, **kwargs):
    resp = requests.request(method=method, url=url, **parse_kwargs(method, kwargs), headers={"authorization": api_token})
    json = ensure_json(resp)
    if not json["success"]:
        return json
    return json_modifications(json)


def create(code,
           api_token=None,
           longer_urls=False,
           instant_delete=False,
           image_embed=False,
           expiration=5,
           encrypted=False,
           password=None):
    """
    Uploads code to https://imperialb.in
    POST https://imperialb.in/api/document
    :type api_token: str
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
    :param password: the document password (only if document is encrypted)123
    :type password: str
    :return: ImperialBin API response (type: dict).
    """
    if not isinstance(code, str):
        return {"success": False,
                "message": "You need to post code! No code was submitted!"}

    return request(
        method="POST",
        url=document_url,
        **locals()
    )


def get(document_id, api_token=None, password=None):
    """
    Gets code from https://imperialb.in
    GET https://imperialb.in/api/document/:documentID
    :type api_token: str
    :param document_id: ImperialBin Document ID.
    :type document_id: str
    :return: ImperialBin API response (type: dict).
    :param password: ImperialBin Document password
    :type password: str
    """
    if not isinstance(document_id, str):
        return {"success": False,
                "message": "We couldn't find that document!"}

    return request(
        method="GET",
        url=(document_url + document_id),
        api_token=api_token,
        password=password
    )


def edit(code, document_id, api_token=None, password=None):
    """
    Edits document code on https://imperialb.in
    PATCH https://imperialb.in/api/document
    :type api_token: str
    :param code: Code from any programming language, capped at 512KB per request (type: str).
    :type code: str
    :param document_id: ImperialBin Document ID.
    :type document_id: str
    :param password: ImperialBin Document password
    :type password: str
    :return: ImperialBin API response (type: dict).
    """
    return request(
        method="PATCH",
        url=document_url,
        api_token=api_token,
        password=password,
        code=code,
        # for some reason this has a different name :/
        document=document_id,
    )


def delete(document_id, api_token=None, password=None):
    return request(
        method="DELETE",
        url=(document_url + document_id),
        api_token=api_token,
        password=password
    )


def verify(api_token):
    """
    Validate API token from https://imperialb.in
    GET https://imperialb.in/api/checkApiToken/:apiToken
    :return: ImperialBin API response (type: dict).
    """
    if isinstance(api_token, str):
        return {"success": False,
                "message": "No token to verify!"}

    if not re.match(api_token_regex, api_token):
        return {"success": False,
                "message": "API token is invalid!"}

    return request(
        method="GET",
        url=(api_token_url + api_token)
    )
