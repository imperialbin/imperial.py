import pytest

from ..exceptions import ImperialError
from ..utils import parser
from requests import Response


def test_ensure_json():
    # this should never be done under normal circumstances
    resp = Response()
    resp._content = b"""{"success":true}"""
    # normal response w/ success true
    assert parser.ensure_json(resp) == {"success": True}

    # html response instead of json
    resp._content = b"""<!DOCTYPE html><head></head><body></body>"""
    with pytest.raises(ImperialError):
        parser.ensure_json(resp)

    # deprecated
    # # expected error
    # resp._content = b"""{"success":false, "message":"error message!"}"""
    # with pytest.raises(ImperialError):
    #     parser.ensure_json(resp)


def test_to_snake_case():
    # values will not get converted
    camel_case_dict = {
        "camelCase": None,
        "alsoCamelCase": {
            "thisWillBeChangedToo": None
        }
    }
    snake_case_dict = {
        "camel_case": None,
        "also_camel_case": {
            "this_will_be_changed_too": None
        }
    }
    assert parser.to_snake_case(camel_case_dict) == snake_case_dict
