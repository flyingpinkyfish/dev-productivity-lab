from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health():
    assert client.get("/health").json() == {"status": "ok"}

def test_add():
    assert client.get("/add", params={"a": 2, "b": 3}).json() == {"result": 5}
