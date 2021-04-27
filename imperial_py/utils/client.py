import requests

# utils
from .hostname import https
from .json_parser import parse_body, ensure_json, json_modifications
from .param_checks import check_code, check_document_id, check_api_token, check_params


def request(*, method: str, url: str, api_token: str = None, **kwargs):
    # check_params is what throws the errors, so parse_body assumes everything is fine
    check_params(method, api_token, **kwargs)
    resp = requests.request(
        method=method,
        url=url,
        headers={"authorization": api_token} if api_token else None,
        # this .copy() isn't necessary it's just to prevent future bugs because we pop from it
        **parse_body(method, kwargs.copy())
    )
    json = ensure_json(resp)
    if not json["success"]:
        return json
    return json_modifications(json)


def create(code: str,
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
    POST https://imperialb.in/api/document
    :param code: Code from any programming language, capped at 512KB per request.
    :param longer_urls: increases the length of the random document id by 3x.
    :param language: the programming language of the code (or plain)
    :param instant_delete: makes the paste delete on its first visit.
    :param image_embed: changes embed content from text to an image (overwritten by instant_delete)
    :param expiration: sets the number of days before the paste deletes (overwritten by instant_delete)
    :param encrypted: whether the document gets encrypted or not
    :param password: the document password (only if document is encrypted)123
    :return: ImperialBin API response (type: dict).
    """
    check_code(code)

    return request(
        method="POST",
        url=https.imperialbin / "api" / "document",
        code=code,
        api_token=api_token,
        # optional
        longer_urls=longer_urls,
        language=language,
        instant_delete=instant_delete,
        image_embed=image_embed,
        expiration=expiration,
        encrypted=encrypted,
        password=password,
    )


def get(document_id: str, api_token: str = None, password: str = None):
    """
    Gets code from https://imperialb.in
    GET https://imperialb.in/api/document/:documentID
    :param document_id: ImperialBin Document ID.
    :param password: ImperialBin Document password
    :return: ImperialBin API response (type: dict).
    """
    check_document_id(document_id)

    return request(
        method="GET",
        url=https.imperialbin / "api" / "document" / document_id,
        api_token=api_token,
        # optional
        password=password
    )


def edit(code: str, document_id: str, api_token: str = None, password: str = None):
    """
    Edits document code on https://imperialb.in
    PATCH https://imperialb.in/api/document
    :param code: Code from any programming language, capped at 512KB per request (type: str).
    :param document_id: ImperialBin Document ID.
    :param password: ImperialBin Document password
    :return: ImperialBin API response (type: dict).
    """
    check_code(code)
    check_document_id(document_id)

    return request(
        method="PATCH",
        url=https.imperialbin / "api" / "document",
        api_token=api_token,
        code=code,
        # for some reason this has a different name :/
        document=document_id,
        # optional
        password=password,
    )


def delete(document_id: str, api_token: str = None, password: str = None):
    check_document_id(document_id)

    return request(
        method="DELETE",
        url=https.imperialbin / "api" / "document" / document_id,
        api_token=api_token,
        password=password
    )


def verify(api_token: str):
    """
    Validate API token from https://imperialb.in
    GET https://imperialb.in/api/checkApiToken/:apiToken
    :return: ImperialBin API response (type: dict).
    """
    check_api_token(api_token)

    return request(
        method="GET",
        url=https.imperialbin / "api" / "checkApiToken" / api_token
    )
