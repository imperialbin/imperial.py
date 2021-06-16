from .request import request
from ..checks import ensure_content, ensure_document_id, ensure_api_token
from ..utils import https


def edit_document(content: str, document_id: str, *, api_token: str = None) -> dict:
    """
    Edits document content on https://imperialb.in
    PATCH https://imperialb.in/api/document
    :param content: the text content to store on imperialbin
    :param document_id: the id associated with the imperialbin document
    :param api_token: the API token linked with your imperial account
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
