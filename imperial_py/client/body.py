from imperial_py.utils import to_camel_case


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

        api_token = kwargs.pop("api_token") if "api_token" in kwargs else None
        password = kwargs.pop("password") if "password" in kwargs else None

        for key, value in kwargs.items():
            self.handle_kwarg(key, value)

        if api_token:
            self.__headers = {"authorization": api_token}

        if not password:
            pass
        elif method == "GET":
            self.__params["password"] = password
        else:  # method isn't GET; password goes to json body instead
            self.__json["password"] = password

    def handle_kwarg(self, key, value):

        if key not in self.__expected_params:
            # mandatory; always set with type string
            self.__json[key] = value
            return

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
