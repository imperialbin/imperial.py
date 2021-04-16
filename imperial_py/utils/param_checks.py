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


def check_params(api_token, **kwargs):
    for key, value in kwargs.items():
        if is_required(key):
            continue
        if not api_token:
            raise ImperialError(
                message="You must be authenticated to pass, `{param}`".format(param=key)
            )
        default_value = default_params[key]
        # i hate how I have to do this in python
        # lmk if there is a better way to check for nullables + types
        expected_types = {type(default_value)} if default_value is not None else {type(None), str}
        if type(value) not in expected_types:
            # this is ugly i know
            raise ImperialError(
                message="{param} expects type(s) {expected} not '{recieved}'".format(
                    param=key,
                    expected=", ".join("'" + str(_type).split("'")[1] + "'" for _type in expected_types),
                    # ex. {NoneType, str} -> 'NoneType', 'str'
                    # quite hacky with the split not sure if theres a better way to convert "<class 'str'>" to "str"
                    recieved=str(type(value)).split("'")[1]
                )
            )


def is_default(key, value):
    return key in default_params and default_params[key] == value


def is_required(key):
    return key not in default_params
