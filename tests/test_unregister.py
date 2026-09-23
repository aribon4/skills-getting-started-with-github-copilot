from src.app import activities


def test_unregister_participant_removes_email(client):
    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_missing_participant_returns_404(client):
    response = client.delete("/activities/Chess Club/participants/unknown@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"


def test_unregister_missing_activity_returns_404(client):
    response = client.delete("/activities/Unknown Club/participants/michael@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
