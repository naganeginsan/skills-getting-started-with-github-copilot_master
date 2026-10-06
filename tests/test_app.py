from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_signup_and_unregister_participant():
    original = activities["Chess Club"]["participants"][:]
    try:
        activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

        response = client.post("/activities/Chess Club/signup?email=student@mergington.edu")
        assert response.status_code == 200
        assert "student@mergington.edu" in activities["Chess Club"]["participants"]

        unregister_response = client.delete(
            "/activities/Chess Club/participants/student@mergington.edu"
        )
        assert unregister_response.status_code == 200
        assert "student@mergington.edu" not in activities["Chess Club"]["participants"]
    finally:
        activities["Chess Club"]["participants"] = original


def test_delete_nonexistent_participant_returns_404():
    original = activities["Chess Club"]["participants"][:]
    try:
        activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

        response = client.delete("/activities/Chess Club/participants/noone@mergington.edu")

        assert response.status_code == 404
    finally:
        activities["Chess Club"]["participants"] = original
