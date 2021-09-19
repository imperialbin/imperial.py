import pytest

from imperial.exceptions import ImperialError, DocumentNotFound, ContentRequired, InvalidAuthorization


def test_imperial_error():
    # make sure it works without param
    with pytest.raises(ImperialError):
        raise ImperialError()
    # and with
    with pytest.raises(ImperialError):
        raise ImperialError("err")

    try:
        raise ImperialError()
    except ImperialError as error:
        print(error.args[0])
        assert error.args[0] == "Uncaught Exception. Report Issues Here: https://github.com/imperialbin/imperial-py"

    error_message = "TEST!"
    try:
        raise ImperialError(error_message)
    except ImperialError as error:
        assert error.args[0].startswith(error_message)


def test_document_error():
    with pytest.raises(DocumentNotFound):
        raise DocumentNotFound()
    with pytest.raises(DocumentNotFound):
        raise DocumentNotFound("09sd1fcs")

    try:
        raise DocumentNotFound()
    except DocumentNotFound as error:
        print(error.args[0])
        assert error.args[0] == "We couldn't find that document!"

    try:
        raise DocumentNotFound("09sd1fcs")
    except DocumentNotFound as error:
        assert error.args[0] == "We couldn't find a document with id, 09sd1fcs!"


def test_content_required():
    with pytest.raises(ContentRequired):
        raise ContentRequired()

    try:
        raise ContentRequired()
    except ContentRequired as error:
        assert error.args[0] == "You need to give text in the `content` parameter!"


def test_authorization_error():
    with pytest.raises(InvalidAuthorization):
        raise InvalidAuthorization("IMPERIAL-00000000-0000-0000-0000-000000000000")
    with pytest.raises(InvalidAuthorization):
        raise InvalidAuthorization()
