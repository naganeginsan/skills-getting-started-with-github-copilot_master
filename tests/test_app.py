from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_signup_and_unregister_participant():
    # Arrange
    original_participants = activities["Chess Club"]["participants"][:]
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    try:
        # Act: sign up
        signup_response = client.post(
            "/activities/Chess Club/signup?email=student@mergington.edu"
        )

        # Assert: sign up succeeds
        assert signup_response.status_code == 200
        assert "student@mergington.edu" in activities["Chess Club"]["participants"]

        # Act: unregister
        unregister_response = client.delete(
            "/activities/Chess Club/participants/student@mergington.edu"
        )

        # Assert: unregister succeeds
        assert unregister_response.status_code == 200
        assert "student@mergington.edu" not in activities["Chess Club"]["participants"]
    finally:
        activities["Chess Club"]["participants"] = original_participants


def test_delete_nonexistent_participant_returns_404():
    # Arrange
    original_participants = activities["Chess Club"]["participants"][:]
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    try:
        # Act
        response = client.delete("/activities/Chess Club/participants/noone@mergington.edu")

        # Assert
        assert response.status_code == 404
    finally:
        activities["Chess Club"]["participants"] = original_participants
