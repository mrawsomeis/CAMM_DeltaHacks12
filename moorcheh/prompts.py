def build_moorcheh_prompt(retrieved_texts: list[str]):
    """
    Build prompt for Moorcheh LLM to generate safe instructions.
    """
    if not retrieved_texts:
        return """
You are assisting nearby community responders.

The person is unresponsive.
No medical info is available.

Provide general safety guidance:
- Ensure the person is safe from injury
- Call emergency services
- Avoid providing medical diagnosis
"""

    context_block = "\n".join(f"- {text}" for text in retrieved_texts)

    return f"""
You are assisting nearby community responders.

The person is unresponsive.
Relevant medical information (minimal personal info):
{context_block}

Generate 3 short, actionable instructions for responders.
Do NOT diagnose. Focus on immediate safety and accessibility.
"""
