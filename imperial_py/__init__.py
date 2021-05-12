__author__ = "Hexiro"
from .imperialbin import *
# not sure if i'm supposed to do use del, but i'm going to,
# so imperialbin module doesn't exist and everything is used directly from imperial_py.
# ie. imperial_py.create_document() and not imperial_py.imperialbin.create_document()
del imperialbin

__all__ = (
    # from imperialbin
    "Imperial",
    "create_document",
    "get_document",
    "edit_document",
    "delete_document",
    "verify",
    "purge_documents",
    # from client
    "client",
    # from exceptions
    "exceptions",
    # from checks
    "checks"
)
