default_params = {
    "api_token": None,
    "longer_urls": False,
    "language": None,
    "instant_delete": False,
    "image_embed": False,
    "expiration": 5,
    "encrypted": False,
    "password": None
}


def is_valid_param(key: str, value: str):
    # check for mandatory and defaults
    if key not in default_params:
        return True
    default_value = default_params[key]
    default_type = type(default_value)
    if default_value == value:
        return False
    # check types
    if isinstance(value, default_type):
        # is expected type
        return True

    if default_value is None and isinstance(value, str):
        # is string when expected type is None
        # could be a problem in the future if we need to pass a non-string into a param with a default value of None
        return True
    return False
