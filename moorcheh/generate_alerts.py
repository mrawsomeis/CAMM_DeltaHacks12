from moorcheh.client import get_moorcheh_client
from moorcheh.retrieve import retrieve_relevant_medical_context
from moorcheh.prompts import build_moorcheh_prompt

def generate_alert(user_id: str):
    """
    Triggered only if NOT_RESPONSIVE.
    Retrieves minimal medical info from Moorcheh and uses Moorcheh LLM
    to generate safe instructions for nearby community responders.
    """
    client = get_moorcheh_client()

    # Step 1: Retrieve relevant medical info
    medical_context = retrieve_relevant_medical_context(user_id)

    # Step 2: Build prompt for Moorcheh LLM
    prompt = build_moorcheh_prompt(medical_context)

    # Step 3: Generate instructions using Moorcheh LLM
    response = client.llm(prompt=prompt, model="cohere-v3.5")  # or Moorcheh default LLM

    return {
        "user_id": user_id,
        "status": "NOT_RESPONSIVE",
        "instructions": response.get("output", "")
    }
