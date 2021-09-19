import json
from datetime import datetime

import pytest

from .response_creator import Response
from ..document import Document
from ..utils.hostname import https
from ..exceptions import ImperialError
from imperial_py import imperialbin as imperial_py

api_token = "IMPERIAL-00000000-0000-0000-0000-000000000000"


def test_create_document(requests_mock):
    resp = Response.POST()
    deletion_resp = Response.DELETE(resp)
    requests_mock.post(url=str(https.imperialbin / "api" / "document"),
                       text=resp.json)
    requests_mock.delete(url=str(https.imperialbin / "api" / "document" / deletion_resp.document_id),
                         text=deletion_resp.json)
    content = "test"

    create_doc = imperial_py.Imperial(api_token=api_token).create_document(content=content)
    shorthand_doc = imperial_py.create_document(api_token=api_token, content=content)
    assert create_doc == shorthand_doc
    assert isinstance(create_doc, Document)

    # check invalid data for code
    for data in ["", 0, {}, [], None, False, True]:
        with pytest.raises(ImperialError):
            imperial_py.create_document(content=data)

    # check w/o api key

    create_doc = imperial_py.create_document(content=content,
                                             longer_urls=True,
                                             language="python",
                                             instant_delete=True,
                                             image_embed=True,
                                             expiration=30,
                                             encrypted=True,
                                             password="susimposter")
    assert create_doc.longer_urls is False
    assert create_doc.language == "auto"
    assert create_doc.instant_delete is False
    assert create_doc.image_embed is False
    assert (create_doc.expiration - create_doc.creation).days == 5
    assert create_doc.encrypted is False
    assert create_doc.password is None
