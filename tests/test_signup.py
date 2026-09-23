import copy

from pytest import fixture  # pyright: ignore[reportMissingImports]
from fastapi.testclient import TestClient

from src.app import activities, app


@fixture
def client():
    original = copy.deepcopy(activities)
    with TestClient(app) as test_client:
        yield test_client
    activities.clear()
    activities.update(original)


def test_signup_adds_new_participant(client):
    response = client.post("/activities/Chess Club/signup?email=student@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up student@mergington.edu for Chess Club"
    assert "student@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_rejects_duplicate_participant(client):
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_rejects_full_activity(client):
    activities["Chess Club"]["max_participants"] = 2
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]

    response = client.post("/activities/Chess Club/signup?email=student@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_signup_missing_activity_returns_404(client):
    response = client.post("/activities/Unknown Club/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
