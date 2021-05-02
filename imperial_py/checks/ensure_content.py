from ..checks.is_invalid_string import is_invalid_string
from ..exceptions import ImperialError


def ensure_content(content: str):
    if is_invalid_string(content):
        raise ImperialError(message="You need to give text in the `code` parameter!", status=400)