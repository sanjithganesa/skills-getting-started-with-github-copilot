"""Tests for GET /activities."""


def test_get_activities_returns_200_and_known_seed_data(client):
    # Arrange
    expected_activity = "Chess Club"
    expected_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert expected_activity in body
    assert expected_fields.issubset(body[expected_activity].keys())


def test_get_activities_every_entry_has_expected_schema(client):
    # Arrange
    expected_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    for name, details in response.json().items():
        assert expected_fields.issubset(details.keys()), f"{name} missing fields"
        assert isinstance(details["participants"], list)
        assert isinstance(details["max_participants"], int)
