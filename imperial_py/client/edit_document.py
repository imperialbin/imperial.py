from .request import request
from ..utils.checks import ensure_content, ensure_document_id
from ..utils.hostname import https


def edit_document(content: str, document_id: str, api_token: str = None):
    """
    Edits document code on https://imperialb.in
    PATCH https://imperialb.in/api/document
    :param content: Code from any programming language, capped at 512KB per request (type: str).
    :param document_id: ImperialBin Document ID.
    :param api_token: ImperialBin API token
    :return: ImperialBin API response (type: dict).
    """
    ensure_content(content)
    ensure_document_id(document_id)

    return request(
        method="PATCH",
        url=https.imperialbin / "api" / "document",
        api_token=api_token,
        code=content,
        # for some reason this has a different name :/
        document=document_id,
    )
