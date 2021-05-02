from .is_invalid_string import is_invalid_string
from ..exceptions import ImperialError


def ensure_document_id(document_id: str):
    if is_invalid_string(document_id):
        raise ImperialError(message="We couldn't find that document!", status=404)
