
# NOTES ON VIBE CODE:

# This takes in a "situation" string (e.g., "Person appears to be having a seizure")
# and retrieves the top-k relevant medical context documents for the user.

# However, we will only be able to obtain user_id through facial recognition
# Recognizing the situation will likely require some computer vision model
# or at least some rules-based determination for detected actions..

from moorcheh.client import get_moorcheh_client

def retrieve_relevant_context(
    user_id: str,
    visual_cues: list[str] = None,
    top_k: int = 3
):
    client = get_moorcheh_client()
    collection_name = f"user_{user_id}_medical"

    query = "Person is not responsive and may require immediate assistance."

    if visual_cues:
        query += " Observed cues: " + ", ".join(visual_cues) + "."

    results = client.search(
        collection_name=collection_name,
        query=query,
        limit=top_k,
        relevance_threshold=0.6
    )

    return [r["text"] for r in results]


# EXAMPLE USAGE:

#situation = "Person appears to be having a seizure"

#context = retrieve_relevant_context(
#    user_id="a9f3c2e1",
#    situation=situation
#)

# Should return:

#- User has epilepsy. Do not restrain limbs during a seizure.
#- User may be non-verbal during distress.