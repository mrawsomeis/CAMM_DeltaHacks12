from moorcheh.retrieve import retrieve_relevant_context
from moorcheh.prompts import responder_prompt

def generate_alert(
    user_id: str,
    visual_cues: list[str],
    llm_client
):
    context_docs = retrieve_relevant_context(
        user_id=user_id,
        visual_cues=visual_cues
    )

    prompt = responder_prompt(context_docs)
    response = llm_client.generate(prompt)

    return {
        "user_id": user_id,
        "status": "NOT_RESPONSIVE",
        "visual_cues": visual_cues,
        "instructions": response
    }
