
# NOTES ON VIBE CODE:

# This takes in a "situation" string (e.g., "Person appears to be having a seizure")
# and retrieves the top-k relevant medical context documents for the user.

# However, we will only be able to obtain user_id through facial recognition
# Recognizing the situation will likely require some computer vision model
# or at least some rules-based determination for detected actions..

from moorcheh.client import get_moorcheh_client

def retrieve_relevant_medical_context(user_id: str):
    """
    Retrieve relevant medical info from Moorcheh for an unresponsive event.
    """
    client = get_moorcheh_client()
    collection_name = f"user_{user_id}_medical"

    # Query focused on collapsed / not responsive
    query = "Person is collapsed and not responsive"

    results = client.search(
        collection_name=collection_name,
        query=query,
        limit=3,
        relevance_threshold=0.5
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