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

default_params = {
    "apiToken": None,
    "longerUrls": False,
    "language": None,
    "instantDelete": False,
    "imageEmbed": False,
    "expiration": 5,
    "encrypted": False,
    "password": None
}


def check_params(params):
    for key, value in params.items():
        if key not in default_params:
            continue
        default_value = default_params[key]
        expected_types = {type(default_value)} if default_value is not None else {type(None), str}
        if type(value) not in expected_types:
            raise ImperialError(
                message="{} expects type(s) {} not '{}'".format(
                    key,
                    ", ".join("'" + str(_type).split("'")[1] + "'" for _type in expected_types),
                    # ex. {NoneType, str} -> 'NoneType', 'str'
                    # quite hacky with the split not sure if theres a better way to convert "<class 'str'>" to "str"
                    str(type(value)).split("'")[1]
                )
            )


def is_default(key, value):
    return key in default_params and default_params[key] == value
