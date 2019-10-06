# pylint: disable=redefined-outer-name
import pytest
from starlette.testclient import TestClient

from service.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_index(client):
    resp = client.get('/')
    assert resp.status_code == 200


def test_assignment_empty_request(client):
    resp = client.post('/api/assignment')
    assert resp.status_code == 422


def test_assignment_validation_fail(client):
    payload = {
        'DM_capacity': 0,
        # 'DE_capacity': 0,
        'data_centers': [
            {'name': '', 'servers': 0},
            {'name': 'Stockholm', 'servers': 20},
        ]
    }
    resp = client.post('/api/assignment', json=payload)
    payload = resp.json()

    # We have errors in 4 fields
    assert len(payload['detail']) == 4
    assert resp.status_code == 422


def test_assignment_validation_success(client):
    payload = {
        'DM_capacity': 1,
        'DE_capacity': 1,
        'data_centers': [
            {'name': 'Paris', 'servers': 9},
            {'name': 'Stockholm', 'servers': 20},
        ]
    }
    resp = client.post('/api/assignment', json=payload)

    assert resp.status_code == 200
