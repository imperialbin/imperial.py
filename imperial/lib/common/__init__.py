HOSTNAME = "https://staging-balls.impb.in"
API_HOSTNAME = "https://staging-balls-api.impb.in"

MISSING = object()


def camel_to_snake(text: str) -> str:
    return "".join("_" + t.lower() if t.isupper() else t for t in text).lstrip("_")


def camel_dict_to_snake(data: dict) -> dict:
    return {camel_to_snake(k): v for k, v in data.items()}
