# test_add_rule.py
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_add_rule(client):
    new_rule = {
        "name": "Temperature Rule",
        "conditions": [{"property": "temperature", "operator": ">", "value": "30"}],
    }
    response = client.post("/addRules", json=new_rule)
    assert response.status_code == 200
    assert response.json['message'] == "Rule and conditions added successfully."
