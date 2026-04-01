def test_signup_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]


def test_signup_activity_not_found(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_already_signed_up(client):
    # Arrange — michael@mergington.edu is a pre-existing participant in Chess Club
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Already signed up for this activity"


def test_signup_activity_full(client):
    # Arrange — Tennis Club has max_participants=10 and 2 existing participants; fill remaining 8 spots
    activity_name = "Tennis Club"
    for i in range(8):
        client.post(f"/activities/{activity_name}/signup", params={"email": f"filler{i}@mergington.edu"})

    # Act — attempt to sign up one more student beyond capacity
    response = client.post(f"/activities/{activity_name}/signup", params={"email": "overflow@mergington.edu"})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_signup_adds_email_to_participants(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]
