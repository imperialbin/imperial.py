__all__ = (
    "ImperialError",
    "DocumentNotFound",
    "ContentRequired",
    "InvalidAuthorization"
)


class ImperialError(Exception):

    def __init__(self, message: str = None):
        message = message or "Uncaught Exception. Report Here: https://github.com/imperialbin/imperial-py"
        super().__init__(message)


class DocumentNotFound(ImperialError):

    def __init__(self, document_id: str = None):
        message = f"We couldn't find a document with id, {document_id}!" if document_id else "We couldn't find that document!"
        super().__init__(message)


class ContentRequired(ImperialError):

    def __init__(self):
        super().__init__("You need to give text in the `content` parameter!")


class InvalidAuthorization(ImperialError):

    def __init__(self, message: str = None, api_token: str = None):
        if not (message or api_token):
            message = "Your authorization is invalid"
        elif api_token and not message:
            message = f"The API token, {api_token} is invalid!" if api_token else "API token is invalid!"
        super().__init__(message)
