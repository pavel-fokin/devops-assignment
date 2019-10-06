# pylint: disable=redefined-outer-name
import asynctest
import pytest
from starlette.testclient import TestClient

from service.main import app
from service import assignment


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


def test_assignment_validation_success(client, mocker):
    solver_solve = mocker.patch(
        'service.solver.solve',
        new_callable=asynctest.CoroutineMock,
        return_value={},
    )

    payload = {
        'DM_capacity': 1,
        'DE_capacity': 1,
        'data_centers': [
            {'name': 'Paris', 'servers': 9},
            {'name': 'Stockholm', 'servers': 20},
        ]
    }
    resp = client.post('/api/assignment', json=payload)

    solver_solve.assert_awaited_once()
    assert resp.status_code == 200


def test_assignment_solve_failed(client, mocker):
    mocker.patch(
        'service.assignment.do',
        return_value=assignment.Solution(),
    )

    payload = {
        'DM_capacity': 1,
        'DE_capacity': 1,
        'data_centers': [
            {'name': 'Paris', 'servers': 9},
            {'name': 'Stockholm', 'servers': 20},
        ]
    }
    resp = client.post('/api/assignment', json=payload)

    assert resp.status_code == 204
    payload = resp.json()
    assert payload['detail'] == 'No solution'


@pytest.mark.integration
def test_assignment_solved(client):
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
