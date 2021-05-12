from http.client import responses

__all__ = (
    "ImperialError",
    "DocumentNotFound",
    "ContentRequired",
    "InvalidAuthorization"
)


class ImperialError(Exception):

    def __init__(self, message=None):
        if not message:
            message = "Uncaught Exception. Report Here: https://github.com/imperialbin/imperial-py"
        super().__init__(message)


class DocumentNotFound(ImperialError):

    def __init__(self, document_id=None):
        if document_id:
            message = "We couldn't find a document with id, {}!".format(document_id)
        else:
            message = "We couldn't find that document!"
        super().__init__(message)


class ContentRequired(ImperialError):
    def __init__(self):
        super().__init__("You need to give text in the `content` parameter!")


class InvalidAuthorization(ImperialError):
    def __init__(self, api_token=None):
        if api_token:
            message = "The API token, {} is invalid!".format(api_token)
        else:
            message = "API token is invalid!"
        super().__init__(message)
