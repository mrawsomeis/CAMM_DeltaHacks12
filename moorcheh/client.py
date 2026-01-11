import os
from moorcheh_sdk import MoorchehClient

# Make sure MOORCHEH_API_KEY is set in environment variables
api_key = os.environ.get("MOORCHEH_API_KEY")
if not api_key:
    raise ValueError("Please set the MOORCHEH_API_KEY environment variable")

# Create a single reusable client instance
client = MoorchehClient(api_key=api_key)

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
