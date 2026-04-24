"""Tests for DELETE /activities/{activity_name}/participants/{email}."""

from urllib.parse import quote


def test_unregister_happy_path_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # seeded in Chess Club

    # Act
    response = client.delete(f"/activities/{activity}/participants/{quote(email)}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity}"}
    participants = client.get("/activities").json()[activity]["participants"]
    assert email not in participants


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity = "Underwater Basket Weaving"
    email = "someone@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants/{quote(email)}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_email_not_registered_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "ghost@mergington.edu"  # not registered in Chess Club

    # Act
    response = client.delete(f"/activities/{activity}/participants/{quote(email)}")

    # Assert
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"].lower()


def test_unregister_url_encoded_email_path_param_works(client):
    # Arrange
    activity = "Chess Club"
    email = "daniel@mergington.edu"  # seeded in Chess Club
    encoded_email = quote(email, safe="")  # encodes '@' as %40

    # Act
    response = client.delete(f"/activities/{activity}/participants/{encoded_email}")

    # Assert
    assert response.status_code == 200
    participants = client.get("/activities").json()[activity]["participants"]
    assert email not in participants
