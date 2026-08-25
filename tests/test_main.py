from fastapi.testclient import TestClient

import src.main as service

client = TestClient(service.app)
HASH_A = "0x" + "a" * 64
HASH_B = "0x" + "b" * 64


def setup_function():
    with service.catalog_lock:
        service.blocks_by_height.clear()
        service.height_by_hash.clear()


def test_health_and_readiness():
    assert client.get("/healthz").status_code == 200
    readiness = client.get("/readyz")
    assert readiness.status_code == 200
    assert readiness.json()["capacity"] == service.MAX_BLOCKS


def test_index_latest_and_by_height():
    first = client.post(
        "/v1/blocks",
        json={"block_hash": HASH_A, "height": 100, "tx_count": 5, "timestamp": 1000},
    )
    second = client.post(
        "/v1/blocks",
        json={"block_hash": HASH_B, "height": 101, "tx_count": 2, "timestamp": 1010},
    )
    assert first.status_code == 201
    assert second.status_code == 201
    assert client.get("/v1/blocks/latest").json()["height"] == 101
    assert client.get("/v1/blocks/100").json()["block_hash"] == HASH_A


def test_idempotent_and_conflicting_blocks_are_distinct():
    payload = {"block_hash": HASH_A, "height": 7, "tx_count": 1}
    assert client.post("/v1/blocks", json=payload).status_code == 201
    existing = client.post("/v1/blocks", json=payload)
    assert existing.status_code == 200
    assert existing.json()["status"] == "existing"
    conflict = client.post(
        "/v1/blocks", json={"block_hash": HASH_B, "height": 7, "tx_count": 1}
    )
    assert conflict.status_code == 409
    duplicate_hash = client.post(
        "/v1/blocks", json={"block_hash": HASH_A, "height": 8, "tx_count": 1}
    )
    assert duplicate_hash.status_code == 409


def test_rejects_invalid_fields_and_missing_blocks():
    assert client.post(
        "/v1/blocks", json={"block_hash": "0x123", "height": 1, "tx_count": 0}
    ).status_code == 422
    assert client.post(
        "/v1/blocks", json={"block_hash": HASH_A, "height": -1, "tx_count": 0}
    ).status_code == 422
    assert client.get("/v1/blocks/latest").status_code == 404
    assert client.get("/v1/blocks/99").status_code == 404


def test_capacity_fails_closed(monkeypatch):
    monkeypatch.setattr(service, "MAX_BLOCKS", 1)
    assert client.post(
        "/v1/blocks", json={"block_hash": HASH_A, "height": 1, "tx_count": 0}
    ).status_code == 201
    assert client.post(
        "/v1/blocks", json={"block_hash": HASH_B, "height": 2, "tx_count": 0}
    ).status_code == 503
