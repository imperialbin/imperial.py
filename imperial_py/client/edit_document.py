from .request import request
from ..checks import ensure_content, ensure_document_id, ensure_api_token
from ..utils import https


def edit_document(content: str, document_id: str, *, api_token: str = None) -> dict:
    """
    Edits document code on https://imperialb.in
    PATCH https://imperialb.in/api/document
    :param content: Code from any programming language, capped at 512KB per request (type: str).
    :param document_id: ImperialBin Document ID.
    :param api_token: ImperialBin API token
    """
    ensure_content(content)
    ensure_document_id(document_id)
    if api_token:
        ensure_api_token(api_token)

    return request(
        method="PATCH",
        url=https.imperialbin / "api" / "document",
        api_token=api_token,
        code=content,
        # for some reason this has a different name :/
        document=document_id,
    )
