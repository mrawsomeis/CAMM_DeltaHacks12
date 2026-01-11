# Here we initialize the Moorcheh client for use
# in medical document storage and retrieval.

# RAG with Moorcheh upon facial recognition so that
# correct, context-dependent and RELEVANT information
# is sent to nearby community members (who are opted in).

from moorcheh import Moorcheh
import os

def get_moorcheh_client():
    return Moorcheh(
        api_key=os.getenv("NEXT_PUBLIC_MOORCHEH_API_KEY")
    )

# we need to keep the API key secret
# so we will use environment variables to store it
# and load it from there