import os
from moorcheh_sdk import MoorchehClient

# Make sure NEXT_PUBLIC_MOORCHEH_API_KEY is set in environment variables
api_key = os.environ.get("NEXT_PUBLIC_MOORCHEH_API_KEY")
if not api_key:
    raise ValueError("Please set the NEXT_PUBLIC_MOORCHEH_API_KEY environment variable")

# Create a single reusable client instance
client = MoorchehClient(api_key=api_key)

def ensure_namespace_exists(namespace_name: str):
    namespaces = client.namespaces.list().get("namespaces", [])
    if not any(ns["namespace_name"] == namespace_name for ns in namespaces):
        raise RuntimeError(
            f"Moorcheh namespace '{namespace_name}' does not exist. "
            f"Run the ingestion script first."
        )

# Ensure required namespaces exist at startup
REQUIRED_NAMESPACES = ["first_aid_guidelines"]

for ns in REQUIRED_NAMESPACES:
    ensure_namespace_exists(ns)

# SYSTEM_PROMPT contains all behavior rules
SYSTEM_PROMPT = """
You are an AI assistant helping nearby community members assist a person in distress.
- The person is assumed collapsed and unresponsive.
- Do NOT diagnose medical conditions.
- Do NOT instruct contacting emergency services.
- Use global first aid and mental health first aid guidelines safely.
- Minimize personal or sensitive information.
- Provide calm, practical guidance.
- Give at most 3 short steps.
"""
