
import os
from google import genai


MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)


def generate_incident_response(
    incident: dict,
    analysis: dict,
    retrieved_knowledge: list
):
    """
    Generate an AI-powered DevOps incident response
    using Google Gemini and retrieved RAG knowledge.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is missing."
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an experienced DevOps engineer
and production incident response assistant.

Analyze the following incident using the
provided incident analysis and retrieved knowledge.

INCIDENT DETAILS:
Application: {incident.get("application")}
Problem: {incident.get("problem")}
Environment: {incident.get("environment")}

RULE-BASED ANALYSIS:
{analysis}

RETRIEVED KNOWLEDGE:
{retrieved_knowledge}

Provide your response in the following sections:

1. Incident Summary
2. Possible Root Causes
3. Recommended Investigation Steps
4. Suggested Resolution
5. Prevention Measures

Important instructions:
- Use the retrieved knowledge as supporting context.
- Do not invent facts about the actual infrastructure.
- Clearly distinguish possible causes from confirmed causes.
- Provide practical Kubernetes or DevOps commands where relevant.
- Never recommend destructive commands without explaining risks.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text
