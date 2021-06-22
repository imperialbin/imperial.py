from typing import List

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
                    editors: List[str] = None) -> dict:
    """
    Uploads content to https://imperialb.in
    POST https://imperialb.in/api/document
    :param content: the text content to store on imperialbin
    :param api_token: the API token linked with your imperial account
    :param short_urls: creates 4 character URLs instead of 8
    :param longer_urls: creates 26 character URLs instead of 8
    :param language: the programming language of the content (or plain text)
    :param public: makes the document publicly viewable on the imperial public page
    :param instant_delete: instantly deletes the document after being viewed once.
    :param image_embed: have a sneak peak with an image through Open Graph embeds
    :param expiration: sets the number of days before the paste deletes (overwritten by instant_delete)
    :param encrypted: encrypts the document with a password and aes256 encryption
    :param password: the password if a document is encrypted
    :param editors: a list of users who are allowed to edit a document
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
