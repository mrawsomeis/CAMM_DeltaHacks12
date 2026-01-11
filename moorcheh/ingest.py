# Ingesting medical context, determines appropriate response
# SEE RETRIEVAL IN moorcheh/retrieve.py

# Should we continuously update? Update manually?


# NOTE FOR FRONTEND:

# from moorcheh.ingest import ingest_medical_info

# ingest_medical_info(user_id, medical_text_string)




from client import moorcheh_client

def ingest_medical_info(user_id: str, medical_text: str):
    """
    Called by external app/web backend when a user submits medical info.

    medical_text:
    - One long natural-language string
    - Stored as-is
    - Parsed later only if relevant
    """

    moorcheh_client.documents.add(
        namespace="medical_records",
        documents=[medical_text],
        metadata=[{"user_id": user_id}]
    )
