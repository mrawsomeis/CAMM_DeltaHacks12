from moorcheh.client import client, SYSTEM_PROMPT
from moorcheh.retrieve import retrieve_combined_context

def generate_alert_message(user_id: str | None, address: str):
    """
    Generates a message for community members when someone is unresponsive.
    Combines:
    - SYSTEM_PROMPT (behavior rules)
    - Global guidelines
    - Optional user-specific medical info
    """
    # Retrieve context
    context_texts = retrieve_combined_context(user_id)
    combined_context = "\n".join(context_texts) if context_texts else "No context available."

    # Build prompt for Moorcheh
    prompt = f"""
Situation:
A person has collapsed and is unresponsive.

Location:
{address}

Guideline + personal info:
{combined_context}

Provide clear, calm guidance for nearby community members.
"""

    # Generate response using Moorcheh answer API
    response = client.answer.generate(
        namespace="first_aid_guidelines",
        query=f"{SYSTEM_PROMPT}\n\n{prompt}"
    )

    return response
