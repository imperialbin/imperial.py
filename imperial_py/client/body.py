import json

from ..exceptions import ImperialError
from ..utils import to_camel_case


class Body:

    __expected_params = {
        # in format: default, expected type
        "api_token": (None, str),
        "short_urls": (False, bool),
        "longer_urls": (False, bool),
        "language": (None, str),
        "public": (False, bool),
        "instant_delete": (False, bool),
        "image_embed": (False, bool),
        "expiration": (5, int),
        "encrypted": (False, bool),
        "password": (None, str),
        "editors": (None, list)
    }

    __slots__ = (
        "__headers",
        "__params",
        "__json"
    )

    def __init__(self, *, method, **kwargs):
        self.__headers = {}
        self.__params = {}
        self.__json = {}
        # handle param validity

        api_token = kwargs.pop("api_token", None)
        password = kwargs.pop("password", None)

        for key, value in kwargs.items():
            if key not in self.__expected_params:
                self.handle_mandatory_param(key, value)
            elif api_token:
                self.handle_optional_param(key, value)

        if api_token:
            self.__headers["authorization"] = api_token

            if not password:
                pass
            elif method == "GET":
                self.__params["password"] = password
            else:  # if method isn't GET, password goes to json body instead
                self.__json["password"] = password

    @staticmethod
    def parse_content(value):
        try:
            if isinstance(value, str):
                pass
            elif isinstance(value, bytes):
                value = value.decode("utf8")
            elif isinstance(value, dict) or isinstance(value, list):
                value = json.dumps(value)
            return value
        except (TypeError, UnicodeDecodeError):
            raise ImperialError("failed to convert content to type str")

    def handle_mandatory_param(self, key, value):
        # checks for expected keys
        # if these keys are changed in the future this won't be an issue,
        # it just won't be able to check them before they hit the server
        if key == "code":
            value = self.parse_content(value)
        self.__json[key] = value

    def handle_optional_param(self, key, value):
        default_value, expected_type = self.__expected_params[key]
        if value != default_value and isinstance(value, expected_type):
            # unique value w/ correct typing
            self.__json[key] = value

    # getters of parsed data

    @property
    def headers(self):
        return self.__headers if self.__headers else None

    @property
    def params(self):
        return self.__params if self.__params else None

    @property
    def json(self):
        return to_camel_case(self.__json) if self.__json else None
