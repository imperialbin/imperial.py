from .request import request
from ..checks import ensure_api_token
from ..utils import https


def purge_documents(api_token: str) -> dict:
    """
    Deletes all documents associated with an account (by API token)
    DELETE https://imperialb.in/api/purgeDocuments
    :param api_token: ImperialBin API token
    :return: ImperialBin API response (type: dict).
    """
    ensure_api_token(api_token)

    return request(
        method="DELETE",
        url=https.imperialbin / "api" / "purgeDocuments",
        api_token=api_token
    )
