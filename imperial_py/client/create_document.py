from .request import request
from ..checks import ensure_content
from ..utils import https


def create_document(content: str, *,
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
    :param content: Code from any programming language, capped at 512KB per request.
    :param api_token: ImperialBin API token
    :param longer_urls: increases the length of the random document id by 3x.
    :param language: the programming language of the code (or plain)
    :param instant_delete: makes the paste delete on its first visit.
    :param image_embed: changes embed content from text to an image (overwritten by instant_delete)
    :param expiration: sets the number of days before the paste deletes (overwritten by instant_delete)
    :param encrypted: whether the document gets encrypted or not
    :param password: the document password (only if document is encrypted)123
    :return: ImperialBin API response (type: dict).
    """
    ensure_content(content)

    return request(
        method="POST",
        url=https.imperialbin / "api" / "document",
        # I can't wait to replace `code` with `content` here
        code=content,
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
