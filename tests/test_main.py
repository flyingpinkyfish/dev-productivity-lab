import logging

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_upper():
    response = client.get("/upper", params={"text": "Hello"})
    assert response.status_code == 200
    assert response.json() == {"result": "HELLO"}


def test_upper_already_capitals():
    response = client.get("/upper", params={"text": "ABC 123!"})
    assert response.status_code == 200
    assert response.json() == {"result": "ABC 123!"}

def test_first_char():
    response = client.get("/first_char", params={"text": "Hello"})
    assert response.status_code == 200
    assert response.json() == {"result": "H"}


def test_first_char_empty():
    response = client.get("/first_char", params={"text": ""})
    assert response.status_code == 400
    assert response.json() == {"detail": "Text must not be empty"}

def test_cube_number_success():
    response = client.get("/cube?n=3")
    assert response.status_code == 200
    assert response.json() == {"result": 27}

def test_cube_number_negative():
    response = client.get("/cube?n=-2")
    assert response.status_code == 200
    assert response.json() == {"result": -8}

def test_cube_number_missing_param():
    response = client.get("/cube")
    assert response.status_code == 422  # FastAPI validation error

def test_cube_number_invalid_type():
    response = client.get("/cube?n=abc")
    assert response.status_code == 422  # FastAPI validation error

def test_square_number():
    # Test with a positive integer
    response = client.get("/square?n=5")
    assert response.status_code == 200
    assert response.json() == {"result": 25}

def test_square_negative_number():
    # Test with a negative integer
    response = client.get("/square?n=-4")
    assert response.status_code == 200
    assert response.json() == {"result": 16}


def test_count_vowels():
    # Test with a standard string
    response = client.get("/vowels?text=hello")
    assert response.status_code == 200
    assert response.json() == {"result": 2}

def test_count_vowels_uppercase():
    # Test to ensure it counts uppercase vowels
    response = client.get("/vowels?text=FastAPI")
    assert response.status_code == 200
    assert response.json() == {"result": 3}

def test_concatenate():
    response = client.get("/concatenate", params={"a": "foo", "b": "bar"})
    assert response.status_code == 200
    assert response.json() == {"result": "foobar"}

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

def test_divide():
    assert client.get("/divide", params={"a": 10, "b": 4}).json() == {"result": 2.5}

def test_divide_by_zero():
    response = client.get("/divide", params={"a": 1, "b": 0})
    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot divide by zero"}

def test_echo():
    assert client.get("/echo", params={"text": "hello world"}).json() == {"text": "hello world"}

def test_request_logging(caplog):
    with caplog.at_level(logging.INFO, logger="uvicorn.error"):
        client.get("/health")
    assert "GET /health -> 200" in caplog.text
