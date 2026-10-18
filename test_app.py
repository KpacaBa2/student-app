"""Unit tests for Student & Course API."""

import pytest
from app import app


@pytest.fixture
def client():
    """Create test client fixture for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_index(client):
    """Test GET / endpoint returns correct text and status 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "Student Information System"


def test_courses(client):
    """Test GET /courses endpoint and check DevOps Engineering presence."""
    response = client.get("/courses")
    assert response.status_code == 200
    data = response.get_json()
    assert "courses" in data
    assert isinstance(data["courses"], list)
    assert "DevOps Engineering" in data["courses"]
    assert "Information Security" in data["courses"]
    assert "Database Systems" in data["courses"]


def test_health(client):
    """Test GET /health endpoint returns status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"status": "ok"}


def test_calculate_gpa_success(client):
    """Test POST /calculate-gpa endpoint with valid grades."""
    payload = {"grades": [4.0, 3.5]}
    response = client.post("/calculate-gpa", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"gpa": 3.75}


def test_calculate_gpa_error(client):
    """Test POST /calculate-gpa endpoint returns 400 for empty grades list."""
    payload = {"grades": []}
    response = client.post("/calculate-gpa", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data == {"error": "Invalid grades"}


def test_calculate_gpa_missing_key(client):
    """Test POST /calculate-gpa returns 400 when grades key is missing."""
    response = client.post("/calculate-gpa", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data == {"error": "Invalid grades"}


def test_calculate_gpa_invalid_items(client):
    """Test POST /calculate-gpa returns 400 when grades contain invalid types."""
    response = client.post("/calculate-gpa", json={"grades": ["A", 4.0]})
    assert response.status_code == 400
    data = response.get_json()
    assert data == {"error": "Invalid grades"}
