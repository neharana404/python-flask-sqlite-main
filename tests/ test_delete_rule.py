# test_delete_rule.py
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_delete_rule(client):
    response = client.delete("/deleteRule/1")
    assert response.status_code == 200
    assert response.json['message'] == "Rule with ID 1 and its conditions have been deleted successfully."
