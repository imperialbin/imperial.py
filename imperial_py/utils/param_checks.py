import re

from ..exceptions import ImperialError

api_token_regex = re.compile(r"^IMPERIAL-[a-zA-Z\d]{8}(-[a-zA-Z\d]{4}){3}-[a-zA-Z\d]{12}$")


def throw_if_invalid(data, message, status=None):
    if not (isinstance(data, str) and data):
        raise ImperialError(message=message, status=status)  # hardcoded caught error


def check_code(code):
    throw_if_invalid(code, message="You need to give text in the `code` parameter!", status=400)


def check_document_id(document_id):
    throw_if_invalid(document_id, message="We couldn't find that document!", status=404)


def check_api_token(api_token=None):
    throw_if_invalid(api_token, message="No token to verify!", status=404)

    if not re.match(api_token_regex, api_token):
        raise ImperialError("API token is invalid!", status=401)  # hardcoded caught error
