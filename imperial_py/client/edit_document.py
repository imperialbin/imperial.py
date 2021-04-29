from .request import request
from ..utils.checks import ensure_code, ensure_document_id
from ..utils.hostname import https


def edit_document(code: str, document_id: str, api_token: str = None, password: str = None):
    """
    Edits document code on https://imperialb.in
    PATCH https://imperialb.in/api/document
    :param code: Code from any programming language, capped at 512KB per request (type: str).
    :param document_id: ImperialBin Document ID.
    :param api_token: ImperialBin API token
    :param password: ImperialBin Document password
    :return: ImperialBin API response (type: dict).
    """
    ensure_code(code)
    ensure_document_id(document_id)

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
