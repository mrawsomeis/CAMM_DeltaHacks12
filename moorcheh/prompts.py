def responder_prompt(context_docs: list[str]):
    if not context_docs:
        return """
You are assisting nearby community responders.

The person is not responsive.
No personal medical context is available.

Provide general safety-focused guidance.
Avoid diagnosis. Be calm and clear.
"""

    context = "\n".join(f"- {doc}" for doc in context_docs)

    return f"""
You are assisting nearby community responders.

The person is not responsive.
Relevant, consented medical and accessibility information:
{context}

Generate 3 short, actionable instructions.
Do NOT diagnose.
Do NOT assume cause.
Focus on immediate safety.
"""
