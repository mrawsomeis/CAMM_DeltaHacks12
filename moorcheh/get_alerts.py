from client import moorcheh_client
from retrieve import retrieve_medical_context

def generate_alert_message(user_id: str | None, address: str):
    """
    Triggered after:
    - NOT_RESPONSIVE
    - Voice prompt failed
    - No hand movement detected
    """

    if user_id is None:
        medical_context = "No medical information available."
    else:
        retrieved = retrieve_medical_context(user_id)
        medical_context = "\n".join(retrieved) if retrieved else "No medical information available."

    prompt = f"""
Situation:
A person has collapsed and is unresponsive.

Location:
{address}

Medical context:
{medical_context}

Provide guidance for nearby community members.
"""

    response = moorcheh_client.llm.generate(
        prompt=prompt,
        temperature=0.2
    )

    return response.text
