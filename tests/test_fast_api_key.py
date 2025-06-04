from fastapi.testclient import TestClient
from . import app  # Replace with your FastAPI app import

client = TestClient(app)

def test_query_without_api_key():
    response = client.post("/api/query", json={"query": "test"})
    assert response.status_code == 401 or response.status_code == 403
    assert "Invalid" in response.text

def test_query_with_api_key():
    headers = {"X-API-Key": "your_valid_api_key_here"}
    response = client.post("/api/query", json={"query": "test"}, headers=headers)
    assert response.status_code == 200
    assert "answer" in response.json()
