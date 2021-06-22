from datetime import datetime
from typing import Optional, List

from . import client
from .exceptions import DocumentNotFound
from .utils import https, get_date_difference

__all__ = (
    "Document",
)


class Document:
    __slots__ = (
        "__api_token",
        "__content",
        "__document_id",
        "__public",
        "__language",
        "__image_embed",
        "__instant_delete",
        "__creation_date",
        "__expiration_date",
        "__allowed_editors",
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
        self.__document_id = kwargs.get("document_id", None)
        self.__language = kwargs.get("language", "auto")
        self.__public = kwargs.get("public", False)
        self.__image_embed = kwargs.get("image_embed", False)
        self.__instant_delete = kwargs.get("instant_delete", False)
        self.__creation_date = kwargs.get("creation_date", None)
        self.__expiration_date = kwargs.get("expiration_date", None)
        self.__allowed_editors = kwargs.get("allowed_editors", [])
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

    def __len__(self):
        return len(self.content) if self.content else 0

    def __iter__(self):
        yield "content", self.content
        yield "document_id", self.id
        yield "language", self.language
        yield "public", self.public
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
        if not self.id:
            return
        if self.short_urls:
            return str(https.impbin / "p" / self.id)
        return str(https.imperialbin / "p" / self.id)

    @property
    def raw_link(self) -> Optional[str]:
        if not self.id:
            return
        if self.short_urls:
            return str(https.impbin / "r" / self.id)
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
    def document_id(self) -> Optional[str]:
        return self.__document_id

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
    def creation_date(self) -> Optional[datetime]:
        return self.__creation_date

    @property
    def expiration_date(self) -> Optional[datetime]:
        return self.__expiration_date

    @property
    def allowed_editors(self) -> List[str]:
        return self.__allowed_editors

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

    # aliases
    id = document_id
    editors = allowed_editors
    creation = creation_date
    expiration = expiration_date
    link = formatted_link

    def __sync(self, **kwargs):
        self.__content = kwargs.get("content", self.__content)
        self.__language = kwargs.get("language", self.__language)
        self.__public = kwargs.get("public", self.__public)
        self.__image_embed = kwargs.get("image_embed", self.__image_embed)
        self.__instant_delete = kwargs.get("instant_delete", self.__instant_delete)
        self.__expiration_date = kwargs.get("expiration_date", self.__expiration_date)
        self.__allowed_editors = kwargs.get("allowed_editors", self.__allowed_editors)
        self.__encrypted = kwargs.get("encrypted", self.__encrypted)
        self.__views = kwargs.get("views", self.__views)

    def sync(self):
        if self.deleted:
            raise DocumentNotFound(self.id)
        try:
            resp = client.get_document(document_id=self.id, password=self.password, api_token=self.api_token)
        except DocumentNotFound as exc:
            self.__deleted = True
            raise exc
        self.__sync(**resp["document"])
        self.__content = resp.get("content", self.__content)

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
        resp = client.edit_document(content, document_id=self.id, api_token=self.api_token)
        # if we make it this far w/o exception then req succeeded.
        self.__sync(**resp["document"])
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
                  editors: List[str] = None):
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
