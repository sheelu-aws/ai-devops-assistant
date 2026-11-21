
import os
import pytest

from app.llm import generate_incident_response


@pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY"),
    reason="Gemini API key is not available"
)
def test_gemini_generates_incident_response():

    incident = {
        "application": "payment-service",
        "problem": "502 Bad Gateway",
        "environment": "production"
    }

    analysis = {
        "category": "Gateway Error",
        "severity": "High"
    }

    retrieved_knowledge = [
        """
        HTTP 502 Bad Gateway:
        Check backend health, application logs,
        load balancer configuration and connectivity.
        """
    ]

    response = generate_incident_response(
        incident=incident,
        analysis=analysis,
        retrieved_knowledge=retrieved_knowledge
    )

    assert response is not None
    assert isinstance(response, str)
    assert len(response.strip()) > 50
