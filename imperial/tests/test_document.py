import json
from datetime import datetime

from .response_creator import Response
from ..document import Document
from ..utils.hostname import https
from imperial_py import imperialbin as imperial_py
from secrets import compare_digest

api_token = "IMPERIAL-00000000-0000-0000-0000-000000000000"


def test_document(requests_mock):
    print("stared testing documents...")
    # text and json are needed so we instead just make text the dumps of the expected resp
    resp = Response.POST()
    deletion_resp = Response.DELETE(resp)

    requests_mock.post(url=str(https.imperialbin / "api" / "document"),
                       text=resp.json)

    requests_mock.delete(url=str(https.imperialbin / "api" / "document" / deletion_resp.document_id),
                         text=deletion_resp.json)

    print("testing document 1...")

    content = "test"
    doc1 = imperial_py.create_document(content=content, api_token=api_token)
    assert isinstance(doc1, Document)
    # check content is passed to doc properly
    assert doc1.content == content
    assert isinstance(doc1.content, str)
    # check properties
    assert doc1.link == resp.formatted_link
    assert doc1.id == resp.document_id
    assert doc1.language == resp.language
    assert doc1.longer_urls is False
    assert doc1.image_embed is False
    assert doc1.instant_delete is False
    assert doc1.editors == []
    assert doc1.encrypted is False
    assert doc1.password is None
    assert doc1.days_left in {4, 5}  # depends on latency
    # check aliases
    assert doc1.id == doc1.document_id
    assert doc1.editors == doc1.allowed_editors
    assert doc1.expiration == doc1.expiration_date
    assert doc1.creation == doc1.creation_date
    # check expirations get converted to datetime objs
    assert isinstance(doc1.creation, datetime)
    assert isinstance(doc1.expiration, datetime)
    # check params
    resp = Response.POST(longer_urls=True,
                         image_embed=True,
                         instant_delete=True,
                         encrypted=True,
                         expiration=8)
    # needed for pytest for some reason :shrug:
    deletion_resp = Response.DELETE(resp)
    requests_mock.post(url=str(https.imperialbin / "api" / "document"),
                       text=resp.json)
    requests_mock.delete(url=str(https.imperialbin / "api" / "document" / deletion_resp.document_id),
                         text=deletion_resp.json)

    print("testing document 2...")

    doc2 = imperial_py.create_document(content=content, api_token=api_token)
    assert doc2.longer_urls is True
    assert doc2.image_embed is True
    assert doc2.instant_delete is True
    assert doc2.encrypted is True
    assert compare_digest(doc2.password, resp.password)
    assert doc2.days_left in {8, 7}
