def test_get_activities_returns_known_activity(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json()["Chess Club"]["description"] == (
        "Learn strategies and compete in chess tournaments"
    )


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
