import re

from ..exceptions import ImperialError

api_token_regex = re.compile(r"^IMPERIAL-[a-zA-Z\d]{8}(-[a-zA-Z\d]{4}){3}-[a-zA-Z\d]{12}$")

__all__ = (
    "throw_if_invalid",
    "ensure_content",
    "ensure_document_id",
    "ensure_api_token",
    "is_valid"
)


def throw_if_invalid(value: str, message: str, status: int = None):
    if not (value and isinstance(value, str)):
        raise ImperialError(message=message, status=status)  # hardcoded caught error


def ensure_content(content: str):
    throw_if_invalid(content, message="You need to give text in the `code` parameter!", status=400)


def ensure_document_id(document_id: str):
    throw_if_invalid(document_id, message="We couldn't find that document!", status=404)


def ensure_api_token(api_token: str = None):
    # does not actually make api req to validate api token
    throw_if_invalid(api_token, message="API token is invalid!", status=401)

    if not re.match(api_token_regex, api_token):
        raise ImperialError(message="API token is invalid!", status=401)  # hardcoded caught error


# optional params

default_params = {
    "api_token": None,
    "longer_urls": False,
    "language": None,
    "instant_delete": False,
    "image_embed": False,
    "expiration": 5,
    "encrypted": False,
    "password": None
}


def is_valid(key: str, value: str):
    # check for mandatory and defaults
    if key not in default_params:
        return True
    default_value = default_params[key]
    default_type = type(default_value)
    if default_value == value:
        return False
    # check types
    if isinstance(value, default_type):
        # is expected type
        return True

    if default_value is None and isinstance(value, str):
        # is string when expected type is None
        # could be a problem in the future if we need to pass a non-string into a param with a default value of None
        return True
