from datetime import datetime

from . import client
from .utils.checks import ensure_api_token
from .utils.hostname import https

__all__ = (
    "Document",
)


class Document:

    def __init__(self, content: str = None, api_token: str = None, **kwargs):
        self.__api_token = api_token
        self.__content = content or kwargs.get("content", None)
        # **kwargs
        self.__id = kwargs.get("document_id", None)
        self.__language = kwargs.get("language", "auto")
        self.__image_embed = kwargs.get("image_embed", False)
        self.__instant_delete = kwargs.get("instant_delete", False)
        self.__creation = kwargs.get("creation_date", None)
        self.__expiration = kwargs.get("expiration_date", None)
        self.__editors = kwargs.get("allowedEditors", [])
        self.__encrypted = kwargs.get("encrypted", None)
        self.__password = kwargs.get("password", None)
        self.__views = kwargs.get("views", 0)
        # success isn't needed,
        # message isn't needed
        # longer_urls is generated dynamically
        # link is generated dynamically

    def __repr__(self):
        representation = "<Document id={self.id}"
        if self.id:
            if isinstance(self.expiration, datetime):
                representation += " expiration={self.expiration:%x}"
            if self.language:
                representation += " language={self.language}"
            if self.password:
                representation += " password={self.password}"
        # this is formatting an insecure string
        # meaning that who ever controls the formatting can access object attrs getters etc
        # this should pose no risk here with self=self though
        return (representation + ">").format(self=self)

    def __eq__(self, other):
        return isinstance(other, Document) and (self.id == other.id or self.content == other.content)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getitem__(self, item: str):
        return getattr(self, item)

    def __setitem__(self, key: str, value: str):
        # reminds me of javascript with dot notation and bracket syntax
        if key == "code":
            self.edit(value)

    def __len__(self):
        return len(self.content)

    def __iter__(self):
        # explicitly yield
        for getter, value in {
            "content": self.content,
            "id": self.id,
            "language": self.language,
            "image_embed": self.image_embed,
            "instant_delete": self.instant_delete,
            "creation": self.creation,
            "expiration": self.expiration,
            "editors": self.editors,
            "encrypted": self.encrypted,
            "password": self.password,
            "views": self.views
        }.items():
            yield getter, value

    # dynamic getters

    @property
    def longer_urls(self):
        return len(self.id) == 26

    @property
    def link(self):
        return str(https.imperialbin / "p" / self.id)

    @property
    def days_left(self):
        # always rounds down
        # ex. 7 days 86399 seconds means 7 days left
        days = (self.expiration - datetime.now()).days
        return days if days > 0 else None

    # getters of private attrs

    @property
    def api_token(self):
        return self.__api_token

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value: str):
        self.edit(value)

    @property
    def id(self):
        return self.__id

    @property
    def language(self):
        return self.__language

    @property
    def image_embed(self):
        return self.__image_embed

    @property
    def instant_delete(self):
        return self.__instant_delete

    @property
    def creation(self):
        return self.__creation

    @property
    def expiration(self):
        return self.__expiration

    @property
    def editors(self):
        return self.__editors

    @property
    def encrypted(self):
        return self.__encrypted

    @property
    def password(self):
        return self.__password

    @property
    def views(self):
        return self.__views

    # aliases (I won't be using these, and I recommend you don't)
    document_id = id
    allowed_editors = editors
    creation_date = creation
    expiration_date = expiration

    def edit(self, code: str):
        """
        Edits document code on https://imperialb.in
        PATCH https://imperialb.in/api/document
        :param code: Code from any programming language, capped at 512KB per request (type: str).
        :return: ImperialBin API response (type: dict).
        """
        ensure_api_token(self.api_token)
        json = client.edit_document(code, document_id=self.id, password=self.password, api_token=self.api_token)
        if json["success"]:
            self.__views = json.get("document", {}).get("views", 0)
            self.__content = code

    def duplicate(self):
        return Document(client.create_document(content=self.content,
                                               longer_urls=self.longer_urls,
                                               instant_delete=self.instant_delete,
                                               image_embed=self.image_embed,
                                               expiration=5,
                                               encrypted=self.encrypted,
                                               password=self.password,
                                               api_token=self.api_token), api_token=self.api_token)
