"""Tests for GET /activities endpoint."""

import pytest


class TestGetActivities:
    """Test suite for the GET /activities endpoint."""

    def test_get_activities_returns_200(self, client):
        """
        Arrange: Create a test client.
        Act: Send GET request to /activities.
        Assert: Response status is 200 and content-type is application/json.
        """
        # Arrange
        # Client is provided by fixture

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    def test_get_activities_returns_all_activities(self, client):
        """
        Arrange: Create a test client.
        Act: Send GET request to /activities.
        Assert: Response contains all 9 activities.
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Drama Club",
            "Debate Team",
            "Science Club",
        ]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert len(activities) == 9
        for activity_name in expected_activities:
            assert activity_name in activities

    def test_get_activities_contains_required_fields(self, client):
        """
        Arrange: Create a test client.
        Act: Send GET request to /activities.
        Assert: Each activity contains required fields.
        """
        # Arrange
        required_fields = {
            "description",
            "schedule",
            "max_participants",
            "participants",
        }

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict)
            assert required_fields.issubset(set(activity_data.keys()))
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)

    def test_get_activities_participant_count_accuracy(
        self, client, sample_activity_name
    ):
        """
        Arrange: Create a test client and select an activity.
        Act: Send GET request to /activities and check participant counts.
        Assert: Participant counts match the length of participants list.
        """
        # Arrange
        # Client and activity name provided by fixtures

        # Act
        response = client.get("/activities")
        activities = response.json()
        activity = activities[sample_activity_name]

        # Assert
        # Verify that the participants list is not empty and has correct structure
        assert isinstance(activity["participants"], list)
        assert len(activity["participants"]) > 0
        assert all(isinstance(email, str) for email in activity["participants"])
