# test_get_rules.py
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_rules(client):
    response = client.get("/getRules")
    assert response.status_code == 200
    rules = response.json
    assert isinstance(rules, list)
