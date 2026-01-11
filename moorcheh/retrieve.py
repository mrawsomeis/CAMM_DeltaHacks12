from client import client

def retrieve_combined_context(user_id: str | None):
    context_texts = []

    # General guidelines
    general_results = client.similarity_search.query(
        namespaces=["first_aid_guidelines"],
        query="unresponsive person first aid and support",
        top_k=5
    )

    for r in general_results.get("results", []):
        context_texts.append(r.get("text", ""))

    # User medical info (optional)
    if user_id:
        personal_results = client.similarity_search.query(
            namespaces=["medical_records"],
            query="relevant medical information",
            top_k=3
        )
        for r in personal_results.get("results", []):
            if r.get("id") == user_id:
                context_texts.append(r.get("text", ""))

    return context_texts

