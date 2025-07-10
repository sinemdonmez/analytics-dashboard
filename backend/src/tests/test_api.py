

import os
os.environ["DB_URL"] = os.getenv("DB_URL", "your-test-db-url")  # Optional fallback

pytest_plugins = ["pytest_dotenv"]

from app.app import app
import pytest

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_active_users(client):
    response = client.get("/api/active-users")
    assert response.status_code == 200
    data = response.get_json()
    assert "active_users" in data
    assert isinstance(data["active_users"], int)

def test_total_purchases(client):
    response = client.get("/api/total-purchases")
    assert response.status_code == 200
    data = response.get_json()
    assert "total_purchases" in data
    assert isinstance(data["total_purchases"], (int, float))

def test_session_lengths(client):
    response = client.get("/api/session-lengths")
    assert response.status_code == 200
    data = response.get_json()
    assert "average_session_minutes" in data
    assert isinstance(data["average_session_minutes"], (int, float, type(None)))

def test_popular_levels(client):
    response = client.get("/api/popular-levels")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "level" in data[0]
        assert "play_count" in data[0]