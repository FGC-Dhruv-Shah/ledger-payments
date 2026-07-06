from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health_returns_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["version"] == "1.2.0"


def test_openapi_schema_available():
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    assert "/payments" in "".join(resp.json()["paths"].keys())
