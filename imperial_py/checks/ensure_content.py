from ..exceptions import ImperialError


def ensure_content(content: str):
    # check truthiness
    # content doesn't necessarily need to be a string, it will get converted to one later
    if not content or isinstance(content, bool):
        raise ImperialError(message="You need to give text in the `content` parameter!", status=400)