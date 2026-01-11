
# NOTES ON VIBE CODE:

# This takes in a "situation" string (e.g., "Person appears to be having a seizure")
# and retrieves the top-k relevant medical context documents for the user.

# However, we will only be able to obtain user_id through facial recognition
# Recognizing the situation will likely require some computer vision model
# or at least some rules-based determination for detected actions..

from client import moorcheh_client

def retrieve_medical_context(user_id: str, k: int = 3):
    """
    Retrieves only the most relevant medical text
    for an unresponsive person.
    """

    results = moorcheh_client.documents.search(
        namespace="medical_records",
        query="collapsed unresponsive safety considerations",
        top_k=k,
        filters={"user_id": user_id}
    )

    return [r["text"] for r in results]
