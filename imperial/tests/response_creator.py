import json
import re
import secrets
import string
import time

# duplicate from parser
# not sure how to do this without this duplicate
from pprint import pprint

snake_regex = re.compile(r"(?<!^)(?<![A-Z])(?=[A-Z])")

# pytest is 3.6+ and past python 3.6+ dicts are ordered by default
# this means that there isn't a point to making __base an OrderedDict


class https:
    # just so pycharm doesn't yell at me :/
    imperialbin = None

    def __init__(self, name: str):
        self.path = str(name).removesuffix("/")

    def __truediv__(self, endpoint: str):
        # handle / operator
        endpoint = endpoint.removeprefix("/")
        endpoint = endpoint.removesuffix("/")
        return https(self.path + "/" + endpoint)

    def __repr__(self):
        return self.path


# because python doesn't have static getters,
# and I don't want the ()
# used as https.imperialbin / "whatever"
https.imperialbin = https("https://imperialb.in")


class Response:
    __base = {
        "success": True,
        "document": {
            "documentId": None,
            "language": "auto",
            "imageEmbed": False,
            "instantDelete": False,
            "creationDate": 0,
            "expirationDate": 0,
            "allowedEditors": [],
            "encrypted": False,
            "password": None
        }
    }
    __snake_regex = re.compile(r"(?<!^)(?<![A-Z])(?=[A-Z])")
    __characters = string.ascii_letters + string.digits

    @classmethod
    def POST(cls, response=None, **kwargs):
        if isinstance(response, Response):
            return cls(method="POST", **{**response.__get_kwargs(), **kwargs})
        return cls(method="POST", **kwargs)

    @classmethod
    def GET(cls, response=None, **kwargs):
        if isinstance(response, Response):
            return cls(method="GET", **{**response.__get_kwargs(), **kwargs})
        return cls(method="GET", **kwargs)

    @classmethod
    def PATCH(cls, response=None, **kwargs):
        if isinstance(response, Response):
            return cls(method="PATCH", **{**response.__get_kwargs(), **kwargs})
        return cls(method="PATCH", **kwargs)

    @classmethod
    def DELETE(cls, response=None, **kwargs):
        if isinstance(response, Response):
            kwargs.update(response.__get_kwargs())
        return cls(method="DELETE", **kwargs)

    def __get_kwargs(self):
        return {item: getattr(self, item) for item in dir(self) if self.__to_camel_case(item) in self.document}

    @staticmethod
    def __generate_time(extra_days=0):
        return int(time.time() * 1000) + (86400000 * extra_days)

    @staticmethod
    def __to_camel_case(text):
        camel_case = "".join(x.title() for x in text.split("_"))
        return camel_case[0].lower() + camel_case[1:]

    def __generate_string(self, length):
        return "".join(secrets.choice(self.__characters) for _ in range(length))

    def __to_snake_case(self, text):
        return self.__snake_regex.sub("_", text).lower()

    def __init__(self, *, method, **kwargs):
        self.__resp = self.__base.copy()
        self.__method = method
        if kwargs.get("document_id", None):
            self.document_id = kwargs.pop("document_id")
        # generate id
        elif kwargs.get("longer_urls", False):
            self.document_id = self.__generate_string(26)
            del kwargs["longer_urls"]
        else:
            self.document_id = self.__generate_string(8)

        # expirations
        # even for the get and edit route we generate new times
        # (it's not going to matter)
        if kwargs.get("expiration", False):
            self.creation_date = self.__generate_time()
            self.expiration_date = self.__generate_time(int(kwargs.pop("expiration")))
        else:
            self.creation_date = self.__generate_time()
            self.expiration_date = self.__generate_time(5)

        if kwargs.get("encrypted", False) and not kwargs.get("password"):
            self.encrypted = True
            self.password = self.__generate_string(12)
            del kwargs["encrypted"]
        elif kwargs.get("encrypted", False):
            self.encrypted = True
            self.password = kwargs.pop("password")
            del kwargs["encrypted"]

        for key, value in kwargs.items():
            if self.__to_camel_case(key) not in self.document:
                continue
            setattr(self, key, value)

        content = kwargs.pop("content") if kwargs.get("content") else "test"
        self.write_exclusives(method, content)

        # to move document to end
        self.document = self.response.pop("document")

    def write_exclusives(self, method, content=None):
        self.content = content if method == "GET" else None
        self.message = "Successfully edit the document!" if method == "PATCH" else None
        self.raw_link = str(https.imperialbin / "r" / self.document_id) if method in {"PATCH", "POST"} else None
        self.formatted_link = str(https.imperialbin / "p" / self.document_id) if method in {"PATCH", "POST"} else None

    @property
    def method(self):
        return self.__method

    @property
    def response(self):
        return self.__resp

    @property
    def json(self):
        return json.dumps(self.response)

    @property
    def document(self):
        return self.response["document"]

    # more specific details
    @property
    def success(self):
        return self.response["success"]

    @property
    def document_id(self):
        return self.document["documentId"]

    @property
    def language(self):
        return self.document["language"]

    @property
    def image_embed(self):
        return self.document["imageEmbed"]

    @property
    def instant_delete(self):
        return self.document["instantDelete"]

    @property
    def creation_date(self):
        return self.document["creationDate"]

    @property
    def expiration_date(self):
        return self.document["expirationDate"]

    @property
    def allowed_editors(self):
        return self.document["allowedEditors"]

    @property
    def encrypted(self):
        return self.document["encrypted"]

    @property
    def password(self):
        return self.document["password"]

    # setters

    @success.setter
    def success(self, value):
        self.response["success"] = value

    @document.setter
    def document(self, value):
        self.response["document"] = value

    @document_id.setter
    def document_id(self, value):
        self.document["documentId"] = value

    @language.setter
    def language(self, value):
        self.document["language"] = value

    @image_embed.setter
    def image_embed(self, value):
        self.document["imageEmbed"] = value

    @instant_delete.setter
    def instant_delete(self, value):
        self.document["instantDelete"] = value

    @creation_date.setter
    def creation_date(self, value):
        self.document["creationDate"] = value

    @expiration_date.setter
    def expiration_date(self, value):
        self.document["expirationDate"] = value

    @allowed_editors.setter
    def allowed_editors(self, value):
        self.document["allowedEditors"] = value

    @encrypted.setter
    def encrypted(self, value):
        self.document["encrypted"] = value

    @password.setter
    def password(self, value):
        self.document["password"] = value

    # optional; not always present

    @property
    def content(self):
        return self.response.get("content")

    @content.setter
    def content(self, value):
        if value is not None:
            self.response["content"] = value

    @property
    def message(self):
        return self.document.get("message")

    @message.setter
    def message(self, value):
        if value is not None:
            self.document["message"] = value

    @property
    def formatted_link(self):
        return self.response.get("formattedLink")

    @formatted_link.setter
    def formatted_link(self, value):
        if value is not None:
            self.response["formattedLink"] = value

    @property
    def raw_link(self):
        return self.response.get("rawLink")

    @raw_link.setter
    def raw_link(self, value):
        if value is not None:
            self.response["rawLink"] = value