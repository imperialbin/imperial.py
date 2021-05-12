from .check_api_token import check_api_token
from .create_document import create_document
from .delete_document import delete_document
from .edit_document import edit_document
from .get_document import get_document
from .purge_documents import purge_documents

# don't think I need to add __all__(s) because they get shadowed by their function name
# ex. client.check_api_token accesses the function and not the module

__all__ = (
    "check_api_token",
    "create_document",
    "delete_document",
    "edit_document",
    "get_document",
    "purge_documents"
)
