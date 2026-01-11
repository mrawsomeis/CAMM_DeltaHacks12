
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


from moorcheh.client import moorcheh_client

def retrieve_combined_context(user_id: str | None):
    """
    Retrieves:
    - Global general first aid & mental health guidelines
    - Optional user-specific medical info
    """

    contexts = []

    # Always include general global guidelines
    general = moorcheh_client.documents.search(
        namespace="first_aid_guidelines",
        query="unresponsive person first aid and support",
        top_k=5
    )

    contexts += [r["text"] for r in general]

    # If user_id exists, include personalized medical info
    if user_id:
        personal = moorcheh_client.documents.search(
            namespace="medical_records",
            query="user-specific medical note relevance",
            top_k=3,
            filters={"user_id": user_id}
        )
        contexts += [r["text"] for r in personal]

    return contexts
