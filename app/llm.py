
def generate_incident_response(
    incident: dict,
    analysis: dict,
    retrieved_knowledge: list
):
    """
    Mock LLM provider.

    Simulates an LLM-generated incident response
    without requiring AWS credentials or an API key.
    """

    application = incident.get("application", "Unknown")
    problem = incident.get("problem", "Unknown problem")
    environment = incident.get("environment", "Unknown")

    category = analysis.get("category", "Unknown")
    severity = analysis.get("severity", "Unknown")

    knowledge = "\n\n".join(retrieved_knowledge)

    response = f"""
Incident Analysis Report

Application: {application}
Environment: {environment}

Reported Problem:
{problem}

Incident Classification:
{category}

Severity:
{severity}

Possible Causes:
"""

    for cause in analysis.get("possible_causes", []):
        response += f"- {cause}\n"

    response += "\nRecommended Actions:\n"

    for action in analysis.get("recommended_actions", []):
        response += f"- {action}\n"

    response += f"""

Relevant Troubleshooting Knowledge:

{knowledge}

Summary:
The incident has been analyzed using the available
classification rules and retrieved troubleshooting
knowledge. Follow the recommended actions to
investigate and resolve the issue.
"""

    return response.strip()
