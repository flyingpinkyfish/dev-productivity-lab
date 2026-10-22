from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health():
    assert client.get("/health").json() == {"status": "ok"}

def test_add():
    assert client.get("/add", params={"a": 2, "b": 3}).json() == {"result": 5}

def test_subtract():
    assert client.get("/subtract", params={"a": 2, "b": 3}).json() == {"result": -1}

def test_version():
    assert client.get("/version").json() == {"version": "0.1.0"}

def test_multiply():
    assert client.get("/multiply", params={"a": 3, "b": 4}).json() == {"result": 12}

def test_add_rejects_large_numbers():
    response = client.get("/add", params={"a": 1_000_001, "b": 1})
    assert response.status_code == 422


def test_add_accepts_limit():
    response = client.get("/add", params={"a": 1_000_000, "b": 1})
    assert response.json() == {"result": 1_000_001}

def test_root():
    assert client.get("/").json() == {"message": "dev-productivity-lab"}
