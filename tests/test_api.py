from copy import deepcopy
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)

ORIGINAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    yield


def test_get_activities():
    # Arrange
    # Current activities are populated by fixture reset.

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_activity():
    # Arrange
    email = "tester@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{quote(activity_name)}/signup?email={quote(email)}")

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate():
    # Arrange
    email = "dup@example.com"
    activity_name = "Chess Club"
    first_response = client.post(f"/activities/{quote(activity_name)}/signup?email={quote(email)}")
    assert first_response.status_code == 200

    # Act
    duplicate_response = client.post(f"/activities/{quote(activity_name)}/signup?email={quote(email)}")

    # Assert
    assert duplicate_response.status_code == 400


def test_remove_participant():
    # Arrange
    existing_email = "michael@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.delete(f"/activities/{quote(activity_name)}/participants?email={quote(existing_email)}")

    # Assert
    assert response.status_code == 200
    assert existing_email not in activities[activity_name]["participants"]


def test_remove_nonexistent_participant():
    # Arrange
    activity_name = "Chess Club"
    missing_email = "nonexistent@mergington.edu"

    # Act
    response = client.delete(f"/activities/{quote(activity_name)}/participants?email={quote(missing_email)}")

    # Assert
    assert response.status_code == 404
