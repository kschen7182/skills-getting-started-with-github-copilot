"""Tests for DELETE /activities/{activity_name}/participants/{email} endpoint."""

import pytest


class TestRemoveParticipant:
    """Test suite for the DELETE /participants endpoint."""

    def test_remove_participant_valid(
        self, client, sample_activity_name, existing_participant_email
    ):
        """
        Arrange: Create a test client with existing participant.
        Act: Send DELETE request to remove participant.
        Assert: Response status is 200 and success message returned.
        """
        # Arrange
        url = f"/activities/{sample_activity_name}/participants/{existing_participant_email}"

        # Act
        response = client.delete(url)

        # Assert
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]
        assert existing_participant_email in response.json()["message"]

    def test_remove_participant_removed_from_list(
        self, client, sample_activity_name, existing_participant_email
    ):
        """
        Arrange: Create a test client with existing participant.
        Act: Send DELETE, then GET activities.
        Assert: Email no longer in activity's participants list.
        """
        # Arrange
        url = f"/activities/{sample_activity_name}/participants/{existing_participant_email}"

        # Act
        delete_response = client.delete(url)
        activities_response = client.get("/activities")
        activities = activities_response.json()

        # Assert
        assert delete_response.status_code == 200
        assert existing_participant_email not in activities[sample_activity_name]["participants"]

    def test_remove_participant_not_found_returns_400(
        self, client, sample_activity_name, sample_email
    ):
        """
        Arrange: Create a test client with email not in activity.
        Act: Send DELETE for email not in participants list.
        Assert: Response status is 400 and error message provided.
        """
        # Arrange
        url = f"/activities/{sample_activity_name}/participants/{sample_email}"

        # Act
        response = client.delete(url)

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_remove_participant_activity_not_found_returns_404(
        self, client, existing_participant_email
    ):
        """
        Arrange: Create a test client with non-existent activity.
        Act: Send DELETE to non-existent activity.
        Assert: Response status is 404 and error message provided.
        """
        # Arrange
        url = f"/activities/NonExistentActivity/participants/{existing_participant_email}"

        # Act
        response = client.delete(url)

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_remove_participant_decreases_count(self, client, sample_activity_name):
        """
        Arrange: Create a test client and get initial participant count.
        Act: Remove one participant, then get updated count.
        Assert: Participant count decreased by 1.
        """
        # Arrange
        initial_activities = client.get("/activities").json()
        initial_count = len(
            initial_activities[sample_activity_name]["participants"]
        )
        participant_to_remove = initial_activities[sample_activity_name]["participants"][0]
        url = f"/activities/{sample_activity_name}/participants/{participant_to_remove}"

        # Act
        client.delete(url)
        updated_activities = client.get("/activities").json()
        updated_count = len(
            updated_activities[sample_activity_name]["participants"]
        )

        # Assert
        assert updated_count == initial_count - 1

    def test_remove_and_readd_same_participant(
        self, client, sample_activity_name, existing_participant_email
    ):
        """
        Arrange: Create a test client with existing participant.
        Act: Remove participant, then add them back with signup.
        Assert: Participant re-added successfully.
        """
        # Arrange
        delete_url = f"/activities/{sample_activity_name}/participants/{existing_participant_email}"
        signup_url = f"/activities/{sample_activity_name}/signup"
        signup_params = {"email": existing_participant_email}

        # Act
        delete_response = client.delete(delete_url)
        signup_response = client.post(signup_url, params=signup_params)
        activities = client.get("/activities").json()

        # Assert
        assert delete_response.status_code == 200
        assert signup_response.status_code == 200
        assert existing_participant_email in activities[sample_activity_name]["participants"]
