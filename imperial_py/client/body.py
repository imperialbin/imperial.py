from imperial_py.utils import to_camel_case


class Body:

    __default_params = {
        "api_token": None,
        "longer_urls": False,
        "language": None,
        "instant_delete": False,
        "image_embed": False,
        "expiration": 5,
        "encrypted": False,
        "password": None
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

        if password and method == "GET":
            self.update_params("password", password)
        else:  # method isn't GET; password goes to json body instead
            self.update_json("password", password)

        # last thing, convert to camel case
        if self.json:
            self.__json = to_camel_case(self.json)

    def handle_kwarg(self, key, value):

        if key not in self.__default_params:
            self.update_json(key, str(value))
            return

        default_value = self.__default_params[key]
        default_type = type(default_value)

        if default_value == value:
            return
        if isinstance(value, default_type):
            # is expected type
            self.update_json(key, value)
            return
        if default_value is None and isinstance(value, str):
            # is string when expected type is None. could be a problem in the future if we need to pass a
            # non-string into a param with a default value of None
            self.update_json(key, value)
            return

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
