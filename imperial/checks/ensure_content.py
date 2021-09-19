from ..exceptions import ContentRequired


def ensure_content(content: str):
    # check truthiness
    # content doesn't necessarily need to be a string, it will get converted to one later

    # not really sure which types to allow vs not allow,
    # but bools seem like they shouldn't be allowed
    if not content or isinstance(content, bool):
        raise ContentRequired()
