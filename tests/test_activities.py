def test_get_activities_returns_200(client):
    # Arrange — no special setup needed; default activities are loaded via conftest

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200


def test_get_activities_returns_dict(client):
    # Arrange — no special setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert isinstance(response.json(), dict)


def test_get_activities_contains_known_activities(client):
    # Arrange — no special setup needed

    # Act
    response = client.get("/activities")

    # Assert
    activities = response.json()
    assert "Chess Club" in activities
    assert "Programming Class" in activities
