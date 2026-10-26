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

    assert data["message"] == "Incident analyzed"
    assert data["incident"]["application"] == "payment-service"
    assert data["analysis"]["category"] == "Gateway Error"
    assert len(data["analysis"]["recommended_actions"]) > 0

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
    assert response.json()["analysis"]["category"] == "High CPU"


def test_memory_incident():
    incident = {
        "application": "payment-service",
        "problem": "Out of memory",
        "environment": "production"
    }

    response = client.post("/incident", json=incident)

    assert response.status_code == 200
    assert response.json()["analysis"]["category"] == "Memory Issue"


def test_unknown_incident():
    incident = {
        "application": "inventory-service",
        "problem": "Unexpected application behavior",
        "environment": "development"
    }

    response = client.post("/incident", json=incident)

    assert response.status_code == 200
    assert response.json()["analysis"]["category"] == "Unknown Incident"
