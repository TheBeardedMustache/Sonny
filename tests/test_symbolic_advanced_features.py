import pytest
from fastapi.testclient import TestClient

# Advanced symbolic AI endpoints integration tests
from services.symbolic_ai_service.backend.symbolic_service import app as symbolic_app

@pytest.fixture(scope="module")
def client():
    return TestClient(symbolic_app)

def test_analyze_endpoint(client):
    response = client.post("/analyze/", json={"text": "Example analysis text"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "analysis" in data

def test_plan_endpoint(client):
    response = client.post("/plan/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "tasks" in data and isinstance(data["tasks"], list)

def test_memory_endpoint(client):
    response = client.get("/memory/", params={"key": "test_key"})
    assert response.status_code == 200
    data = response.json()
    assert data.get("key") == "test_key"
    assert "value" in data