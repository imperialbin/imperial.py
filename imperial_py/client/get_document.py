from .request import request
from ..utils.checks import ensure_document_id
from ..utils.hostname import https


def get_document(document_id: str, *, api_token: str = None, password: str = None):
    """
    Gets code from https://imperialb.in
    GET https://imperialb.in/api/document/:documentID
    :param document_id: ImperialBin Document ID.
    :param api_token: ImperialBin API token
    :param password: ImperialBin Document password
    :return: ImperialBin API response (type: dict).
    """
    ensure_document_id(document_id)

    return request(
        method="GET",
        url=https.imperialbin / "api" / "document" / document_id,
        api_token=api_token,
        # optional
        password=password
    )
