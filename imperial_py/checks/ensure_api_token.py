import re

from ..exceptions import ImperialError

api_token_regex = re.compile(r"^IMPERIAL-[a-zA-Z\d]{8}(-[a-zA-Z\d]{4}){3}-[a-zA-Z\d]{12}$")


def ensure_api_token(api_token: str = None):
    # used with if api_token: ensure_api_token() alot,
    # but I guess it's better to be explicit and show that it's only checking if it exists
    # could be changed if i had better names, ex `throw_if_invalid_api_token` would more clearly
    # show that it's only throwing if it's invalid and not if it's None

    # does not actually make api req to validate api token
    # short circuiting if statements mean that we don't need to worry about type handling in the regex
    # because the prior isinstance call will do that for us
    if not api_token or not isinstance(api_token, str) or not re.match(api_token_regex, api_token):
        raise ImperialError(message="API token is invalid!", status=401)
