from ..exceptions import DocumentNotFound


def ensure_document_id(document_id: str):
    # document_id has to be a string, and has to be a valid length for a document id
    # 8 is standard; 26 with longer_urls enabled
    # `if not document_id` check is redundant, as it will be determined by len
    if not isinstance(document_id, str) or not (len(document_id) == 8 or len(document_id) == 26):
        raise DocumentNotFound(document_id)
