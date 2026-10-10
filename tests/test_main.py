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
    assert response.json()["message"] == "Incident received"
    assert response.json()["incident"] == incident
def test_incident_missing_environment():
    incident = {
        "application": "payment-service",
        "problem": "502 Bad Gateway"

    }
    response =client.post("/incident", json=incident)
    assert response.status_code == 422
    
