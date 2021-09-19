from .request import request
from ..checks import ensure_document_id, ensure_api_token
from ..utils import https


def get_document(document_id: str, *, password: str = None, api_token: str = None) -> dict:
    """
    Gets document from https://imperialb.in
    GET https://imperialb.in/api/document/:documentID
    :param document_id: the id associated with the imperialbin document
    :param password: the password if a document is encrypted
    :param api_token: the API token linked with your imperial account
    """
    ensure_document_id(document_id)
    if api_token:
        ensure_api_token(api_token)

    return request(
        method="GET",
        url=https.imperialbin / "api" / "document" / document_id,
        api_token=api_token,
        # optional
        password=password
    )
