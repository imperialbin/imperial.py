import re

from ..exceptions import ImperialError

api_token_regex = re.compile(r"^IMPERIAL-[a-zA-Z\d]{8}(-[a-zA-Z\d]{4}){3}-[a-zA-Z\d]{12}$")


def check_code(code):
    if not isinstance(code, str):
        raise ImperialError("You need to give text in the `code` parameter!", status=400)  # hardcoded caught error


def check_document_id(document_id):
    if not isinstance(document_id, str):
        raise ImperialError("We couldn't find that document!", status=404)  # hardcoded caught error


def check_api_token(api_token=None):
    if isinstance(api_token, str):
        raise ImperialError("No token to verify!")  # hardcoded caught error

    if not re.match(api_token_regex, api_token):
        raise ImperialError("API token is invalid!", status=401)  # hardcoded caught error
