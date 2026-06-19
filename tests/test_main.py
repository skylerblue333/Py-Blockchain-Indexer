from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_index_and_latest():
    client.post("/api/v1/blocks", json={"hash": "0x123", "height": 100, "tx_count": 5})
    client.post("/api/v1/blocks", json={"hash": "0x456", "height": 101, "tx_count": 2})
    r = client.get("/api/v1/blocks/latest")
    assert r.status_code == 200
    assert r.json()["height"] == 101

