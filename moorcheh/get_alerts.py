from moorcheh.client import moorcheh_client
from moorcheh.retrieve import retrieve_combined_context

def generate_alert_message(user_id: str | None, address: str):
    """
    Uses:
    - Global first aid & mental health guidelines
    - Optional user-specific medical info
    """

    context_texts = retrieve_combined_context(user_id)
    combined_context = "\n".join(context_texts) if context_texts else "No context available."

    prompt = f"""
Situation:
A person has collapsed and is unresponsive.
Location:
{address}

Guideline + personal info:
{combined_context}

Provide guidance for nearby community members.
"""

    response = moorcheh_client.llm.generate(
        prompt=prompt,
        temperature=0.2
    )

    return response.text
