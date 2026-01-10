# Ingesting medical context, determines appropriate response
# SEE RETRIEVAL IN moorcheh/retrieve.py

# Should we continuously update? Update manually?

# FOR MVP --> one-ingestion?? Consult with team.

from moorcheh.client import get_moorcheh_client

def ingest_user_medical_docs(user_id: str, documents: list[str]):
    client = get_moorcheh_client()
    collection_name = f"user_{user_id}_medical"

    client.collections.create_if_not_exists(name=collection_name)

    for idx, doc in enumerate(documents):
        client.documents.add(
            collection_name=collection_name,
            document={
                "id": f"{user_id}_doc_{idx}",
                "text": doc,
                "metadata": {
                    "category": "medical_safety"
                }
            }
        )


# EXAMPLE USAGE:

#docs = [
#    "User has epilepsy. Do not restrain limbs during a seizure.",
#    "User has severe peanut allergy. Avoid exposure.",
#    "User may be non-verbal during distress."
#]

#ingest_user_medical_docs("a9f3c2e1", docs)
