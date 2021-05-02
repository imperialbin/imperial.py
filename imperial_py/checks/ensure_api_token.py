import re

from ..exceptions import ImperialError

api_token_regex = re.compile(r"^IMPERIAL-[a-zA-Z\d]{8}(-[a-zA-Z\d]{4}){3}-[a-zA-Z\d]{12}$")


def ensure_api_token(api_token: str = None):
    # does not actually make api req to validate api token
    # short circuiting if statements mean that
    if not (api_token and isinstance(api_token, str) and re.match(api_token_regex, api_token)):
        raise ImperialError(message="API token is invalid!", status=401)
