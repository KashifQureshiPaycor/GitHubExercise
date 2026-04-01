def test_unregister_success(client):
    # Arrange — michael@mergington.edu is a pre-existing participant in Chess Club
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]


def test_unregister_activity_not_found(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_not_found(client):
    # Arrange — this email is not registered in Chess Club
    activity_name = "Chess Club"
    email = "nobody@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_removes_email_from_participants(client):
    # Arrange — michael@mergington.edu is a pre-existing participant in Chess Club
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]
