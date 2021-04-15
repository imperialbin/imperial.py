import re

from ..exceptions import ImperialError

api_token_regex = re.compile(r"^IMPERIAL-[a-zA-Z\d]{8}(-[a-zA-Z\d]{4}){3}-[a-zA-Z\d]{12}$")


# required params


def throw_if_invalid(key, value, message, status=None):
    if not (isinstance(value, str) and value):
        raise ImperialError(message=message, status=status)  # hardcoded caught error


def check_code(code):
    throw_if_invalid("code", code, message="You need to give text in the `code` parameter!", status=400)


def check_document_id(document_id):
    throw_if_invalid("documentId", document_id, message="We couldn't find that document!", status=404)


def check_api_token(api_token=None):
    throw_if_invalid("apiToken", api_token, message="No token to verify!", status=404)

    if not re.match(api_token_regex, api_token):
        raise ImperialError("API token is invalid!", status=401)  # hardcoded caught error


# optional params

default_params =  {
    "longerUrls": False,
    "language": None,
    "instantDelete": False,
    "imageEmbed": False,
    "expiration": 5,
    "encrypted": False,
    "password": None
}


def is_required(key):
    return key in default_params


def is_valid_data(key, value):
    default_value = default_params.get(key)
    return default_value != value and isinstance(type(value), type(default_value))
