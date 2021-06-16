from .request import request
from ..checks import ensure_api_token
from ..utils import https


def purge_documents(api_token: str) -> dict:
    """
    Deletes all documents created by an API token
    DELETE https://imperialb.in/api/purgeDocuments
    :param api_token: the API token linked with your imperial account
    """
    ensure_api_token(api_token)

    return request(
        method="DELETE",
        url=https.imperialbin / "api" / "purgeDocuments",
        api_token=api_token
    )
