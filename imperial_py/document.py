from datetime import datetime
from typing import Optional

from . import client
from .exceptions import DocumentNotFound, ImperialError
from .utils import https, get_date_difference

__all__ = (
    "Document",
)


class Document:
    __slots__ = (
        "__api_token",
        "__content",
        "__id",
        "__public",
        "__language",
        "__image_embed",
        "__instant_delete",
        "__creation",
        "__expiration",
        "__editors",
        "__encrypted",
        "__password",
        "__views",
        "__deleted"
    )

    def __init__(self, content: str, api_token: str = None, **kwargs):
        # success isn't needed,
        # message isn't needed
        # longer_urls is generated dynamically
        # formatted_link and raw_link are generated dynamically
        self.__content = content
        self.__api_token = api_token
        # **kwargs
        self.__id = kwargs.get("document_id", None)
        self.__language = kwargs.get("language", "auto")
        self.__public = kwargs.get("public", False)
        self.__image_embed = kwargs.get("image_embed", False)
        self.__instant_delete = kwargs.get("instant_delete", False)
        self.__creation = kwargs.get("creation_date", None)
        self.__expiration = kwargs.get("expiration_date", None)
        self.__editors = kwargs.get("allowed_editors", [])
        self.__encrypted = kwargs.get("encrypted", False)
        self.__password = kwargs.get("password", None)
        self.__views = kwargs.get("views", 0)
        # not from api
        self.__deleted = False

    def __repr__(self):
        representation = f"<Document id={self.id}"
        if self.id:
            if isinstance(self.expiration, datetime):
                representation += f" expiration={self.expiration:%x}"
            if self.language:
                representation += f" language={self.language}"
            if self.password:
                representation += f" password={self.password}"
            if self.deleted:
                # self.deleted will always be true here
                representation += " deleted=True"
        return representation + ">"

    def __eq__(self, other):
        return isinstance(other, Document) and (self.id == other.id or self.content == other.content)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(self.content) if self.content else 0

    def __iter__(self):
        yield "content", self.content
        yield "document_id", self.id
        yield "language", self.language
        yield "image_embed", self.image_embed
        yield "instant_delete", self.instant_delete
        yield "creation_date", self.creation
        yield "expiration_date", self.expiration
        yield "allowed_editors", self.editors
        yield "encrypted", self.encrypted
        yield "password", self.password
        yield "views", self.views

    # dynamic getters

    @property
    def short_urls(self) -> bool:
        return len(self.id) == 4

    @property
    def longer_urls(self) -> bool:
        return len(self.id) == 26

    @property
    def formatted_link(self) -> Optional[str]:
        if self.id:
            return str(https.imperialbin / "p" / self.id)

    @property
    def raw_link(self) -> Optional[str]:
        if self.id:
            return str(https.imperialbin / "r" / self.id)

    @property
    def days_left(self) -> Optional[int]:
        # number of FULL DAYS left
        # 7 days 86399 seconds means 7 days left
        return get_date_difference(datetime.now(), self.expiration)

    # getters of private attrs

    @property
    def api_token(self) -> Optional[str]:
        return self.__api_token

    @property
    def content(self) -> str:
        return self.__content

    @property
    def id(self) -> Optional[str]:
        return self.__id

    @property
    def language(self) -> str:
        return self.__language

    @property
    def public(self) -> bool:
        return self.__public

    @property
    def image_embed(self) -> bool:
        return self.__image_embed

    @property
    def instant_delete(self) -> bool:
        return self.__instant_delete

    @property
    def creation(self) -> Optional[datetime]:
        return self.__creation

    @property
    def expiration(self) -> Optional[datetime]:
        return self.__expiration

    @property
    def editors(self) -> list[str]:
        return self.__editors

    @property
    def encrypted(self) -> bool:
        return self.__encrypted

    @property
    def password(self) -> Optional[str]:
        return self.__password

    @property
    def views(self) -> int:
        return self.__views

    @property
    def deleted(self) -> bool:
        return self.__deleted

    @property
    def editable(self) -> bool:
        return self.api_token and not self.deleted

    # aliases (to match api response keys)
    document_id = id
    allowed_editors = editors
    creation_date = creation
    expiration_date = expiration
    # aliases because cool
    link = formatted_link

    def sync(self):
        if self.deleted:
            raise DocumentNotFound(self.id)
        try:
            updated_doc = client.get_document(document_id=self.id, password=self.password, api_token=self.api_token)
        except ImperialError as exc:
            self.__deleted = True
            raise exc
        self.__content = updated_doc["content"]
        self.__language = updated_doc["document"]["language"]
        self.__public = updated_doc["document"]["public"]
        self.__image_embed = updated_doc["document"]["image_embed"]
        self.__instant_delete = updated_doc["document"]["instant_delete"]
        self.__expiration = updated_doc["document"]["expiration_date"]
        self.__editors = updated_doc["document"]["allowed_editors"]
        self.__encrypted = updated_doc["document"]["encrypted"]
        self.__views = updated_doc["document"]["views"]

    def edit(self, content: str) -> None:
        """
        Edits document code on https://imperialb.in
        PATCH https://imperialb.in/api/document
        :param content: Code from any programming language, capped at 512KB per request (type: str).
        :return: ImperialBin API response (type: dict).
        """
        if not self.editable:
            raise DocumentNotFound(self.id)

        # in the future, `password` might be available as a kwarg
        json = client.edit_document(content, document_id=self.id, api_token=self.api_token)
        if json["success"]:
            self.__views = json.get("document", {}).get("views", 0)
            self.__content = content

    def duplicate(self,
                  content: str = None,
                  *,
                  short_urls: bool = False,
                  longer_urls: bool = False,
                  language: str = None,
                  public: bool = False,
                  instant_delete: bool = False,
                  image_embed: bool = False,
                  expiration: int = 5,
                  encrypted: bool = False,
                  password: str = None,
                  editors: list[str] = None):
        """
        :rtype: Document
        """

        # similar to `create_document` in Imperial
        # using predetermined values or params

        content = content or self.content
        expiration_ = get_date_difference(self.creation, self.expiration)

        resp = client.create_document(
            content=content,
            short_urls=short_urls or self.short_urls,
            longer_urls=longer_urls or self.longer_urls,
            language=language or self.language,
            public=public or self.public,
            instant_delete=instant_delete or self.instant_delete,
            image_embed=image_embed or self.image_embed,
            expiration=expiration or expiration_,
            encrypted=encrypted or self.encrypted,
            password=password or self.password,
            editors=editors or self.editors,
            api_token=self.api_token
        )

        return Document(
            content=content,
            api_token=self.api_token,
            **resp["document"]
        )

    def delete(self) -> None:
        if self.deleted:
            raise DocumentNotFound(self.id)
        client.delete_document(document_id=self.id, api_token=self.api_token)
        # if it doesn't raise then it succeeded
        self.__deleted = True
