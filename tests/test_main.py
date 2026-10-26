
import os
import tempfile

os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="incident-tests-")

from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "AI DevOps Incident Assistant is running."
    }
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }

def test_create_incident():
    incident = {
        "application": "payment-service",
        "problem": "502 Bad Gateway",
        "environment": "production"
    }

    response = client.post("/incident", json=incident)

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Incident analyzed and saved"
    assert data["incident"]["application"] == "payment-service"
    assert data["incident"]["analysis"]["category"] == "Gateway Error"
    assert len(data["incident"]["analysis"]["recommended_actions"]) > 0

def test_incident_missing_environment():
    incident = {
        "application": "payment-service",
        "problem": "502 Bad Gateway"

    }
    response =client.post("/incident", json=incident)
    assert response.status_code == 422
    

def test_high_cpu_incident():
    incident = {
        "application": "order-service",
        "problem": "High CPU usage",
        "environment": "production"
    }

    response = client.post("/incident", json=incident)

    assert response.status_code == 200
    assert response.json()["incident"]["analysis"]["category"] == "High CPU"


def test_memory_incident():
    incident = {
        "application": "payment-service",
        "problem": "Out of memory",
        "environment": "production"
    }

    response = client.post("/incident", json=incident)

    assert response.status_code == 200
    assert response.json()["incident"]["analysis"]["category"] == "Memory Issue"


def test_unknown_incident():
    incident = {
        "application": "inventory-service",
        "problem": "Unexpected application behavior",
        "environment": "development"
    }

    response = client.post("/incident", json=incident)

    assert response.status_code == 200
    assert response.json()["incident"]["analysis"]["category"] == "Unknown Incident"

def test_filter_incidents_by_environment():
    response = client.get("/incidents?environment=production")

    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 1
    assert all(
        incident["environment"].lower() == "production"
        for incident in data["incidents"]
    )


def test_filter_incidents_by_category():
    response = client.get("/incidents?category=Gateway%20Error")

    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 1
    assert all(
        incident["analysis"]["category"].lower() == "gateway error"
        for incident in data["incidents"]
    )

def test_incident_summary():
    response = client.get("/incidents/summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_incidents" in data
    assert "production_incidents" in data
    assert "by_category" in data
    assert "by_environment" in data

    assert data["total_incidents"] == sum(
        data["by_category"].values()
    )

    assert data["production_incidents"] <= data["total_incidents"]


