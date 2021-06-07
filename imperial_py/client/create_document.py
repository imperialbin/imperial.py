from .request import request
from ..checks import ensure_content, ensure_api_token
from ..utils import https


def create_document(content: str, *,
                    api_token: str = None,
                    short_urls: bool = False,
                    longer_urls: bool = False,
                    language: str = None,
                    public: bool = False,
                    instant_delete: bool = False,
                    image_embed: bool = False,
                    expiration: int = 5,
                    encrypted: bool = False,
                    password: str = None,
                    editors: list[str] = None):
    """
    Uploads code to https://imperialb.in
    POST https://imperialb.in/api/document
    :param content: Code from any programming language, capped at 512KB per request.
    :param api_token: ImperialBin API token
    :param short_urls: increases the length of the random document id from 8 to 4
    :param longer_urls: increases the length of the random document id from 8 to 26
    :param language: the programming language of the code (or plain)
    :param public: makes the document publicly viewable on an imperial public page
    :param instant_delete: makes the paste delete on its first visit.
    :param image_embed: changes embed content from text to an image (overwritten by instant_delete)
    :param expiration: sets the number of days before the paste deletes (overwritten by instant_delete)
    :param encrypted: whether the document gets encrypted or not
    :param password: the document password (only if document is encrypted)
    :param editors: list of users who're allowed to edit a document
    :return: ImperialBin API response (type: dict).
    """
    ensure_content(content)
    if api_token:
        ensure_api_token(api_token)

    return request(
        method="POST",
        url=https.imperialbin / "api" / "document",
        # I can't wait to replace `code` with `content` here
        code=content,
        api_token=api_token,
        # optional
        short_urls=short_urls,
        longer_urls=longer_urls,
        language=language,
        public=public,
        instant_delete=instant_delete,
        image_embed=image_embed,
        expiration=expiration,
        encrypted=encrypted,
        password=password,
        editors=editors
    )
