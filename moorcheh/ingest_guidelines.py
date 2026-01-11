from client import client
from moorcheh_sdk import ConflictError
import glob
import os

NAMESPACE = "first_aid_guidelines"
GUIDELINE_PATH = "firstaid_guidelines"

def ingest_first_aid_guidelines():
    """
    Upload all text files in firstaid_guidelines/ to Moorcheh
    """
    try:
        client.namespaces.create(namespace_name=NAMESPACE, type="text")
    except ConflictError:
        pass

    docs = []
    for filepath in glob.glob(os.path.join(GUIDELINE_PATH, "*.txt")):
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read().strip()
            doc_id = os.path.basename(filepath)
            docs.append({"id": doc_id, "text": text})

    res = client.documents.upload(namespace_name=NAMESPACE, documents=docs)
    return res
