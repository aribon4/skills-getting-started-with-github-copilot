import copy

import pytest # pyright: ignore[reportMissingImports]
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    original = copy.deepcopy(activities)
    with TestClient(app) as test_client:
        yield test_client
    activities.clear()
    activities.update(original)


def test_unregister_participant_removes_email(client):
    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_missing_participant_returns_404(client):
    response = client.delete("/activities/Chess Club/participants/unknown@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"
