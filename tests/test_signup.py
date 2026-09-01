"""Tests for POST /activities/{activity_name}/signup endpoint."""

import pytest


class TestSignupForActivity:
    """Test suite for the POST /signup endpoint."""

    def test_signup_valid_new_participant(self, client, sample_activity_name, sample_email):
        """
        Arrange: Create a test client with an activity and new email.
        Act: Send POST signup request with new participant email.
        Assert: Response status is 200 and participant is added.
        """
        # Arrange
        url = f"/activities/{sample_activity_name}/signup"
        params = {"email": sample_email}

        # Act
        response = client.post(url, params=params)

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert sample_email in response.json()["message"]

    def test_signup_participant_added_to_list(
        self, client, sample_activity_name, sample_email
    ):
        """
        Arrange: Create a test client and prepare new participant.
        Act: Send POST signup, then GET activities.
        Assert: New email appears in activity's participants list.
        """
        # Arrange
        signup_url = f"/activities/{sample_activity_name}/signup"
        signup_params = {"email": sample_email}

        # Act
        signup_response = client.post(signup_url, params=signup_params)
        activities_response = client.get("/activities")
        activities = activities_response.json()

        # Assert
        assert signup_response.status_code == 200
        assert sample_email in activities[sample_activity_name]["participants"]

    def test_signup_duplicate_email_returns_400(
        self, client, sample_activity_name, existing_participant_email
    ):
        """
        Arrange: Create a test client with existing participant.
        Act: Send POST signup with same email again.
        Assert: Response status is 400 and error message provided.
        """
        # Arrange
        url = f"/activities/{sample_activity_name}/signup"
        params = {"email": existing_participant_email}

        # Act
        response = client.post(url, params=params)

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_activity_not_found_returns_404(self, client, sample_email):
        """
        Arrange: Create a test client with non-existent activity name.
        Act: Send POST signup to non-existent activity.
        Assert: Response status is 404 and error message provided.
        """
        # Arrange
        url = "/activities/NonExistentActivity/signup"
        params = {"email": sample_email}

        # Act
        response = client.post(url, params=params)

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_with_special_characters_in_email(
        self, client, sample_activity_name
    ):
        """
        Arrange: Create a test client with email containing special characters.
        Act: Send POST signup with email containing allowed special characters.
        Assert: Response status is 200 and signup succeeds.
        """
        # Arrange
        special_email = "student+2024@mergington.edu"
        url = f"/activities/{sample_activity_name}/signup"
        params = {"email": special_email}

        # Act
        response = client.post(url, params=params)

        # Assert
        assert response.status_code == 200
        activities = client.get("/activities").json()
        assert special_email in activities[sample_activity_name]["participants"]
