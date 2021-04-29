from .utils import client
from .utils.checks import ensure_api_token
from .utils.hostname import https


class Document:

    def __init__(self, document_dict: dict, code: str = None, api_token: str = None):
        self.__document_dict = {}
        if isinstance(document_dict, dict) and document_dict.get("success", False):
            self.__api_token = api_token
            self.__document_dict = document_dict["document"]

            if "content" in document_dict:
                self.__document_dict["content"] = document_dict["content"]
            elif code:
                self.__document_dict["content"] = code
            elif not self.instant_delete or not self.__document_dict.get("content"):
                self.__document_dict["content"] = client.get(self.id, password=self.password).get("content")
            # this should cover all cases but just in case
            else:
                self.__document_dict["content"] = None

    def __eq__(self, other):
        return isinstance(other, Document) and (self.id == other.id or self.code == other.code)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        representation = "<Document id={self.id}"
        if self.id:
            if hasattr(self.expiration, "strftime"):
                # due to a bug expiration was unable to be converted into a datetime obj so now we have this check
                # kind of a hacky way of seeing if it's a datetime obj w/o needing to import datetime for a type check
                representation += " expiration={self.expiration:%x}"
            if self.language:
                representation += " language={self.language}"
            if self.password:
                representation += " password={self.password}"
        return (representation + ">").format(self=self)

    def __getitem__(self, item: str):
        return self.__document_dict.get(item)

    def __setitem__(self, key: str, value: str):
        if key == "code":
            # reminds me of javascript with . and [""] syntax for dicts
            self.edit(value)

    def __len__(self):
        return len(self.code)

    def __iter__(self):
        for item, key in self.__document_dict.items():
            yield item, key

    # extra properties

    @property
    def api_token(self):
        return self.__api_token

    @property
    def code(self):
        return self.__document_dict.get("content", "")

    @code.setter
    def code(self, value: str):
        self.edit(value)

    # properties that might get added to the api response in the future

    @property
    def longer_urls(self):
        return len(self.id) == 26

    # properties directly from the api

    # general

    @property
    def link(self):
        return str(https.imperialbin / "p" / self.id)

    # nested inside `document` key

    @property
    def id(self):
        return self.__document_dict.get("document_id")

    @property
    def language(self):
        return self.__document_dict.get("language", "auto")

    @property
    def image_embed(self):
        return self.__document_dict.get("image_embed", False)

    @property
    def instant_delete(self):
        return self.__document_dict.get("instant_delete", False)

    @property
    def creation(self):
        return self.__document_dict.get("creation_date")

    @property
    def expiration(self):
        return self.__document_dict.get("expiration_date")

    @property
    def editors(self):
        return self.__document_dict.get("allowed_editors", [])

    @property
    def encrypted(self):
        return self.__document_dict.get("encrypted", False)

    @property
    def password(self):
        return self.__document_dict.get("password")

    @property
    def views(self):
        return self.__document_dict.get("views", 0)

    # aliases (i won't be using these)
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
        json = client.edit(code, document_id=self.id, password=self.password, api_token=self.api_token)
        if json["success"]:
            self.__document_dict["views"] = json.get("document", {}).get("views", 0)
            self.__document_dict["content"] = code

    def duplicate(self):
        return Document(client.create(code=self.code,
                                      longer_urls=self.longer_urls,
                                      instant_delete=self.instant_delete,
                                      image_embed=self.image_embed,
                                      expiration=5,
                                      encrypted=self.encrypted,
                                      password=self.password,
                                      api_token=self.api_token), api_token=self.api_token)
