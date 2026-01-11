# NOTE FOR FRONTEND:

# from moorcheh.ingest import ingest_medical_info

# ingest_medical_info(user_id, medical_text_string)


from moorcheh.client import client
from moorcheh_sdk import ConflictError

NAMESPACE = "medical_records"

def ingest_medical_info(user_id: str, medical_text: str):
    """
    Upload a user medical record into Moorcheh.
    """
    # Create namespace if not exists
    try:
        client.namespaces.create(namespace_name=NAMESPACE, type="text")
    except ConflictError:
        pass

    doc = [{"id": user_id, "text": medical_text}]
    res = client.documents.upload(namespace_name=NAMESPACE, documents=doc)
    return res

