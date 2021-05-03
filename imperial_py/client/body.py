from imperial_py.utils import to_camel_case


class Body:

    __expected_params = {
        # in format: default, expected type
        "api_token": (None, str),
        "longer_urls": (False, bool),
        "language": (None, str),
        "instant_delete": (False, bool),
        "image_embed": (False, bool),
        "expiration": (5, int),
        "encrypted": (False, bool),
        "password": (None, str)
    }

    __slots__ = (
        "__headers",
        "__params",
        "__json"
    )

    def __init__(self, *, method, **kwargs):
        self.__headers = None
        self.__params = None
        self.__json = None
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
            self.update_params("password", password)
        else:  # method isn't GET; password goes to json body instead
            self.update_json("password", password)

        # last thing, convert to camel case
        if self.json:
            self.__json = to_camel_case(self.json)

    def handle_kwarg(self, key, value):

        if key not in self.__expected_params:
            # mandatory; always set with type string
            self.update_json(key, str(value))
            return

        default_value, expected_type = self.__expected_params[key]

        if value != default_value and isinstance(value, expected_type):
            # unique value w/ correct typing
            self.update_json(key, value)

    def update_json(self, key, value):
        if self.__json is None:
            self.__json = {}
        self.__json[key] = value

    def update_params(self, key, value):
        if self.__params is None:
            self.__params = {}
        self.__params[key] = value

    # getters of parsed data
    # by default they're all None,
    # but will get switched to a mutable data type
    # if they get data to hold

    @property
    def headers(self):
        return self.__headers

    @property
    def params(self):
        return self.__params

    @property
    def json(self):
        return self.__json
