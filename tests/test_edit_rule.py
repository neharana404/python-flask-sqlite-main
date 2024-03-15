# test_edit_rule.py
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_edit_rule(client):
    updated_rule = {
        "rule_id": 1,
        "name": "Updated Rule",
        "conditions": [{"property": "humidity", "operator": "<", "value": "50"}],
    }
    response = client.put("/editRule", json=updated_rule)
    assert response.status_code == 200
    assert response.json['message'] == "Rule with ID 1 has been updated successfully."
