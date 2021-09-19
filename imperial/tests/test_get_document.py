import json
import os

import pytest

from .response_creator import Response
from ..document import Document
from ..utils.hostname import https
from ..exceptions import ImperialError
from ..imperialbin import Imperial, get_document

api_token = "IMPERIAL-00000000-0000-0000-0000-000000000000"


def test_get_document(requests_mock):
    resp = Response.GET()
    deletion_resp = Response.DELETE(resp)
    requests_mock.get(url=str(https.imperialbin / "api" / "document" / resp.document_id),
                      text=resp.json)
    requests_mock.delete(url=str(https.imperialbin / "api" / "document" / resp.document_id),
                         text=deletion_resp.json)
    get_doc = Imperial(api_token=api_token).get_document(document_id=resp.document_id)
    shorthand_doc = get_document(api_token=api_token, document_id=resp.document_id)
    assert isinstance(get_doc, Document)
    assert get_doc == shorthand_doc

    for data in ["", 0, {}, [], None, False, True]:
        with pytest.raises(ImperialError):
            get_document(document_id=data)
