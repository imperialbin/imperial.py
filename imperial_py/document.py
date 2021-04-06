from .utils import client


class Document:

    def __init__(self, document_dict, code=None, api_token=None):
        if isinstance(document_dict, dict) and document_dict.get("success", False):
            self.__full_document_dict = document_dict
            self.__document_dict = self.__full_document_dict["document"]
            self.__api_token = api_token
            if "code" not in self.__document_dict:
                # `code` is added to document_dict so everything is easy to access
                if not self.success:
                    self.__document_dict["code"] = None
                elif code:
                    self.__document_dict["code"] = code
                elif not self.instant_delete:
                    # code isn't specified so we try and fetch it
                    # kind of confusing with two `get` functions, but they do different things. (one is a builtin)
                    self.__document_dict["code"] = client.get(self.id, password=self.password).get("content")
        else:
            self.__full_document_dict = {"document": {}}
            self.__document_dict = self.__full_document_dict["document"]

    def __eq__(self, other):
        return isinstance(other, Document) and (self.id == other.id or self.code == other.code)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        if not self.success:
            return "<Document id=None>"
        representation = "<Document id={self.id}"

        if hasattr(self.expiration, "strftime"):
            # due to a bug expiration was unable to be converted into a datetime obj so now we have this check
            # kind of a hacky way of seeing if it's a datetime obj w/o needing to import datetime for a type check
            representation += " expiration={self.expiration:%x}"
        if self.language:
            representation += " language={self.language}"
        if self.password:
            representation += " password={self.password}"
        return (representation + ">").format(self=self)

    def __getitem__(self, item):
        return self.__full_document_dict.get(item)

    def __setitem__(self, key, value):
        if key == "code":
            # reminds me of javascript with . and [""] syntax for dicts
            self.edit(value)

    def __len__(self):
        return len(self.code)

    def __iter__(self):
        for item, key in self.__full_document_dict.items():
            yield item, key

    # extra properties

    @property
    def code(self):
        return self.__document_dict.get("code")

    @code.setter
    def code(self, value):
        self.edit(value)

    # properties that might get added to the api response in the future

    @property
    def longer_urls(self):
        return len(self.id) == 26

    # properties directly from the api

    # general

    @property
    def success(self):
        return self.__full_document_dict.get("success", False)

    @property
    def link(self):
        return self.__full_document_dict.get("formatted_link")

    # nested inside `document` key

    @property
    def id(self):
        return self.__document_dict.get("document_id")

    @property
    def language(self):
        return self.__document_dict.get("language")

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
        return self.__document_dict.get("allowed_editors")

    @property
    def encrypted(self):
        return self.__document_dict.get("encrypted", False)

    @property
    def password(self):
        return self.__document_dict.get("password")

    @property
    def views(self):
        return self.__document_dict.get("views")

    # aliases (i won't be using these)
    document_id = id
    allowed_editors = editors
    creation_date = creation
    expiration_date = expiration

    def edit(self, code):
        """
        Edits document code on https://imperialb.in
        PATCH https://imperialb.in/api/document
        :param code: Code from any programming language, capped at 512KB per request (type: str).
        :type code: str
        :return: ImperialBin API response (type: dict).
        """
        json = client.edit(code, document_id=self.id, password=self.password, api_token=self.__api_token)
        if json["success"]:
            if "message" in json:
                del json["message"]
            self.__full_document_dict["document"]["views"] = json["document"]["views"]
            self.__full_document_dict["document"]["code"] = code
            self.__document_dict = self.__full_document_dict["document"]
        return self

    def duplicate(self):
        return Document(client.create(code=self.code,
                                      longer_urls=self.longer_urls,
                                      instant_delete=self.instant_delete,
                                      image_embed=self.image_embed,
                                      expiration=5,
                                      encrypted=self.encrypted,
                                      password=self.password,
                                      api_token=self.__api_token), api_token=self.__api_token)
