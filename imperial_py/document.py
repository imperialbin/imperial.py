from .client import create, get, edit, delete


class Document:

    def __init__(self, document_dict, code=None, api_token=None):
        self.__document_dict = document_dict
        self.__api_token = api_token
        # doesn't get code if instant_delete is on
        if self.success:
            # `code` is added to document_dict so everything is easy to access
            if "code" in self.__document_dict:
                pass
            elif code:
                self.__document_dict["code"] = code
            elif not self.instant_delete:
                # code isn't specified so we try and fetch it
                # kind of confusing with two `get` functions, but they do different things. (one is a builtin)
                self.__document_dict["code"] = get(self.id, password=self.password).get("content")
            else:
                self.__document_dict["code"] = None

    def __eq__(self, other):
        return isinstance(other, Document) and hasattr(other, "id") and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        if not self.success:
            return f"<Document success=False id=None>"
        return "<Document id={0.id} password={0.password} expiration={0.expiration!r}>".format(self)

    def __getitem__(self, item):
        return self.__document_dict.get(item)

    def __setitem__(self, key, value):
        if key == "code":
            # reminds me of javascript with . and [""] syntax for dicts
            self.edit(value)

    def __len__(self):
        return len(self.code)

    @property
    def dict(self):
        return self.__document_dict

    @property
    def success(self):
        return self.__document_dict.get("success", False)

    @property
    def code(self):
        return self.__document_dict.get("code")

    @code.setter
    def code(self, value):
        self.edit(value)

    @property
    def longer_urls(self):
        return self.__document_dict.get("longer_urls")

    @property
    def image_embed(self):
        return self.__document_dict.get("image_embed")

    @property
    def expiration(self):
        return self.__document_dict.get("expiration")

    @property
    def id(self):
        return self.__document_dict.get("document_id")

    @property
    def encrypted(self):
        return self.__document_dict.get("encrypted")

    @property
    def password(self):
        return self.__document_dict.get("password")

    @property
    def instant_delete(self):
        return self.__document_dict.get("instant_delete", False)

    @property
    def link(self):
        return self.__document_dict.get("formatted_link")

    def edit(self, code):
        """
        Edits document code on https://imperialb.in
        PATCH https://imperialb.in/api/document
        :param code: Code from any programming language, capped at 512KB per request (type: str).
        :type code: str
        :return: ImperialBin API response (type: dict).
        """
        json = edit(code, document_id=self.id, password=self.password, api_token=self.__api_token)
        if json["success"]:
            self.__document_dict = json
            self.__document_dict["code"] = code
        return json
