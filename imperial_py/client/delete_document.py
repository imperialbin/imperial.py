from .request import request
from ..checks import ensure_document_id, ensure_api_token
from ..utils import https


def delete_document(document_id: str, *, api_token: str = None):
    """
    Deletes document on https://imperialb.in
    DELETE https://imperialb.in/api/document/:document_id
    :param document_id: ImperialBin Document ID.
    :param api_token: ImperialBin API token
    :return: ImperialBin API response (type: dict).
    """
    ensure_document_id(document_id)
    if api_token:
        ensure_api_token(api_token)

    return request(
        method="DELETE",
        url=https.imperialbin / "api" / "document" / document_id,
        api_token=api_token,
    )
