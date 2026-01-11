
# NOTES ON VIBE CODE:

# This takes in a "situation" string (e.g., "Person appears to be having a seizure")
# and retrieves the top-k relevant medical context documents for the user.

# However, we will only be able to obtain user_id through facial recognition
# Recognizing the situation will likely require some computer vision model
# or at least some rules-based determination for detected actions..

# CV SYSTEM SHOULD GIVE ME:

#{
#  "event": "NOT_RESPONSIVE",
#  "user_id": "abc123" | null
#}


from client import client

def retrieve_combined_context(user_id: str | None):
    """
    Retrieves:
    - General first-aid & mental health guidelines
    - Optional user-specific medical info
    """
    context_texts = []

    # 1. General guidelines
    general_results = client.similarity_search.query(
        namespaces=["first_aid_guidelines"],
        query="unresponsive person first aid and support",
        top_k=5
    )
    context_texts += [r["text"] for r in general_results]

    # 2. User-specific medical info
    if user_id:
        personal_results = client.similarity_search.query(
            namespaces=["medical_records"],
            query="user-specific medical note relevance",
            top_k=3
        )
        personal_texts = [r["text"] for r in personal_results if r.get("id") == user_id]
        context_texts += personal_texts

    return context_texts
